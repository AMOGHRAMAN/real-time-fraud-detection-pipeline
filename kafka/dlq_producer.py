import json
import logging
from kafka import KafkaProducer

# Logging Configuration

logging.basicConfig(
    filename="logs/fraud_pipeline.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

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

    try:

        producer.send(
            DLQ_TOPIC,
            value=dlq_record
        )

        producer.flush()

        message = (
            f"Sent to DLQ | "
            f"Transaction={transaction.get('transaction_id', 'UNKNOWN')} | "
            f"Error={error_message}"
        )

        print(message)

        logging.warning(message)

    except Exception as e:

        logging.error(
            f"Failed to publish message to DLQ | Error={str(e)}"
        )

        print(
            f"Failed to publish message to DLQ | Error={str(e)}"
        )