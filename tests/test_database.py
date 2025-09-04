import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import pytest

# Cargamos las variables del archivo .env al entorno
load_dotenv()

# Leemos la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

def test_database_connection():
    """
    Prueba que la aplicación puede conectarse a la base de datos.
    """
    # Si no se encuentra la variable, la prueba se omite en lugar de fallar
    if not DATABASE_URL:
        pytest.skip("No se encontró la DATABASE_URL en las variables de entorno, omitiendo prueba.")

    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()

        # La prueba pasa si la conexión no es None.
        assert connection is not None

        connection.close()
    except OperationalError as e:
        # Si hay un error de conexión, la prueba falla explícitamente.
        pytest.fail(f"No se pudo conectar a la base de datos: {e}")