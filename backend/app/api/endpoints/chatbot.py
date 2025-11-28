from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.schemas import ChatMessage, ChatResponse
from app.models import ChatConversation
from app.services.ai_service import ai_service
import uuid
import json

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(chat_message: ChatMessage, db: Session = Depends(get_db)):
    """
    Chat with the medical AI assistant
    """
    # Generate session ID if not provided
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Get conversation history
    history = get_conversation_history(session_id, db)
    
    # Get AI response with context
    bot_response = await ai_service.chat(chat_message.message, context=history)
    
    # Save conversation to database
    conversation = ChatConversation(
        session_id=session_id,
        user_message=chat_message.message,
        bot_response=bot_response
    )
    db.add(conversation)
    db.commit()
    
    return ChatResponse(
        response=bot_response,
        session_id=session_id
    )

@router.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    """
    Stream chat response from the medical AI assistant
    """
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Get conversation history
    # We need a DB session here since this is an async generator endpoint
    try:
        db = SessionLocal()
        history = get_conversation_history(session_id, db)
        db.close()
    except Exception as e:
        print(f"Error fetching history: {e}")
        history = ""
    
    async def generate():
        full_response = ""
        try:
            async for chunk in ai_service.chat_stream(chat_message.message, context=history):
                full_response += chunk
                yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"
        
        # Save to database after streaming is complete
        try:
            db = SessionLocal()
            conversation = ChatConversation(
                session_id=session_id,
                user_message=chat_message.message,
                bot_response=full_response
            )
            db.add(conversation)
            db.commit()
            db.close()
        except Exception as e:
            print(f"Error saving chat to DB: {e}")

    return StreamingResponse(generate(), media_type="text/plain")

def get_conversation_history(session_id: str, db: Session, limit: int = 5) -> str:
    """
    Retrieve recent conversation history for context
    """
    try:
        conversations = db.query(ChatConversation).filter(
            ChatConversation.session_id == session_id
        ).order_by(ChatConversation.created_at.desc()).limit(limit).all()
        
        # Reverse to get chronological order
        conversations.reverse()
        
        context_str = ""
        for conv in conversations:
            context_str += f"User: {conv.user_message}\nAssistant: {conv.bot_response}\n\n"
        
        return context_str
    except Exception as e:
        print(f"Error getting history: {e}")
        return ""

@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Get chat history for a specific session
    """
    conversations = db.query(ChatConversation).filter(
        ChatConversation.session_id == session_id
    ).order_by(ChatConversation.created_at).all()
    
    return {
        "session_id": session_id,
        "messages": [
            {
                "user": conv.user_message,
                "bot": conv.bot_response,
                "timestamp": conv.created_at
            }
            for conv in conversations
        ]
    }
