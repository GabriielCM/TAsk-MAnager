import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # Adicionado import do JWTManager
from app.config import config
from app.models import db, migrate

# Inicialização de extensões
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
jwt = JWTManager()  # Inicialização do JWTManager

def create_app(config_name=None):
    """
    Função Factory para criar a aplicação Flask
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configuração do JWT
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 horas (opcional)
    
    # Inicializar extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)  # Inicialização do JWT com a aplicação
    CORS(app)
    
    # Registrar blueprints
    from app.api.auth import auth_bp
    from app.api.tasks import tasks_bp
    from app.api.insights import insights_bp
    from app.api.meals import meals_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(insights_bp, url_prefix='/api/insights')
    app.register_blueprint(meals_bp, url_prefix='/api/meals')
    
    # Registrar rotas da interface web
    from app.views.auth import auth as auth_views
    from app.views.dashboard import dashboard as dashboard_views
    from app.views.tasks import tasks as tasks_views
    from app.views.meals import meals as meals_views
    
    app.register_blueprint(auth_views, url_prefix='/auth')
    app.register_blueprint(dashboard_views, url_prefix='/dashboard')
    app.register_blueprint(tasks_views, url_prefix='/tasks')
    app.register_blueprint(meals_views, url_prefix='/meals')
    
    # Adicionar rota raiz
    @app.route('/')
    def index():
        return redirect(url_for('dashboard_views.index'))
    
    # Configurar o carregador de usuários para o Flask-Login
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Adicionar shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db, User=User)
    
    return app