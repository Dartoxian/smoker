import json
import psycopg2
from mqtt_client import client

conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
conn.autocommit = True

if __name__ == "__main__":

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        data = json.loads(msg.payload)
        with conn.cursor() as cur:
            for key, value in data.items():
                cur.execute(
                    "INSERT INTO temp_records (created_at, source, value) VALUES (CURRENT_TIMESTAMP,%s, %s)",
                    (key, value))
            conn.commit()

    client.on_message = on_message
    client.subscribe("smoker")
    client.loop_forever()

