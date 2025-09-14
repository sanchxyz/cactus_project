import pymysql
import sys
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
# Esto buscará un archivo .env en la misma carpeta (o carpetas superiores)
load_dotenv()

# --- CONFIGURACIÓN DE LA CONEXIÓN DESDE EL ENTORNO ---
# Leemos las credenciales del entorno. Usamos valores por defecto por si alguna no está definida.
DB_CONFIG = {
    # Si el script corre en tu máquina local (host), usa '127.0.0.1'.
    # Si corre en otro contenedor Docker en la misma red, usa el nombre del servicio: 'camila_db'.
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3306)), # El puerto debe ser un número entero
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'cursorclass': pymysql.cursors.DictCursor
}

def test_connection():
    """
    Intenta conectarse a la base de datos y ejecuta una consulta simple.
    """
    # Validar que las variables esenciales fueron cargadas
    if not all([DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['database']]):
        print("❌ Error: Faltan variables de entorno. Asegúrate de que MYSQL_USER, MYSQL_PASSWORD y MYSQL_DATABASE estén en tu .env")
        return # Salir de la función si faltan datos

    connection = None
    try:
        print("Intentando conectar a la base de datos...")
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ ¡Conexión exitosa!")

        with connection.cursor() as cursor:
            sql_query = "SELECT VERSION();"
            cursor.execute(sql_query)
            result = cursor.fetchone()
            print(f"Versión de la base de datos MySQL: {result['VERSION()']}")
            print("--------------------------------------------------")
            print("La configuración y las credenciales son correctas.")

    except pymysql.MySQLError as e:
        print(f"❌ ¡Error al conectar a la base de datos!")
        print(f"Detalles del error: {e}")

    finally:
        if connection:
            connection.close()
            print("Conexión cerrada.")

# --- Ejecutar la función de prueba ---
if __name__ == "__main__":
    test_connection()

