from models import User, UserRole
from extensions import db

def test_successful_login(client, app):
    """
    Prueba el flujo de un inicio de sesión exitoso.
    """
    # 1. PREPARACIÓN: Creamos un usuario de prueba directamente en la BD temporal
    with app.app_context():
        test_user = User(username='testuser', email='test@test.com', role=UserRole.admin)
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()

    # 2. ACCIÓN: Simulamos el envío del formulario de login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True) # Sigue la redirección después del login

    # 3. VERIFICACIÓN: Comprobamos que el resultado es el esperado
    assert response.status_code == 200 # La página cargó bien
    assert b"Bienvenido, testuser!" in response.data # Aparece el mensaje flash
    assert b"Centro de Control" in response.data # Se cargó el contenido del dashboard