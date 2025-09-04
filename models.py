from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event, CheckConstraint
from sqlalchemy.orm import validates
import enum
from extensions import db

# ------------------------------------------
# ENUMS (Mejor organización y type-safety)
# ------------------------------------------
class UserRole(enum.Enum):
    admin = "admin"
    editor = "editor"

class SunExposure(enum.Enum):
    directo = "directo"
    indirecto = "indirecto"
    parcial = "parcial"
    sombra = "sombra"

class Watering(enum.Enum):
    bajo = "bajo"
    moderado = "moderado"
    alto = "alto"
class ProductCategory(enum.Enum):
    cactus = "cactus"
    suculenta = "suculenta"
    otro = "otro"
    destacado = "destacado"

# ------------------------------------------
# MODELO USER (Con mejoras de seguridad)
# ------------------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)  # Índice para búsquedas
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.editor)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones explícitas con nombres descriptivos
    created_products = db.relationship(
        'Product', 
        foreign_keys='Product.created_by', 
        backref='creator', 
        lazy='dynamic'
    )
    updated_products = db.relationship(
        'Product', 
        foreign_keys='Product.updated_by', 
        backref='updater', 
        lazy='dynamic'
    )

    # ---- Métodos de seguridad ----
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# ------------------------------------------
# MODELO PRODUCT (Con validaciones mejoradas)
# ------------------------------------------
class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('price_level BETWEEN 1 AND 100', name='check_price_level'),  # Restricción a nivel BD
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)  # Índice para búsquedas
    category = db.Column(db.Enum(ProductCategory), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sun_exposure = db.Column(db.Enum(SunExposure), nullable=False)
    watering = db.Column(db.Enum(Watering), nullable=False)
    fertilizer = db.Column(db.String(100), nullable=False)  # Longitud de 100 en lugar de 50
    price_level = db.Column(db.SmallInteger, nullable=False)  # ← Nuevo campo (SmallInteger = TINYINT UNSIGNED)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Llaves foráneas con ondelete explícito
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=True)

    # Validación de precios a nivel de modelo
    @validates('price_level')
    def validate_price_level(self, key, value):
        if not (1 <= value <= 100):
            raise ValueError("El nivel de precio debe estar entre 1 y 100")
        return value

    def __repr__(self):
        return f"<Product {self.name}>"

# ------------------------------------------
# MODELO PRODUCT_IMAGE (Con gestión de cascada mejorada)
# ------------------------------------------
class ProductImage(db.Model):
    __tablename__ = 'product_images'
    __table_args__ = (
        db.Index('idx_product_id', 'product_id'),  # Índice para JOINs frecuentes
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, 
        db.ForeignKey('products.id', ondelete='CASCADE'),  # Cascada en BD
        nullable=False
    )
    image_url = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(100), nullable=True)
    is_main = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con cascada en ORM + BD
    product = db.relationship(
        'Product', 
        backref=db.backref(
            'images', 
            cascade='all, delete-orphan',  # Eliminación en cascada vía ORM
            passive_deletes=True  # Respeta la cascada de la BD
        )
    )

    def __repr__(self):
        return f"<ProductImage {self.image_url}>"