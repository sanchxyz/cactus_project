from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import current_app
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, login_required, logout_user
from models import User, Product, ProductImage, UserRole, ProductCategory
from extensions import db
from forms import ProductForm, RegistrationForm, LoginForm
import os

# Creación del blueprint principal
main = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')    



@main.route('/')
def index():
    # Buscamos solo los productos de la categoría 'destacado'
    destacados_products = Product.query.filter_by(category=ProductCategory.destacado).all()
    # Le pasamos la lista de productos y la página activa a la plantilla
    return render_template('index.html', active_page='home', products=destacados_products)

@main.route('/cactus')
def cactus():
    cactus_products = Product.query.filter_by(category=ProductCategory.cactus).all()
    # Ahora le pasamos la variable para activar el enlace del menú
    return render_template('cactus.html', products=cactus_products, active_page='cactus')


@main.route('/suculentas')
def succulentas():
    suculenta_products = Product.query.filter_by(category=ProductCategory.suculenta).all()
    # Añadimos la variable para activar el enlace del menú
    return render_template('suculentas.html', products=suculenta_products, active_page='suculentas')

@main.route('/otros')
def otros():
    otros_products = Product.query.filter_by(category=ProductCategory.otro).all()
    # Añadimos la variable para activar el enlace del menú
    return render_template('otros.html', products=otros_products, active_page='otros')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('auth/already_logged_in.html', user=current_user)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('¡Bienvenido, {}!'.format(user.username), 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))





@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Se asegura de que solo los administradores puedan registrar
    if current_user.role != UserRole.admin:
        flash("No tienes permisos de administrador", "danger")
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Si el formulario es válido, crea el usuario
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            role=UserRole[form.role.data]
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada exitosamente para {}'.format(user.username), 'success')
        return redirect(url_for('auth.login'))

    # Si el método es GET o el formulario no es válido, muestra la página con el formulario
    return render_template('auth/register.html', form=form)





@admin_bp.route('/dashboard')  #  Ruta para el dashboard de administración
@login_required 
def dashboard():
    return render_template('admin/dashboard.html')




@admin_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        # Primero, creamos el producto para obtener un ID
        new_product = Product(
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            sun_exposure=form.sun_exposure.data,
            watering=form.watering.data,
            fertilizer=form.fertilizer.data,
            price_level=form.price_level.data,
            created_by=current_user.id
        )
        db.session.add(new_product)
        db.session.commit() # Hacemos commit para que new_product.id esté disponible

        
        image_file = form.image.data
        if image_file:
            # 1. Asegurar el nombre del archivo
            filename = secure_filename(image_file.filename)
            # 2. Crear la ruta completa para guardar
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            # 3. Guardar el archivo físico
            image_file.save(filepath)

            # 4. Guardar la referencia en la base de datos
            new_image = ProductImage(
                product_id=new_product.id,
                image_url=f'uploads/{filename}', # URL relativa para usar en HTML
                is_main=True
            )
            db.session.add(new_image)
            db.session.commit()

        flash('¡Producto añadido exitosamente!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_product.html', form=form, title="Añadir Producto")


@admin_bp.route('/manage')
@login_required
def manage_products():
    # Obtenemos todos los productos ordenados por nombre
    all_products = Product.query.order_by(Product.name).all()
    return render_template('admin/manage_products.html', products=all_products, title="Gestionar Productos")



@admin_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        # ---- INICIA LA NUEVA LÓGICA DE GUARDADO ----
        form.populate_obj(product)

        # Manejo de la imagen (si el usuario sube una nueva)
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)

            # Busca si ya hay una imagen principal para actualizarla, o crea una nueva
            main_image = ProductImage.query.filter_by(product_id=product.id, is_main=True).first()
            if main_image:
                main_image.image_url = f'uploads/{filename}'
            else:
                new_image = ProductImage(
                    product_id=product.id,
                    image_url=f'uploads/{filename}',
                    is_main=True
                )
                db.session.add(new_image)

        # Guarda todos los cambios en la base de datos
        db.session.commit()

        flash('¡Producto actualizado exitosamente!', 'success')
        return redirect(url_for('admin.manage_products'))


    return render_template('admin/add_product.html', form=form, title="Editar Producto")





@admin_bp.route('/delete_list')
@login_required
def delete_list():
    # Obtenemos todos los productos para listarlos
    all_products = Product.query.order_by(Product.name).all()
    return render_template('admin/delete_product_list.html', products=all_products, title="Eliminar un Producto")



@admin_bp.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    # Buscamos el producto. Si no existe, dará un error 404.
    product_to_delete = Product.query.get_or_404(product_id)

    # 1. Eliminar las imágenes asociadas del servidor
    for image in product_to_delete.images:
        try:
            # Extrae solo el nombre del archivo de la URL
            filename = os.path.basename(image.image_url)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Error eliminando archivo de imagen: {e}") # Log para el servidor

    # 2. Eliminar el producto de la base de datos
    db.session.delete(product_to_delete)
    db.session.commit()

    flash('Producto eliminado exitosamente.', 'success')
    # Redirige de vuelta a la lista de eliminación
    return redirect(url_for('admin.delete_list'))