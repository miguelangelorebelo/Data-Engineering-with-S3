FROM python:3.10

RUN python -m pip install --upgrade pip
RUN apt-get update

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN echo "#!/bin/bash\n"\
         "sleep 10s\n"\
         "python create_db.py\n"\
         "python etl_routine.py" >> launch.sh

RUN chmod +x launch.sh

ENTRYPOINT [ "./launch.sh" ]