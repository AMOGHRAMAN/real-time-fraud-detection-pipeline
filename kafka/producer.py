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
        "customer_id": f"CUST{random.randint(100,999)}",
        "amount": random.randint(1000,1500000),
        "country": random.choice(countries)
    }

    # Generate bad records intentionally
    if random.randint(1,10) == 1:

        txn = {
            "transaction_id": str(uuid.uuid4()),
            "customer_id": f"CUST{random.randint(100,999)}",
            "amount": random.randint(1000,1500000)
        }

    producer.send(
        TOPIC_NAME,
        value=txn
    )

    print(
        f"Published: "
        f"{txn.get('transaction_id')} | "
        f"{txn.get('amount')} | "
        f"{txn.get('country','MISSING')}"
    )

    time.sleep(0.2)