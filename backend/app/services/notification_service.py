import asyncio
from typing import Dict
from collections import defaultdict
import json
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        # Store queues for each doctor: {doctor_id: [queue1, queue2, ...]}
        self.connections: Dict[int, list] = defaultdict(list)
    
    async def subscribe(self, doctor_id: int):
        """
        Subscribe a doctor to receive notifications via SSE.
        Yields notification events as they arrive.
        """
        queue = asyncio.Queue()
        self.connections[doctor_id].append(queue)
        
        try:
            logger.info(f"📡 Doctor {doctor_id} subscribed to notifications")
            
            # Send initial connection message
            yield {
                "event": "connected",
                "data": json.dumps({"message": "Connected to notification stream"})
            }
            
            # Keep connection alive and send notifications
            while True:
                try:
                    # Wait for notification with timeout for heartbeat
                    notification = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield notification
                except asyncio.TimeoutError:
                    # Send heartbeat to keep connection alive
                    yield {
                        "event": "heartbeat",
                        "data": json.dumps({"timestamp": asyncio.get_event_loop().time()})
                    }
        except asyncio.CancelledError:
            logger.info(f"📡 Doctor {doctor_id} unsubscribed from notifications")
        finally:
            # Clean up connection
            if queue in self.connections[doctor_id]:
                self.connections[doctor_id].remove(queue)
            if not self.connections[doctor_id]:
                del self.connections[doctor_id]
    
    async def send_notification(self, doctor_id: int, event_type: str, data: dict):
        """
        Send a notification to a specific doctor.
        """
        if doctor_id not in self.connections:
            logger.debug(f"📡 No active connections for doctor {doctor_id}")
            return
        
        notification = {
            "event": event_type,
            "data": json.dumps(data)
        }
        
        # Send to all active connections for this doctor
        for queue in self.connections[doctor_id]:
            try:
                await queue.put(notification)
                logger.info(f"📡 Sent {event_type} notification to doctor {doctor_id}")
            except Exception as e:
                logger.error(f"📡 Error sending notification to doctor {doctor_id}: {e}")

# Global instance
notification_service = NotificationService()
