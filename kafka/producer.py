import json
import time
from kafka import KafkaProducer

TOPIC_NAME = "transactions_topic"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

transactions = [
    {
        "transaction_id": "TXN1001",
        "customer_id": "CUST101",
        "amount": 5000,
        "country": "IN"
    },
    {
        "transaction_id": "TXN1002",
        "customer_id": "CUST102",
        "amount": 750000,
        "country": "NG"
    }
]

for txn in transactions:

    producer.send(
        TOPIC_NAME,
        value=txn
    )

    print(f"Published: {txn['transaction_id']}")

    time.sleep(0.2)

producer.flush()

print("All messages published")