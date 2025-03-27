import os
import sys
from datetime import datetime, timedelta
import random

# Garantir que estamos no diretório correto para importações relativas
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.task import Task, TaskCategory
from app.models.notification import Notification
from app.models.meal import FoodItem, Meal, MealItem

def create_admin():
    """Criar um usuário admin para teste"""
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado com sucesso.')
    else:
        print('Usuário admin já existe.')
    
    return admin

def create_categories(user_id):
    """Criar categorias padrão para tarefas"""
    categories = [
        {'name': 'Trabalho', 'color': '#007bff'},
        {'name': 'Estudo', 'color': '#28a745'},
        {'name': 'Pessoal', 'color': '#dc3545'},
        {'name': 'Saúde', 'color': '#17a2b8'},
        {'name': 'Finanças', 'color': '#ffc107'}
    ]
    
    created_categories = []
    
    for category_data in categories:
        existing = TaskCategory.query.filter_by(
            name=category_data['name'], 
            user_id=user_id
        ).first()
        
        if not existing:
            category = TaskCategory(
                name=category_data['name'],
                color=category_data['color'],
                user_id=user_id
            )
            db.session.add(category)
            created_categories.append(category)
    
    if created_categories:
        db.session.commit()
        print(f'Criadas {len(created_categories)} categorias para o usuário.')
    else:
        print('Todas as categorias já existem.')
    
    return TaskCategory.query.filter_by(user_id=user_id).all()

def create_tasks(user_id, categories):
    """Criar tarefas de exemplo"""
    today = datetime.now()
    
    example_tasks = [
        {
            'title': 'Reunião semanal',
            'description': 'Reunião de acompanhamento de projeto',
            'due_date': today + timedelta(days=1, hours=10),
            'priority': 1,
            'category': 'Trabalho',
            'recurrence': 'weekly'
        },
        {
            'title': 'Preparar apresentação',
            'description': 'Slides para apresentação de resultados trimestrais',
            'due_date': today + timedelta(days=3, hours=14),
            'priority': 2,
            'category': 'Trabalho',
            'recurrence': None
        },
        {
            'title': 'Estudar Python avançado',
            'description': 'Tópicos: decoradores, metaclasses e concorrência',
            'due_date': today + timedelta(days=2, hours=18),
            'priority': 2,
            'category': 'Estudo',
            'recurrence': 'daily'
        },
        {
            'title': 'Academia',
            'description': 'Treino de força e cardio',
            'due_date': today + timedelta(hours=4),
            'priority': 3,
            'category': 'Saúde',
            'recurrence': 'daily'
        },
        {
            'title': 'Planejar orçamento mensal',
            'description': 'Revisar despesas e planejar investimentos',
            'due_date': today + timedelta(days=5, hours=10),
            'priority': 2,
            'category': 'Finanças',
            'recurrence': 'monthly'
        }
    ]
    
    # Mapear nomes de categorias para objetos de categoria
    category_map = {category.name: category for category in categories}
    
    tasks_created = 0
    
    for task_data in example_tasks:
        # Verificar se a tarefa já existe
        existing = Task.query.filter_by(
            title=task_data['title'],
            user_id=user_id
        ).first()
        
        if not existing:
            category = category_map.get(task_data['category'])
            category_id = category.id if category else None
            
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                due_date=task_data['due_date'],
                priority=task_data['priority'],
                recurrence=task_data['recurrence'],
                user_id=user_id,
                category_id=category_id
            )
            
            db.session.add(task)
            db.session.flush()  # Para obter o ID da tarefa
            
            # Criar notificação para a tarefa
            notification = Notification(
                title=f"Lembrete: {task_data['title']}",
                message=f"Sua tarefa '{task_data['title']}' está agendada para breve.",
                scheduled_for=task_data['due_date'] - timedelta(hours=1),
                user_id=user_id,
                task_id=task.id  # Usar o ID real da tarefa
            )
            
            db.session.add(notification)
            tasks_created += 1
    
    if tasks_created > 0:
        db.session.commit()
        print(f'Criadas {tasks_created} tarefas de exemplo.')
    else:
        print('Todas as tarefas de exemplo já existem.')

