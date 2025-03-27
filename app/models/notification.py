from datetime import datetime
from app.models import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    delivered = db.Column(db.Boolean, default=False)
    delivered_at = db.Column(db.DateTime)
    read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    # Relacionamentos
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    
    def mark_delivered(self):
        self.delivered = True
        self.delivered_at = datetime.utcnow()
    
    def mark_read(self):
        self.read = True
        self.read_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Notification {self.title}>'