import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# db_env values
user = 'root'
passwd = 'P@ssw0rd'
host = 'localhost'
port = 3306
db = 'flightstat_db'

# DB configuration
# DATABASE_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'
DATABASE_URL = sqlalchemy.engine.URL.create(drivername="mysql", username=user, password=passwd, host=host, port=port, database=db)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()