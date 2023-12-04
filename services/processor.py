import json
import os
import re
from datetime import datetime

from sqlalchemy.dialects.mysql import insert


class EventProcessor:
    def __init__(self, contact_s3):

        # Depends on contact_s3 object
        self.s3_client, self.bucket_name, self.events = contact_s3()

        # Init instances
        self.vehicle_instances = []
        self.operating_period_instances = []

    def process(self):
        n_events = len(self.events)
        count = 0
        for event in self.events:
            # progress
            count += 1
            print(
                "\rprocessing {:.0%} - file: {}".format(count / n_events, event),
                end="",
                flush=True,
            )

            # Rename downloaded file
            d_event = "lib/" + "downloaded-" + re.findall(r"data/(.+)", event)[0]

            # Download file from s3 bucket
            self.s3_client.download_file(self.bucket_name, event, d_event)

            # send file to s3 bucket
            # Here I could use another s3 client to send the files to another s3 bucket
            # But I didn't have time to learn about that
            # sorry

            # Read jsons
            jsons = EventProcessor.__read_jsons(d_event)

            for jsn in jsons:
                # Extract variables
                cln_json = EventProcessor.__extract_variables(jsn)

                # Clean date
                cln_json["at"] = EventProcessor.__process_date(cln_json["at"])

                if cln_json["on"] != "vehicle":
                    # Clean dates
                    for key in ["start", "finish"]:
                        cln_json[key] = EventProcessor.__process_date(cln_json[key])
                    # Append instance
                    cln_json.pop("on", None)
                    self.operating_period_instances.append(cln_json)
                else:
                    # Append instance
                    cln_json.pop("on", None)
                    if "lat" not in cln_json.keys():
                        cln_json["lat"] = None
                    if "lng" not in cln_json.keys():
                        cln_json["lng"] = None
                    self.vehicle_instances.append(cln_json)

            try:
                os.remove(d_event)  # remove temporary file
            except OSError:
                pass

        return print("All events processed successfully")

    def load(self, engine, vehicle_table, operating_table):

        # mini-batch bulk insert vehicle info
        stmt = insert(vehicle_table).values(self.vehicle_instances)
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.close()

        # mini-batch bulk insert operating_period info
        stmt = insert(operating_table).values(self.operating_period_instances)
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.close()
        return print("loading complete!")

    @staticmethod
    def __read_jsons(event_file):
        jsons = []
        with open(event_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                jsons.append(json.loads(line))
        return jsons

    @staticmethod
    def __extract_variables(data):
        variables = {}
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    variables.update(EventProcessor.__extract_variables(value))
                else:
                    variables[key] = value
        return variables

    @staticmethod
    def __process_date(date_string):
        # Convert string to datetime object
        datetime_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        # remove microsec info
        datetime_obj = datetime.combine(
            datetime_obj.date(), datetime_obj.time().replace(microsecond=0)
        )

        return datetime_obj
