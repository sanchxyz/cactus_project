from flask import Blueprint, render_template

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


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')  # Plantilla en templates/auth/

@auth_bp.route('/register')
def register():
    return render_template('auth/register.html')



@admin_bp.route('/dashboard')  # ✔️ Ruta para el dashboard de administración
def dashboard():
    return render_template('admin/dashboard.html')