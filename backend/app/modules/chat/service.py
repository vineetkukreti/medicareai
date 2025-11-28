from sqlalchemy.orm import Session
from app.modules.chat import models
from app.services.ai_service import ai_service

class ChatService:
    def get_conversation_history(self, db: Session, session_id: str, limit: int = 5) -> str:
        try:
            conversations = db.query(models.ChatConversation).filter(
                models.ChatConversation.session_id == session_id
            ).order_by(models.ChatConversation.created_at.desc()).limit(limit).all()
            
            # Reverse to get chronological order
            conversations.reverse()
            
            context_str = ""
            for conv in conversations:
                context_str += f"User: {conv.user_message}\nAssistant: {conv.bot_response}\n\n"
            
            return context_str
        except Exception as e:
            print(f"Error getting history: {e}")
            return ""

    def save_conversation(self, db: Session, session_id: str, user_message: str, bot_response: str):
        conversation = models.ChatConversation(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response
        )
        db.add(conversation)
        db.commit()
        return conversation

    async def get_ai_response(self, message: str, context: str):
        return await ai_service.chat(message, context=context)

    async def get_ai_response_stream(self, message: str, context: str):
        async for chunk in ai_service.chat_stream(message, context=context):
            yield chunk

    def get_chat_history_for_session(self, db: Session, session_id: str):
        return db.query(models.ChatConversation).filter(
            models.ChatConversation.session_id == session_id
        ).order_by(models.ChatConversation.created_at).all()

chat_service = ChatService()
