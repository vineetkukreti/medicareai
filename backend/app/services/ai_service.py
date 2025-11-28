import os
import google.generativeai as genai
from typing import Optional

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.enabled = True
        else:
            self.enabled = False
            print("Warning: GEMINI_API_KEY not found. AI features will be disabled.")
    
    async def chat(self, message: str, context: Optional[str] = None) -> str:
        """
        Send a message to the AI chatbot and get a response
        """
        if not self.enabled:
            return "AI service is currently unavailable. Please configure GEMINI_API_KEY."
        
        try:
            # Create a medical-focused system prompt
            system_prompt = """You are MediCareAI, a caring and knowledgeable health companion.
            
            Your goal is to have a natural, human-like conversation about health.
            
            Guidelines:
            1. **Be Concise**: Give short, direct answers. Avoid long lectures unless asked.
            2. **Be Human**: Use a warm, conversational tone. Don't sound like a robot or a textbook.
            3. **Context Matters**: Remember what we just talked about. If I ask a follow-up, answer that specific follow-up.
            4. **Safety First, But Natural**: If you need to give a disclaimer, weave it naturally into the conversation. Don't just paste a standard warning block at the end every time.
            5. **No Diagnosis**: You can explain symptoms and suggest possibilities, but clarify you can't diagnose.
            
            If the user asks a simple question, give a simple answer.
            """
            
            # Combine system prompt with user message
            full_prompt = system_prompt
            if context:
                full_prompt += f"\n\nPrevious Conversation History:\n{context}\n\n"
            full_prompt += f"Current User Question: {message}\n\nAssistant:"
            
            response = self.model.generate_content(full_prompt)
            
            # Check if response is valid
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"I apologize, but I cannot answer that query due to safety guidelines (Reason: {response.prompt_feedback.block_reason}). Please try rephrasing."
            
            if not response.parts and not response.text:
                return "I apologize, but I couldn't generate a response. Please try again."
                
            return response.text
        except Exception as e:
            print(f"Error in AI chat: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."

    async def chat_stream(self, message: str, context: Optional[str] = None):
        """
        Stream the response from the AI chatbot
        """
        if not self.enabled:
            yield "AI service is currently unavailable. Please configure GEMINI_API_KEY."
            return
        
        try:
            # Create a medical-focused system prompt
            system_prompt = """You are MediCareAI, a caring and knowledgeable health companion.
            
            Your goal is to have a natural, human-like conversation about health.
            
            Guidelines:
            1. **Be Concise**: Give short, direct answers. Avoid long lectures unless asked.
            2. **Be Human**: Use a warm, conversational tone. Don't sound like a robot or a textbook.
            3. **Context Matters**: Remember what we just talked about. If I ask a follow-up, answer that specific follow-up.
            4. **Safety First, But Natural**: If you need to give a disclaimer, weave it naturally into the conversation. Don't just paste a standard warning block at the end every time.
            5. **No Diagnosis**: You can explain symptoms and suggest possibilities, but clarify you can't diagnose.
            
            If the user asks a simple question, give a simple answer.
            """
            
            # Combine system prompt with user message
            full_prompt = system_prompt
            if context:
                full_prompt += f"\n\nPrevious Conversation History:\n{context}\n\n"
            full_prompt += f"Current User Question: {message}\n\nAssistant:"
            
            response = self.model.generate_content(full_prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            print(f"Error in AI chat stream: {str(e)}")
            yield "I apologize, but I'm having trouble processing your request right now."
    
    async def analyze_symptoms(self, symptoms: str, age: Optional[int] = None, gender: Optional[str] = None) -> dict:
        """
        Analyze symptoms and provide possible conditions and recommendations
        """
        if not self.enabled:
            return {
                "possible_conditions": [],
                "recommendations": "AI service is currently unavailable.",
                "severity": "unknown"
            }
        
        try:
            prompt = f"""As a medical AI assistant, analyze the following symptoms and provide:
            1. Possible conditions (list 3-5 most likely)
            2. General recommendations
            3. Severity level (low, medium, high)
            
            Patient information:
            - Symptoms: {symptoms}
            - Age: {age if age else 'Not provided'}
            - Gender: {gender if gender else 'Not provided'}
            
            Provide your response in this exact format:
            POSSIBLE CONDITIONS:
            - [condition 1]
            - [condition 2]
            - [condition 3]
            
            RECOMMENDATIONS:
            [Your recommendations here]
            
            SEVERITY: [low/medium/high]
            
            Remember to always recommend consulting a healthcare professional for accurate diagnosis.
            """
            
            response = self.model.generate_content(prompt)
            
            # Check for safety blocks
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return {
                    "possible_conditions": ["Analysis blocked by safety filters"],
                    "recommendations": f"I cannot analyze these symptoms due to safety guidelines ({response.prompt_feedback.block_reason}). Please consult a doctor.",
                    "severity": "unknown"
                }
                
            try:
                result_text = response.text
            except Exception:
                return {
                    "possible_conditions": ["Unable to generate analysis"],
                    "recommendations": "Please try again or consult a healthcare professional.",
                    "severity": "medium"
                }
            
            # Parse the response
            possible_conditions = []
            recommendations = ""
            severity = "medium"
            
            lines = result_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if "POSSIBLE CONDITIONS:" in line:
                    current_section = "conditions"
                elif "RECOMMENDATIONS:" in line:
                    current_section = "recommendations"
                elif "SEVERITY:" in line:
                    severity_text = line.split("SEVERITY:")[-1].strip().lower()
                    if "low" in severity_text:
                        severity = "low"
                    elif "high" in severity_text:
                        severity = "high"
                    else:
                        severity = "medium"
                elif current_section == "conditions" and line.startswith("-"):
                    possible_conditions.append(line[1:].strip())
                elif current_section == "recommendations" and line:
                    recommendations += line + " "
            
            return {
                "possible_conditions": possible_conditions if possible_conditions else ["Unable to determine. Please consult a doctor."],
                "recommendations": recommendations.strip() if recommendations else "Please consult a healthcare professional for proper diagnosis and treatment.",
                "severity": severity
            }
        except Exception as e:
            print(f"Error in symptom analysis: {str(e)}")
            return {
                "possible_conditions": ["Unable to analyze symptoms"],
                "recommendations": "Please consult a healthcare professional.",
                "severity": "medium"
            }
    
    async def get_health_advice(self, topic: str) -> str:
        """
        Get general health advice on a specific topic
        """
        if not self.enabled:
            return "AI service is currently unavailable."
        
        try:
            prompt = f"""As a medical AI assistant, provide helpful and accurate health advice about: {topic}
            
            Keep the advice:
            - Evidence-based and factual
            - Easy to understand
            - Practical and actionable
            - Include when to see a doctor if relevant
            """
            
            response = self.model.generate_content(prompt)
            
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return "I cannot provide advice on this topic due to safety guidelines."
                
            try:
                return response.text
            except Exception:
                return "I apologize, but I couldn't generate advice at this moment."
        except Exception as e:
            print(f"Error getting health advice: {str(e)}")
            return "I apologize, but I'm unable to provide advice on this topic right now."

# Create a singleton instance
ai_service = AIService()
