from datetime import datetime
from app.models import db

class TaskCategory(db.Model):
    __tablename__ = 'task_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    color = db.Column(db.String(7), default='#007bff')  # Formato de cor hexadecimal
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamentos
    tasks = db.relationship('Task', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<TaskCategory {self.name}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    # Prioridade (1: alta, 2: média, 3: baixa)
    priority = db.Column(db.Integer, default=2)
    
    # Recorrência (diária, semanal, mensal, anual, etc.)
    recurrence = db.Column(db.String(20))
    
    # Relacionamentos
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('task_categories.id'))
    notifications = db.relationship('Notification', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    insights = db.relationship('TaskInsight', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    
    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Task {self.title}>'

class TaskInsight(db.Model):
    __tablename__ = 'task_insights'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    insight_type = db.Column(db.String(20), nullable=False)  # 'suggestion', 'risk', etc.
    
    # URLs para materiais relacionados
    related_urls = db.Column(db.Text)
    
    # Relacionamentos
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    
    def __repr__(self):
        return f'<TaskInsight for Task {self.task_id}>'