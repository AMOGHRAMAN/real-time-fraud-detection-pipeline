import json
import time
import random
import uuid
from kafka import KafkaProducer

TOPIC_NAME = "transactions_topic"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

countries = [
    "IN",
    "US",
    "UK",
    "NG",
    "BR",
    "CN",
    "RU",
    "ZA"
]

print("Fraud Producer Started...")

while True:
    txn = {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST{random.randint(100, 999)}",
        "amount": random.randint(1000, 1500000),
        "country": random.choice(countries)
    }

    producer.send(
        TOPIC_NAME,
        value=txn
    )

    print(
        f"Published: "
        f"{txn['transaction_id']} | "
        f"{txn['amount']} | "
        f"{txn['country']}"
    )

    time.sleep(0.2)
