from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.services.task_service import TaskService
from app.services.gpt_service import GPTService

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Obter todas as tarefas do usuário com filtros opcionais
    """
    user_id = get_jwt_identity()
    
    # Parâmetros de filtro opcionais
    completed = request.args.get('completed')
    priority = request.args.get('priority')
    category_id = request.args.get('category_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Converter tipos
    if completed is not None:
        completed = completed.lower() == 'true'
    
    if priority is not None:
        priority = int(priority)
    
    if category_id is not None:
        category_id = int(category_id)
    
    if date_from is not None:
        date_from = datetime.fromisoformat(date_from)
    
    if date_to is not None:
        date_to = datetime.fromisoformat(date_to)
    
    # Obter tarefas com filtros
    tasks = TaskService.get_tasks_by_user(
        user_id, 
        completed=completed, 
        priority=priority, 
        category_id=category_id,
        date_from=date_from,
        date_to=date_to
    )
    
    # Formatar a resposta
    tasks_data = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat(),
        'completed': task.completed,
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'priority': task.priority,
        'recurrence': task.recurrence,
        'category_id': task.category_id
    } for task in tasks]
    
    return jsonify({
        'status': 'success',
        'tasks': tasks_data
    }), 200

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """
    Criar uma nova tarefa
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar dados obrigatórios
    if not all(k in data for k in ('title', 'due_date')):
        return jsonify({'message': 'Campos obrigatórios ausentes', 'status': 'error'}), 400
    
    # Converter a data de vencimento
    try:
        due_date = datetime.fromisoformat(data['due_date'])
    except ValueError:
        return jsonify({'message': 'Formato de data inválido', 'status': 'error'}), 400
    
    # Criar a tarefa
    task = TaskService.create_task(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', ''),
        due_date=due_date,
        priority=data.get('priority', 2),
        category_id=data.get('category_id'),
        recurrence=data.get('recurrence')
    )
    
    # Gerar insights para a tarefa (assíncrono em produção)
    insights = GPTService.generate_task_insights(task)
    
    return jsonify({
        'message': 'Tarefa criada com sucesso',
        'status': 'success',
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat(),
            'completed': task.completed,
            'priority': task.priority,
            'category_id': task.category_id,
            'recurrence': task.recurrence
        },
        'insights': insights
    }), 201

# Implementação mínima para rotas básicas
# Na versão completa teríamos todas as operações CRUD

@tasks_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Obter todas as categorias do usuário
    """
    user_id = get_jwt_identity()
    
    categories = TaskService.get_categories_by_user(user_id)
    
    categories_data = [{
        'id': category.id,
        'name': category.name,
        'color': category.color
    } for category in categories]
    
    return jsonify({
        'status': 'success',
        'categories': categories_data
    }), 200