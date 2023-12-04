from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from .configs import username, password, ip, port

db_name = "data_db"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{ip}:{port}")

Base = declarative_base()
