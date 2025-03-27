from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, timedelta
from app.services.meal_service import MealService

meals_bp = Blueprint('meals', __name__)

@meals_bp.route('/', methods=['GET'])
@jwt_required()
def get_meals():
    """
    Obter refeições do usuário por data ou intervalo de datas
    """
    user_id = get_jwt_identity()
    
    date_str = request.args.get('date')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Obter uma data específica
    if date_str:
        try:
            meal_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            meals = MealService.get_meals_by_date(user_id, meal_date)
        except ValueError:
            return jsonify({'message': 'Formato de data inválido', 'status': 'error'}), 400
    
    # Obter um intervalo de datas
    elif start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            meals = MealService.get_meals_by_date_range(user_id, start_date, end_date)
        except ValueError:
            return jsonify({'message': 'Formato de data inválido', 'status': 'error'}), 400
    
    # Padrão: obter refeições do dia atual
    else:
        meal_date = date.today()
        meals = MealService.get_meals_by_date(user_id, meal_date)
    
    # Formatar a resposta
    meals_data = []
    for meal in meals:
        items = []
        for item in meal.items:
            items.append({
                'id': item.id,
                'food_id': item.food_item_id,
                'food_name': item.food.name if item.food else 'Unknown',
                'quantity': item.quantity,
                'unit': item.unit,
                'calories': item.calories,
                'protein': item.protein,
                'carbs': item.carbs,
                'fat': item.fat
            })
        
        meals_data.append({
            'id': meal.id,
            'meal_type': meal.meal_type,
            'date': meal.date.isoformat(),
            'time': meal.time.isoformat(),
            'notes': meal.notes,
            'total_calories': meal.total_calories,
            'total_protein': meal.total_protein,
            'total_carbs': meal.total_carbs,
            'total_fat': meal.total_fat,
            'items': items
        })
    
    return jsonify({
        'status': 'success',
        'meals': meals_data
    }), 200

@meals_bp.route('/', methods=['POST'])
@jwt_required()
def create_meal():
    """
    Criar uma nova refeição
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar dados obrigatórios
    if 'meal_type' not in data:
        return jsonify({'message': 'Tipo de refeição é obrigatório', 'status': 'error'}), 400
    
    # Processar data e hora, se fornecidos
    meal_date = None
    meal_time = None
    
    if 'date' in data:
        try:
            meal_date = datetime.fromisoformat(data['date']).date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido', 'status': 'error'}), 400
    
    if 'time' in data:
        try:
            meal_time = datetime.fromisoformat(data['time']).time()
        except ValueError:
            return jsonify({'message': 'Formato de hora inválido', 'status': 'error'}), 400
    
    # Criar a refeição
    meal = MealService.create_meal(
        user_id=user_id,
        meal_type=data['meal_type'],
        date=meal_date,
        time=meal_time,
        notes=data.get('notes')
    )
    
    # Adicionar itens alimentares, se fornecidos
    if 'items' in data and isinstance(data['items'], list):
        for item_data in data['items']:
            MealService.add_food_to_meal(
                meal_id=meal.id,
                food_item_id=item_data['food_id'],
                quantity=item_data.get('quantity', 1.0),
                unit=item_data.get('unit', 'serving')
            )
    
    return jsonify({
        'message': 'Refeição criada com sucesso',
        'status': 'success',
        'meal': {
            'id': meal.id,
            'meal_type': meal.meal_type,
            'date': meal.date.isoformat(),
            'time': meal.time.isoformat(),
            'notes': meal.notes
        }
    }), 201

@meals_bp.route('/<int:meal_id>/items', methods=['POST'])
@jwt_required()
def add_meal_item(meal_id):
    """
    Adicionar um item a uma refeição existente
    """
    data = request.get_json()
    
    # Validar dados obrigatórios
    if 'food_id' not in data:
        return jsonify({'message': 'ID do alimento é obrigatório', 'status': 'error'}), 400
    
    # Adicionar o item à refeição
    meal_item = MealService.add_food_to_meal(
        meal_id=meal_id,
        food_item_id=data['food_id'],
        quantity=data.get('quantity', 1.0),
        unit=data.get('unit', 'serving')
    )
    
    if not meal_item:
        return jsonify({'message': 'Alimento não encontrado', 'status': 'error'}), 404
    
    return jsonify({
        'message': 'Item adicionado com sucesso',
        'status': 'success',
        'meal_item': {
            'id': meal_item.id,
            'food_id': meal_item.food_item_id,
            'food_name': meal_item.food.name if meal_item.food else 'Unknown',
            'quantity': meal_item.quantity,
            'unit': meal_item.unit,
            'calories': meal_item.calories,
            'protein': meal_item.protein,
            'carbs': meal_item.carbs,
            'fat': meal_item.fat
        }
    }), 201

@meals_bp.route('/food-items', methods=['GET'])
@jwt_required()
def search_food_items():
    """
    Pesquisar itens alimentares
    """
    query = request.args.get('query', '')
    
    food_items = MealService.search_food_items(query)
    
    food_items_data = [{
        'id': item.id,
        'name': item.name,
        'calories': item.calories,
        'protein': item.protein,
        'carbs': item.carbs,
        'fat': item.fat,
        'fiber': item.fiber
    } for item in food_items]
    
    return jsonify({
        'status': 'success',
        'food_items': food_items_data
    }), 200

@meals_bp.route('/food-items', methods=['POST'])
@jwt_required()
def create_food_item():
    """
    Criar um novo item alimentar
    """
    data = request.get_json()
    
    # Validar dados obrigatórios
    if 'name' not in data:
        return jsonify({'message': 'Nome do alimento é obrigatório', 'status': 'error'}), 400
    
    # Criar o item alimentar
    food_item = MealService.create_food_item(
        name=data['name'],
        calories=data.get('calories', 0),
        protein=data.get('protein', 0),
        carbs=data.get('carbs', 0),
        fat=data.get('fat', 0),
        fiber=data.get('fiber', 0)
    )
    
    return jsonify({
        'message': 'Item alimentar criado com sucesso',
        'status': 'success',
        'food_item': {
            'id': food_item.id,
            'name': food_item.name,
            'calories': food_item.calories,
            'protein': food_item.protein,
            'carbs': food_item.carbs,
            'fat': food_item.fat,
            'fiber': food_item.fiber
        }
    }), 201

@meals_bp.route('/nutrition-summary', methods=['GET'])
@jwt_required()
def get_nutrition_summary():
    """
    Obter resumo nutricional para uma data específica
    """
    user_id = get_jwt_identity()
    
    date_str = request.args.get('date')
    
    if date_str:
        try:
            summary_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido', 'status': 'error'}), 400
    else:
        summary_date = date.today()
    
    summary = MealService.get_nutrition_summary(user_id, summary_date)
    
    return jsonify({
        'status': 'success',
        'date': summary_date.isoformat(),
        'summary': summary
    }), 200