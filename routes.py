from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from models import User, Product, ProductImage, UserRole
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
    # Si ya está logueado, mostramos otra página
    if current_user.is_authenticated:
        return render_template('auth/already_logged_in.html', user=current_user)


    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        # Validación básica
        if not all([username, email, password]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('auth.login'))

        # Buscar usuario por username Y email
        user = User.query.filter_by(username=username, email=email).first()

        if not user or not user.check_password(password):
            flash('Credenciales inválidas', 'error')
            return redirect(url_for('auth.login'))


        login_user(user)
        flash('¡Bienvenido, {}!'.format(user.username), 'success')
        return redirect(url_for('admin.dashboard'))  # 🔄 Cambia esta línea

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))



@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Verificar permisos primero
    if current_user.role != UserRole.admin:
        flash("No tienes permisos de administrador", "danger")
        return redirect(url_for('main.index'))

    # Inicializar variables para GET o POST
    username = email = password = confirm = ""
    form_errors = {}

    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Validaciones
        if not all([username, email, password, confirm]):
            form_errors['required'] = 'Todos los campos son obligatorios'
        
        if password != confirm:
            form_errors['password_mismatch'] = 'Las contraseñas no coinciden'
        
        if len(password) < 8:
            form_errors['password_length'] = 'La contraseña debe tener al menos 8 caracteres'

        # Verificar si el usuario/email ya existe
        exists = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if exists:
            form_errors['exists'] = 'El usuario o email ya están registrados'

        # Si hay errores, mostrarlos
        if form_errors:
            for error in form_errors.values():
                flash(error, 'danger')
            return render_template('auth/register.html', 
                username=username, 
                email=email, 
                form_errors=form_errors
            )

        # Si todo está bien, crear usuario
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Cuenta creada exitosamente', 'success')
        return redirect(url_for('auth.login'))

    # Renderizar template (GET o POST con errores)
    return render_template('auth/register.html', 
        username=username, 
        email=email,
        form_errors=form_errors
    )





@admin_bp.route('/dashboard')  # ✔️ Ruta para el dashboard de administración
@login_required 
def dashboard():
    return render_template('admin/dashboard.html')