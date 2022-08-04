from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import setting

#SQLALCHEMY_DATABASE_URL= 'postgresql://postgres:root@localhost/postgres' #postgres://username:password@localhost/database

SQLALCHEMY_DATABASE_URL= f"postgresql://{setting.database_name}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_username}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False , autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try: 
        conn = psycopg2.connect(host = 'localhost', database= 'postgres', user='postgres', password= 'root',
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connected Successfully.')
        break
    except Exception as error:
        print('Database connection failed.')
        print('Error:', error )
        time.sleep(2)
