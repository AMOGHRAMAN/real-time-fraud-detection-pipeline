import json
import logging
from kafka import KafkaConsumer
import psycopg2

from dlq_producer import send_to_dlq

# Logging Configuration

logging.basicConfig(
    filename="logs/fraud_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

TOPIC_NAME = "transactions_topic"

# Kafka Consumer

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers="localhost:9092",
    group_id="fraud-consumer-group",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# PostgreSQL Connection

conn = psycopg2.connect(
    host="localhost",
    database="frauddb",
    user="frauduser",
    password="fraudpass"
)

cursor = conn.cursor()


def calculate_risk(transaction):

    amount = transaction["amount"]
    country = transaction["country"]

    score = 0

    # Amount Based Scoring
    if amount > 1000000:
        score += 70

    elif amount > 500000:
        score += 50

    elif amount > 100000:
        score += 20

    # Country Based Scoring
    if country not in ["IN", "US", "UK"]:
        score += 30

    # Risk Classification
    if score >= 80:
        return "CRITICAL"

    elif score >= 50:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    return "LOW"


def validate_transaction(txn):

    required_fields = [
        "transaction_id",
        "customer_id",
        "amount",
        "country"
    ]

    for field in required_fields:

        if field not in txn:

            raise ValueError(
                f"Missing required field: {field}"
            )


print("Fraud Consumer Started...")
logging.info("Fraud Consumer Started")


for message in consumer:

    txn = message.value

    try:

        validate_transaction(txn)

        risk = calculate_risk(txn)

        message_text = (
            f"Transaction={txn['transaction_id']} | "
            f"Amount={txn['amount']} | "
            f"Country={txn['country']} | "
            f"Risk={risk}"
        )

        print(message_text)

        logging.info(message_text)

        
        # Store Transaction
        
        cursor.execute(
            """
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                amount,
                country,
                risk_level
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id)
            DO NOTHING
            """,
            (
                txn["transaction_id"],
                txn["customer_id"],
                txn["amount"],
                txn["country"],
                risk
            )
        )

        
        # Store Fraud Alerts
        
        if risk in ("HIGH", "CRITICAL"):

            cursor.execute(
                """
                INSERT INTO fraud_alerts (
                    transaction_id,
                    risk_level
                )
                VALUES (%s, %s)
                ON CONFLICT (transaction_id)
                DO NOTHING
                """,
                (
                    txn["transaction_id"],
                    risk
                )
            )

            logging.warning(
                f"Fraud Alert Generated | "
                f"Transaction={txn['transaction_id']} | "
                f"Risk={risk}"
            )

        conn.commit()

    except Exception as e:

        conn.rollback()

        error_message = (
            f"FAILED Transaction={txn.get('transaction_id')} "
            f"| Error={str(e)}"
        )

        print(error_message)

        logging.error(error_message)

        send_to_dlq(
            txn,
            str(e)
        )