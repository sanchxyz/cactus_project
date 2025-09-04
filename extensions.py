
# Importar clases de las extensiones Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

# Inicializar la extensión SQLAlchemy para manejar la base de datos
db = SQLAlchemy()

# Inicializar la extensión LoginManager para manejar la autenticación de usuarios
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate() 
# Configurar la ruta de login para redirigir usuarios no autenticados
# ('auth.login' asume un blueprint llamado 'auth' con endpoint 'login')
login_manager.login_view = 'auth.login'

# Establecer la categoría de mensaje para mostrar alertas de login
login_manager.login_message_category = 'info'