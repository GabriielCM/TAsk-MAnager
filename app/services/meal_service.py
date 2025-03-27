from datetime import datetime
from app.models import db
from app.models.meal import Meal, MealItem, FoodItem

class MealService:
    @staticmethod
    def create_meal(user_id, meal_type, date=None, time=None, notes=None):
        """
        Cria uma nova refeição
        """
        if date is None:
            date = datetime.utcnow().date()
        
        if time is None:
            time = datetime.utcnow().time()
        
        meal = Meal(
            user_id=user_id,
            meal_type=meal_type,
            date=date,
            time=time,
            notes=notes
        )
        
        db.session.add(meal)
        db.session.commit()
        return meal
    
    @staticmethod
    def add_food_to_meal(meal_id, food_item_id, quantity=1.0, unit='serving'):
        """
        Adiciona um item alimentar a uma refeição
        """
        food_item = FoodItem.query.get(food_item_id)
        if not food_item:
            return None
        
        meal_item = MealItem(
            meal_id=meal_id,
            food_item_id=food_item_id,
            quantity=quantity,
            unit=unit
        )
        
        # Calcular os valores nutricionais
        meal_item.calories = food_item.calories * quantity
        meal_item.protein = food_item.protein * quantity
        meal_item.carbs = food_item.carbs * quantity
        meal_item.fat = food_item.fat * quantity
        
        db.session.add(meal_item)
        db.session.commit()
        return meal_item
    
    @staticmethod
    def get_meals_by_date_range(user_id, start_date, end_date):
        """
        Obtém refeições de um usuário em um intervalo de datas
        """
        return Meal.query.filter_by(
            user_id=user_id
        ).filter(
            Meal.date >= start_date,
            Meal.date <= end_date
        ).order_by(Meal.date, Meal.time).all()
    
    @staticmethod
    def get_meals_by_date(user_id, date):
        """
        Obtém refeições de um usuário em uma data específica
        """
        return Meal.query.filter_by(
            user_id=user_id,
            date=date
        ).order_by(Meal.time).all()
    
    @staticmethod
    def create_food_item(name, calories=0, protein=0, carbs=0, fat=0, fiber=0):
        """
        Cria um novo item alimentar
        """
        food_item = FoodItem(
            name=name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            fiber=fiber
        )
        
        db.session.add(food_item)
        db.session.commit()
        return food_item
    
    @staticmethod
    def search_food_items(query, limit=10):
        """
        Pesquisa itens alimentares por nome
        """
        return FoodItem.query.filter(
            FoodItem.name.ilike(f'%{query}%')
        ).limit(limit).all()
    
    @staticmethod
    def get_nutrition_summary(user_id, date):
        """
        Obtém um resumo nutricional para uma data específica
        """
        meals = Meal.query.filter_by(
            user_id=user_id,
            date=date
        ).all()
        
        summary = {
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fat': 0,
            'meals': []
        }
        
        for meal in meals:
            meal_data = {
                'meal_type': meal.meal_type,
                'calories': meal.total_calories,
                'protein': meal.total_protein,
                'carbs': meal.total_carbs,
                'fat': meal.total_fat
            }
            
            summary['meals'].append(meal_data)
            summary['total_calories'] += meal.total_calories
            summary['total_protein'] += meal.total_protein
            summary['total_carbs'] += meal.total_carbs
            summary['total_fat'] += meal.total_fat
        
        return summary