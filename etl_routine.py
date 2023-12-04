import time

from sqlalchemy import Table

from database.database import Base, engine, db_name
from services import EventProcessor
from utils import contact_s3

# # testing - UNCOMENT to test on local machine
# from sqlalchemy import create_engine
# from database.configs import username, password, ip, port
# engine = create_engine(f'mysql+pymysql://{username}:{password}@localhost:{port}')

engine.execute(f"USE {db_name}")
Base.metadata.bind = engine

vehicle_table = Table("on_vehicle", Base.metadata, autoload=True, autoload_with=engine)
operating_table = Table(
    "on_operating_period", Base.metadata, autoload=True, autoload_with=engine
)


def run():
    # Load contact_s3 object
    etl = EventProcessor(contact_s3)
    print("contact_s3 object loaded")
    # Extract and transform events
    etl.process()
    print("S3_bucket events processed")
    # Load data into wharehouse
    etl.load(engine, vehicle_table, operating_table)
    print("Data loaded to wharehouse")
    print("Finished processing")


if __name__ == "__main__":
    while True:
        run()
        print("Wainting or next run...")
        time.sleep(60 * 60)  # 60 minutes
