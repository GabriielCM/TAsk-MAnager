from datetime import datetime
from app.models import db
from app.models.notification import Notification

class NotificationService:
    @staticmethod
    def create_notification(user_id, title, message, scheduled_for, task_id=None):
        """
        Cria uma nova notificação
        """
        notification = Notification(
            title=title,
            message=message,
            scheduled_for=scheduled_for,
            user_id=user_id,
            task_id=task_id
        )
        
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def get_pending_notifications(user_id):
        """
        Obtém notificações pendentes de um usuário
        """
        now = datetime.utcnow()
        return Notification.query.filter_by(
            user_id=user_id,
            delivered=False
        ).filter(
            Notification.scheduled_for <= now
        ).order_by(Notification.scheduled_for).all()
    
    @staticmethod
    def mark_notification_delivered(notification_id):
        """
        Marca uma notificação como entregue
        """
        notification = Notification.query.get(notification_id)
        if notification:
            notification.mark_delivered()
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def mark_notification_read(notification_id):
        """
        Marca uma notificação como lida
        """
        notification = Notification.query.get(notification_id)
        if notification:
            notification.mark_read()
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_unread_notifications(user_id):
        """
        Obtém notificações não lidas de um usuário
        """
        return Notification.query.filter_by(
            user_id=user_id,
            delivered=True,
            read=False
        ).order_by(Notification.delivered_at.desc()).all()
    
    @staticmethod
    def get_recent_notifications(user_id, limit=10):
        """
        Obtém notificações recentes de um usuário
        """
        return Notification.query.filter_by(
            user_id=user_id,
            delivered=True
        ).order_by(Notification.delivered_at.desc()).limit(limit).all()