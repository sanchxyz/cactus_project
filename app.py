from flask import Flask
from config import Config          # Configuración de la aplicación (variables de entorno, BD, etc.)
from extensions import db, login_manager  # Extensiones: SQLAlchemy (BD) y LoginManager (autenticación)
from routes import main            # Blueprint con rutas principales (ej: página de inicio)
from models import User            # Modelo de usuario para la autenticación

def create_app():
    """Factory function para crear y configurar la instancia de la aplicación Flask."""
    app = Flask(__name__)
    
    # Cargar configuración desde la clase Config (config.py)
    app.config.from_object(Config)
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)               # Conectar SQLAlchemy con la app
    login_manager.init_app(app)    # Conectar Flask-Login con la app

    # Configurar user_loader para Flask-Login (necesario para cargar usuarios desde la BD)
    @login_manager.user_loader
    def load_user(user_id):
        """Callback para recargar el objeto usuario desde el ID guardado en la sesión."""
        return User.query.get(int(user_id))  # Query directamente usando SQLAlchemy
    
    # Registrar blueprints (rutas)
    app.register_blueprint(main)    # Registra las rutas definidas en el blueprint 'main'
    
    return app

if __name__ == '__main__':
    # Crear la aplicación y ejecutarla en modo debug
    app = create_app()
    app.run(debug=True)            # ¡OJO: En producción debug=False!