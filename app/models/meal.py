from datetime import datetime
from app.models import db

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    fiber = db.Column(db.Float)
    
    # Relacionamento com MealItem
    meal_items = db.relationship('MealItem', backref='food', lazy='dynamic')
    
    def __repr__(self):
        return f'<FoodItem {self.name}>'

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_type = db.Column(db.String(20), nullable=False)  # 'breakfast', 'lunch', 'dinner', 'snack'
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('MealItem', backref='meal', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def total_calories(self):
        return sum(item.calories for item in self.items)
    
    @property
    def total_protein(self):
        return sum(item.protein for item in self.items)
    
    @property
    def total_carbs(self):
        return sum(item.carbs for item in self.items)
    
    @property
    def total_fat(self):
        return sum(item.fat for item in self.items)
    
    def __repr__(self):
        return f'<Meal {self.meal_type} on {self.date}>'

class MealItem(db.Model):
    __tablename__ = 'meal_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit = db.Column(db.String(20), default='serving')
    
    # Campos calculados
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    
    # Relacionamentos
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    
    def calculate_nutrition(self):
        if self.food:
            self.calories = self.food.calories * self.quantity
            self.protein = self.food.protein * self.quantity
            self.carbs = self.food.carbs * self.quantity
            self.fat = self.food.fat * self.quantity
    
    def __repr__(self):
        return f'<MealItem {self.quantity} {self.unit} of {self.food_item_id}>'