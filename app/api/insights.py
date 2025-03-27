from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.gpt_service import GPTService
from app.models.task import Task

insights_bp = Blueprint('insights', __name__)

@insights_bp.route('/task/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task_insights(task_id):
    """
    Obter insights para uma tarefa específica
    """
    user_id = get_jwt_identity()
    
    # Verificar se a tarefa pertence ao usuário
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Tarefa não encontrada', 'status': 'error'}), 404
    
    # Obter insights existentes
    insights = GPTService.get_insights_by_task(task_id)
    
    # Formatar a resposta
    insights_data = [{
        'id': insight.id,
        'content': insight.content,
        'insight_type': insight.insight_type,
        'related_urls': insight.related_urls,
        'created_at': insight.created_at.isoformat()
    } for insight in insights]
    
    return jsonify({
        'status': 'success',
        'task_id': task_id,
        'insights': insights_data
    }), 200

@insights_bp.route('/task/<int:task_id>/generate', methods=['POST'])
@jwt_required()
def generate_task_insights(task_id):
    """
    Gerar novos insights para uma tarefa
    """
    user_id = get_jwt_identity()
    
    # Verificar se a tarefa pertence ao usuário
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Tarefa não encontrada', 'status': 'error'}), 404
    
    # Gerar novos insights
    insights = GPTService.generate_task_insights(task)
    
    if 'error' in insights:
        return jsonify({
            'status': 'error',
            'message': insights['error']
        }), 500
    
    return jsonify({
        'status': 'success',
        'message': 'Insights gerados com sucesso',
        'task_id': task_id,
        'insights': insights
    }), 200