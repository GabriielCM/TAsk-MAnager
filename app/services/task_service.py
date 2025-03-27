from datetime import datetime, timedelta
from app.models import db
from app.models.task import Task, TaskCategory
from app.models.notification import Notification

class TaskService:
    @staticmethod
    def create_task(user_id, title, description, due_date, priority=2, category_id=None, recurrence=None):
        """
        Cria uma nova tarefa e notificações associadas
        """
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            recurrence=recurrence,
            user_id=user_id,
            category_id=category_id
        )
        
        db.session.add(task)
        db.session.flush()  # Para obter o ID da tarefa antes do commit
        
        # Criar notificação para a tarefa
        notification_time = due_date - timedelta(hours=1)
        notification = Notification(
            title=f"Lembrete: {title}",
            message=f"Sua tarefa '{title}' vence em uma hora.",
            scheduled_for=notification_time,
            user_id=user_id,
            task_id=task.id
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return task
    
    @staticmethod
    def update_task(task_id, user_id, **kwargs):
        """
        Atualiza uma tarefa existente
        """
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return None
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        db.session.commit()
        return task
    
    @staticmethod
    def delete_task(task_id, user_id):
        """
        Exclui uma tarefa
        """
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return False
        
        db.session.delete(task)
        db.session.commit()
        return True
    
    @staticmethod
    def get_tasks_by_user(user_id, completed=None, priority=None, category_id=None, date_from=None, date_to=None):
        """
        Obtém tarefas de um usuário com filtros opcionais
        """
        query = Task.query.filter_by(user_id=user_id)
        
        if completed is not None:
            query = query.filter_by(completed=completed)
        
        if priority is not None:
            query = query.filter_by(priority=priority)
        
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        
        if date_from is not None:
            query = query.filter(Task.due_date >= date_from)
        
        if date_to is not None:
            query = query.filter(Task.due_date <= date_to)
        
        return query.order_by(Task.due_date).all()
    
    @staticmethod
    def mark_task_completed(task_id, user_id):
        """
        Marca uma tarefa como concluída
        """
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return None
        
        task.mark_completed()
        db.session.commit()
        return task
    
    @staticmethod
    def get_upcoming_tasks(user_id, days=7):
        """
        Obtém tarefas próximas do prazo
        """
        now = datetime.utcnow()
        end_date = now + timedelta(days=days)
        
        return Task.query.filter_by(
            user_id=user_id, 
            completed=False
        ).filter(
            Task.due_date >= now, 
            Task.due_date <= end_date
        ).order_by(Task.due_date).all()
    
    @staticmethod
    def create_category(user_id, name, color='#007bff'):
        """
        Cria uma nova categoria de tarefa
        """
        category = TaskCategory(name=name, color=color, user_id=user_id)
        db.session.add(category)
        db.session.commit()
        return category
    
    @staticmethod
    def get_categories_by_user(user_id):
        """
        Obtém todas as categorias de um usuário
        """
        return TaskCategory.query.filter_by(user_id=user_id).all()