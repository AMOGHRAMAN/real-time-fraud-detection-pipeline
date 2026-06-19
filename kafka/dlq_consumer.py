import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "fraud_dlq",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m:
        json.loads(m.decode("utf-8"))
)

print("Listening to DLQ...")

for message in consumer:

    print("\nDLQ RECORD")

    print(
        json.dumps(
            message.value,
            indent=4
        )
    )