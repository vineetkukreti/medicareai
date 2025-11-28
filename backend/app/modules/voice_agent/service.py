from sqlalchemy.orm import Session
from app.modules.voice_agent import models, schemas
import uuid

class VoiceAgentService:
    def create_session(self, db: Session, user_id: int = None):
        session_id = str(uuid.uuid4())
        session = models.VoiceSession(session_id=session_id, user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def get_session(self, db: Session, session_id: str):
        return db.query(models.VoiceSession).filter(models.VoiceSession.session_id == session_id).first()

    def update_session_state(self, db: Session, session_id: str, state: str, data: str = None):
        session = self.get_session(db, session_id)
        if session:
            session.conversation_state = state
            if data:
                session.collected_data = data
            db.commit()
            db.refresh(session)
        return session

voice_agent_service = VoiceAgentService()
