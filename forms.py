# en forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from models import ProductCategory, SunExposure, Watering
from wtforms import PasswordField
from wtforms.validators import Email, EqualTo, ValidationError
from models import User



class ProductForm(FlaskForm):
    """Formulario para crear y editar productos."""

    name = StringField(
        'Nombre del Producto',
        validators=[DataRequired(), Length(min=3, max=100)]
    )

    description = TextAreaField(
        'Descripción',
        validators=[Length(max=500)]
    )

    category = SelectField(
        'Categoría',
        choices=[(cat.name, cat.value.capitalize()) for cat in ProductCategory],
        validators=[DataRequired()]
    )

    sun_exposure = SelectField(
        'Exposición Solar',
        choices=[(sun.name, sun.value.capitalize()) for sun in SunExposure],
        validators=[DataRequired()]
    )

    watering = SelectField(
        'Nivel de Riego',
        choices=[(wat.name, wat.value.capitalize()) for wat in Watering],
        validators=[DataRequired()]
    )

    fertilizer = StringField(
        'Fertilizante',
        validators=[DataRequired(), Length(min=3, max=100)]
    )

    price_level = IntegerField(
        'Nivel de Precio (1-100)',
        validators=[DataRequired(), NumberRange(min=1, max=100)]
    )

    image = FileField(
        'Imagen Principal',
        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], '¡Solo se permiten imágenes!')]
    )


    submit = SubmitField('Guardar Producto')






class RegistrationForm(FlaskForm):
    """Formulario de registro con validaciones."""
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(message="Por favor, introduce un email válido.")])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, message="La contraseña debe tener al menos 8 caracteres.")])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                     validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    role = SelectField('Rol', choices=[('editor', 'Editor'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Crear Cuenta')

    # Función para validar que el username no esté ya en uso
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')

    # Función para validar que el email no esté ya registrado
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Ese correo electrónico ya está registrado.')


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión."""
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(message="Por favor, introduce un email válido.")])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')