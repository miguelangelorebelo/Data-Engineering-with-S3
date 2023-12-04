# Data Engineering Project

### Author: Miguel Ângelo Pontes Rebelo

To see it in action simply run:
`make up`

This will use docker compose to build the containers and start them.

You can connect to the db:
host: localhost
port: 3306
user: root
password: password (very secure)

To remove them (and the images):
`make down`

This downloads the event jsons from the s3 bucket, extracts and transforms the data and loads it into 2 separate tables in the loka_db. (A database on a MariaDB running on a separate docker). Unfortunatelly I didn't had time to configure a data lake. This is something that I've never done so it would have taken me some extra time to figure out. 

The process goes like this:
- The first time it runs `create_db.py` script that creates the db and tables in the MariaDB container.
- the `etl_routine.py` is called every day at the same hour.
- it uses the `processor` class in `services` to collect, extract, transform and load the data into the db.
- the `processor` needs a function in `utils`, which is responsible for contacting the s3 bucket.

I hope you like the project. It was fun to build it. 
