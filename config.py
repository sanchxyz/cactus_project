import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or os.environ.get("SECRET_KEY")
    
    # Validación directa en la asignación
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or os.environ.get("DATABASE_URL") 
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')

    
    # Verificación inmediata al cargar la clase
    if not SQLALCHEMY_DATABASE_URI:  
        raise RuntimeError("Falta DATABASE_URL en .env o variables de entorno")