# conexion.py
from sqlalchemy import create_engine


def get_engine():
    user = 'jbpm'
    password = 'jbpm'
    host = 'localhost'
    port = '5432'
    database = 'jbpm'
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
