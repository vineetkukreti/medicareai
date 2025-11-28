from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.modules.chat import schemas
from app.modules.chat.service import chat_service
import uuid

router = APIRouter()

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat_with_bot(chat_message: schemas.ChatMessage, db: Session = Depends(get_db)):
    """
    Chat with the medical AI assistant
    """
    # Generate session ID if not provided
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Get conversation history
    history = chat_service.get_conversation_history(db, session_id)
    
    # Get AI response with context
    bot_response = await chat_service.get_ai_response(chat_message.message, context=history)
    
    # Save conversation to database
    chat_service.save_conversation(db, session_id, chat_message.message, bot_response)
    
    return schemas.ChatResponse(
        response=bot_response,
        session_id=session_id
    )

@router.post("/chat/stream")
async def chat_stream(chat_message: schemas.ChatMessage):
    """
    Stream chat response from the medical AI assistant
    """
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Get conversation history
    # We need a DB session here since this is an async generator endpoint
    try:
        db = SessionLocal()
        history = chat_service.get_conversation_history(db, session_id)
        db.close()
    except Exception as e:
        print(f"Error fetching history: {e}")
        history = ""
    
    async def generate():
        full_response = ""
        try:
            async for chunk in chat_service.get_ai_response_stream(chat_message.message, context=history):
                full_response += chunk
                yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"
        
        # Save to database after streaming is complete
        try:
            db = SessionLocal()
            chat_service.save_conversation(db, session_id, chat_message.message, full_response)
            db.close()
        except Exception as e:
            print(f"Error saving chat to DB: {e}")

    return StreamingResponse(generate(), media_type="text/plain")

@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Get chat history for a specific session
    """
    conversations = chat_service.get_chat_history_for_session(db, session_id)
    
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
