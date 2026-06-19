import json
from kafka import KafkaProducer

DLQ_TOPIC = "fraud_dlq"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_to_dlq(transaction, error_message):

    dlq_record = {
        "failed_transaction": transaction,
        "error": error_message
    }

    producer.send(
        DLQ_TOPIC,
        value=dlq_record
    )

    producer.flush()

    print(
        f"Sent to DLQ | Error={error_message}"
    )