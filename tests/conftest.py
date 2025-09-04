import pytest
from app import create_app
from extensions import db

@pytest.fixture(scope='module')
def app():
    """Crea una instancia de la aplicación Flask para las pruebas."""
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
        # Usa una base de datos en memoria para no tocar tu BD real
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,  # Desactivamos CSRF para facilitar las pruebas
    })

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """Un cliente de prueba para la aplicación."""
    return app.test_client()