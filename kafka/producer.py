import json
import time
from kafka import KafkaProducer

TOPIC_NAME = "transactions_topic"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

with open("kafka/sample_events.json", "r") as file:
    transactions = json.load(file)

for txn in transactions:

    producer.send(
        TOPIC_NAME,
        value=txn
    )

    print(f"Published Transaction: {txn['transaction_id']}")

    time.sleep(2)

producer.flush()

print("All transactions published successfully.")