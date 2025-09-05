import click
from flask.cli import with_appcontext
from getpass import getpass
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, csrf, migrate
from routes import main
from routes import auth_bp, admin_bp
from models import User, UserRole 

def create_app():
    """Factory function para crear y configurar la instancia de la aplicación Flask."""
    app = Flask(__name__)

    # Cargar configuración desde la clase Config (config.py)
    app.config.from_object(Config)
    
    # Asegurarse de que la carpeta de subidas existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configurar user_loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Callback para recargar el objeto usuario desde el ID guardado en la sesión."""
        return User.query.get(int(user_id))

    # Registrar blueprints (rutas)
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Manejadores de errores personalizados
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback() 
        return render_template('errors/500.html'), 500

    return app




@click.command(name='create-admin')
@with_appcontext
def create_admin_command():
    """Crea el usuario administrador inicial de forma interactiva."""
    print("--- Creando Cuenta de Administrador ---")
    username = input("Nombre de usuario del admin: ")
    email = input("Email del admin: ")
    password = getpass("Contraseña del admin: ")
    confirm_password = getpass("Confirma la contraseña: ")

    if password != confirm_password:
        print("Error: Las contraseñas no coinciden.")
        return

    if User.query.filter((User.username == username) | (User.email == email)).first():
        print("Error: El usuario o email ya existe.")
        return
    
    try:
        admin = User(username=username, email=email.lower(), role=UserRole.admin)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        print(f"¡Administrador '{username}' creado exitosamente!")
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear el administrador: {e}")

app = create_app()
app.cli.add_command(create_admin_command)

if __name__ == '__main__':
    app.run(debug=False)
