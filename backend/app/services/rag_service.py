import os
from typing import List, Dict, Optional, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from openai import OpenAI
import cohere
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        
        # Initialize clients
        if self.qdrant_url:
            self.qdrant = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        else:
            # Fallback to local storage
            storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "qdrant_data")
            os.makedirs(storage_path, exist_ok=True)
            self.qdrant = QdrantClient(path=storage_path)
            logger.info(f"Using local Qdrant storage at {storage_path}")
            
        self.openai = OpenAI(api_key=self.openai_api_key)
        self.cohere = cohere.Client(self.cohere_api_key)
        
        self.collection_name = "health_insights"
        self.embedding_model = "text-embedding-3-small"
        self.vector_size = 1536  # Size for text-embedding-3-small

    def initialize_collection(self):
        """Initialize Qdrant collection if it doesn't exist"""
        try:
            collections = self.qdrant.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name not in collection_names:
                self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.vector_size,
                        distance=qmodels.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI"""
        try:
            response = self.openai.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def upsert_data(self, user_id: int, data_type: str, content: str, metadata: Dict[str, Any] = None):
        """Store data in Qdrant"""
        try:
            if not content:
                return

            embedding = self.embed_text(content)
            
            payload = {
                "user_id": user_id,
                "data_type": data_type,
                "content": content,
                **(metadata or {})
            }
            
            # Generate a deterministic ID based on content to avoid duplicates
            import hashlib
            point_id = hashlib.md5(f"{user_id}_{data_type}_{content}".encode()).hexdigest()
            
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    qmodels.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )
                ]
            )
            logger.info(f"Upserted {data_type} for user {user_id}")
        except Exception as e:
            logger.error(f"Error upserting data: {e}")
            raise

    def search(self, user_id: int, query: str, limit: int = 10) -> List[Dict]:
        """Retrieve relevant documents from Qdrant"""
        try:
            query_vector = self.embed_text(query)
            
            search_result = self.qdrant.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=qmodels.Filter(
                    must=[
                        qmodels.FieldCondition(
                            key="user_id",
                            match=qmodels.MatchValue(value=user_id)
                        )
                    ]
                ),
                limit=limit
            ).points
            
            return [
                {
                    "content": hit.payload.get("content"),
                    "metadata": hit.payload,
                    "score": hit.score
                }
                for hit in search_result
            ]
        except Exception as e:
            logger.error(f"Error searching data: {e}")
            raise

    def rerank(self, query: str, docs: List[Dict], top_n: int = 5) -> List[Dict]:
        """Rerank documents using Cohere"""
        try:
            if not docs:
                return []
                
            documents = [doc["content"] for doc in docs]
            
            results = self.cohere.rerank(
                query=query,
                documents=documents,
                top_n=top_n,
                model="rerank-english-v3.0"
            )
            
            reranked_docs = []
            for hit in results.results:
                doc = docs[hit.index]
                doc["rerank_score"] = hit.relevance_score
                reranked_docs.append(doc)
                
            return reranked_docs
        except Exception as e:
            logger.error(f"Error reranking data: {e}")
            # Fallback to original order if reranking fails
            return docs[:top_n]

    def generate_insight(self, user_id: int, query: str) -> str:
        """Generate insight using RAG pipeline with security audit logging"""
        try:
            # Security audit log
            logger.info(f"[SECURITY AUDIT] RAG query initiated - User ID: {user_id}, Query: '{query[:100]}'")
            
            # 1. Retrieve
            retrieved_docs = self.search(user_id, query, limit=10)
            logger.info(f"[SECURITY AUDIT] Retrieved {len(retrieved_docs)} documents for user {user_id}")
            
            # 2. Rerank
            reranked_docs = self.rerank(query, retrieved_docs, top_n=5)
            logger.info(f"[SECURITY AUDIT] Reranked to {len(reranked_docs)} documents for user {user_id}")
            
            # Warn if no data available
            if not reranked_docs:
                logger.warning(f"[SECURITY AUDIT] No context data available for user {user_id}")
            
            # 3. Generate
            context = "\n\n".join([f"Document {i+1}: {doc['content']}" for i, doc in enumerate(reranked_docs)])
            
            system_prompt = """You are an advanced AI health assistant with STRICT USER DATA ISOLATION requirements.

        CRITICAL SECURITY RULES - MUST FOLLOW:
        1. You MUST ONLY use information from the provided context below
        2. The context contains data EXCLUSIVELY for the currently authenticated user
        3. NEVER reference, mention, or infer information about other users/patients
        4. If the context is empty or insufficient, clearly state "I don't have enough data for this user"
        5. NEVER make assumptions or generate data not present in the context
        6. If asked about data belonging to another user, respond: "I can only access your personal health data"

        USER DATA ISOLATION:
        - All data in the context belongs to ONE user only
        - You are forbidden from accessing or mentioning any other user's data
        - Treat this as a HIPAA compliance requirement

        RESPONSE FORMAT:
        Return a valid JSON object with this structure:
        {
            "summary": "Brief summary based ONLY on provided context (1-2 sentences)",
            "metrics": [
                {
                    "label": "Metric Name",
                    "value": "Value with units",
                    "status": "Normal" | "High" | "Low" | "Warning" | "Good",
                    "insight": "Brief explanation"
                }
            ],
            "analysis": "Detailed analysis in markdown format using ONLY context data",
            "recommendations": [
                "Actionable recommendation based on context"
            ]
        }

        HANDLING INSUFFICIENT DATA:
        - If context is empty: Return empty metrics array and explain in summary: "I don't have enough health data for your account yet. Please add health records, medications, or appointments to get personalized insights."
        - If context is partial: Only analyze what's available
        - NEVER fabricate medical data or diagnoses

        Guidelines:
        - Provide personalized, actionable, empathetic insights
        - Cite specific data from the context
        - Do NOT make up medical diagnoses
        - Ensure JSON is valid and parseable
        """
        
            user_prompt = f"Context:\n{context}\n\nUser Question: {query}\n\nResponse (JSON):"
            
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            raise

# Singleton instance
rag_service = RAGService()