def create_food_items():
    """Criar alimentos padrão para o sistema"""
    common_foods = [
        {
            'name': 'Arroz branco cozido',
            'calories': 130,
            'protein': 2.7,
            'carbs': 28.2,
            'fat': 0.3,
            'fiber': 0.4
        },
        {
            'name': 'Feijão preto cozido',
            'calories': 132,
            'protein': 8.7,
            'carbs': 23.7,
            'fat': 0.5,
            'fiber': 8.7
        },
        {
            'name': 'Peito de frango grelhado',
            'calories': 165,
            'protein': 31,
            'carbs': 0,
            'fat': 3.6,
            'fiber': 0
        },
        {
            'name': 'Ovo cozido',
            'calories': 78,
            'protein': 6.3,
            'carbs': 0.6,
            'fat': 5.3,
            'fiber': 0
        },
        {
            'name': 'Maçã',
            'calories': 52,
            'protein': 0.3,
            'carbs': 14,
            'fat': 0.2,
            'fiber': 2.4
        },
        {
            'name': 'Banana',
            'calories': 89,
            'protein': 1.1,
            'carbs': 22.8,
            'fat': 0.3,
            'fiber': 2.6
        },
        {
            'name': 'Pão integral',
            'calories': 81,
            'protein': 4,
            'carbs': 13.8,
            'fat': 1.1,
            'fiber': 2.0
        },
        {
            'name': 'Leite desnatado',
            'calories': 83,
            'protein': 8.2,
            'carbs': 12.2,
            'fat': 0.2,
            'fiber': 0
        },
        {
            'name': 'Queijo branco',
            'calories': 98,
            'protein': 14,
            'carbs': 3.1,
            'fat': 4.3,
            'fiber': 0
        },
        {
            'name': 'Brócolis cozido',
            'calories': 55,
            'protein': 3.7,
            'carbs': 11.2,
            'fat': 0.6,
            'fiber': 5.1
        }
    ]
    
    foods_created = 0
    
    for food_data in common_foods:
        existing = FoodItem.query.filter_by(name=food_data['name']).first()
        
        if not existing:
            food = FoodItem(
                name=food_data['name'],
                calories=food_data['calories'],
                protein=food_data['protein'],
                carbs=food_data['carbs'],
                fat=food_data['fat'],
                fiber=food_data['fiber']
            )
            
            db.session.add(food)
            foods_created += 1
    
    if foods_created > 0:
        db.session.commit()
        print(f'Criados {foods_created} alimentos padrão.')
    else:
        print('Todos os alimentos padrão já existem.')
    
    return FoodItem.query.all()

def create_example_meals(user_id, food_items):
    """Criar refeições de exemplo para o usuário"""
    today = datetime.now().date()
    
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    meal_times = {
        'breakfast': '08:00',
        'lunch': '12:30',
        'dinner': '19:00',
        'snack': '16:00'
    }
    
    # Verificar se já existem refeições para hoje
    existing_meal = Meal.query.filter_by(
        user_id=user_id,
        date=today
    ).first()
    
    if existing_meal:
        print('Já existem refeições registradas para hoje.')
        return
    
    meals_created = 0
    
    for meal_type in meal_types:
        time_parts = meal_times[meal_type].split(':')
        meal_time = datetime.now().replace(
            hour=int(time_parts[0]), 
            minute=int(time_parts[1]), 
            second=0, 
            microsecond=0
        ).time()
        
        meal = Meal(
            meal_type=meal_type,
            date=today,
            time=meal_time,
            notes=f'Exemplo de {meal_type}',
            user_id=user_id
        )
        
        db.session.add(meal)
        db.session.flush()  # Para obter o ID da refeição
        
        # Adicionar alimentos à refeição
        # Número aleatório de itens (1-3)
        num_items = random.randint(1, 3)
        selected_foods = random.sample(food_items, num_items)
        
        for food in selected_foods:
            quantity = round(random.uniform(0.5, 2.0), 1)  # Quantidade aleatória entre 0.5 e 2.0
            
            meal_item = MealItem(
                meal_id=meal.id,
                food_item_id=food.id,
                quantity=quantity,
                unit='porção'
            )
            
            # Calcular valores nutricionais
            meal_item.calories = food.calories * quantity
            meal_item.protein = food.protein * quantity
            meal_item.carbs = food.carbs * quantity
            meal_item.fat = food.fat * quantity
            
            db.session.add(meal_item)
        
        meals_created += 1
    
    db.session.commit()
    print(f'Criadas {meals_created} refeições de exemplo para hoje.')

def init_db():
    """Inicializar o banco de dados com dados de exemplo"""
    app = create_app('development')
    
    with app.app_context():
        # Criar tabelas
        db.create_all()
        print('Tabelas do banco de dados criadas.')
        
        # Criar usuário admin
        admin = create_admin()
        
        # Criar categorias
        categories = create_categories(admin.id)
        
        # Criar tarefas
        create_tasks(admin.id, categories)
        
        # Criar alimentos
        food_items = create_food_items()
        
        # Criar refeições
        create_example_meals(admin.id, food_items)
        
        print('Inicialização do banco de dados concluída com sucesso!')

if __name__ == '__main__':
    init_db()