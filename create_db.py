from database.db_model import VehicleModel, OperatingPeriodModel
from database.database import Base, engine, db_name

import time

if __name__ == "__main__":
    
    # Create db
    engine.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    engine.execute(f"USE {db_name}")
    
    # Create tables
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    print("tables successfully created")
    time.sleep(5)
