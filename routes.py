from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from models import User, Product, ProductImage
from extensions import db

# Creación del blueprint principal
main = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')    


@main.route('/')
def index():
    # Renderiza el template 'index.html'
    return render_template('index.html')

@main.route('/cactus')
def cactus():
    # Renderiza el template 'cactus.html'
    return render_template('cactus.html')

@main.route('/suculentas')
def succulentas():
    # Renderiza el template 'succulentas.html'
    return render_template('suculentas.html')

@main.route('/otros')
def otros():
    # Renderiza el template 'otros.html'
    return render_template('otros.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        # Validación básica
        if not all([username, email, password]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('auth.login'))

        # Buscar usuario por username Y email
        user = User.query.filter_by(username=username, email=email).first()

        if not user or not user.check_password(password):
            flash('Credenciales inválidas', 'danger')
            return redirect(url_for('auth.login'))

        # Iniciar sesión
        login_user(user)
        flash('¡Bienvenido, {}!'.format(user.username), 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        # Validaciones básicas
        if not all([username, email, password, confirm]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar unicidad de usuario y email
        exists = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if exists:
            flash('El nombre de usuario o el email ya están en uso', 'danger')
            return redirect(url_for('auth.register'))

        # Crear y guardar usuario
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Cuenta creada con éxito. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')





@admin_bp.route('/dashboard')  # ✔️ Ruta para el dashboard de administración
def dashboard():
    return render_template('admin/dashboard.html')