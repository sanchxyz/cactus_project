from flask import Blueprint, render_template

# Creación del blueprint principal
main = Blueprint('main', __name__)


@main.route('/')
def index():
    # Renderiza el template 'index.html'
    return render_template('index.html')