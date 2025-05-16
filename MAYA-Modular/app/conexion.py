# conexion.py
from sqlalchemy import create_engine
import os

def get_engine():
    user = os.getenv('DB_USER', 'jbpm')
    password = os.getenv('DB_PASS', 'jbpm')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'jbpm')
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')