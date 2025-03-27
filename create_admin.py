from app import create_app
from app.models import db
from app.models.user import User

app = create_app()

with app.app_context():
    # Verificar se o admin já existe
    admin = User.query.filter_by(email='admin@example.com').first()
    
    if not admin:
        # Criar usuário admin (modificado para incluir o password)
        admin = User(
            username='admin',
            email='admin@example.com',
            password='adminpassword'  # Adicionado password como argumento
        )
        
        db.session.add(admin)
        db.session.commit()
        print("Usuário administrador criado com sucesso!")
    else:
        # Atualizar senha do admin existente se ele já existe
        admin.set_password('adminpassword')
        db.session.commit()
        print("Senha do administrador atualizada com sucesso!")