from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://app_user:Userpasstokenhashcode2025DB@127.0.0.1/camila_db")
connection = engine.connect()
print("¡Conexión exitosa!")
connection.close()