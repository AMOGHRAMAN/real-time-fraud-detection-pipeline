import json
from kafka import KafkaConsumer
import psycopg2

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

    # Amount-based scoring
    if amount > 1000000:
        score += 70

    elif amount > 500000:
        score += 50

    elif amount > 100000:
        score += 20

    # Country-based scoring
    if country not in ["IN", "US", "UK"]:
        score += 30

    # Risk classification
    if score >= 80:
        return "CRITICAL"

    elif score >= 50:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    return "LOW"


print("Fraud Consumer Started...")


for message in consumer:

    try:

        txn = message.value

        risk = calculate_risk(txn)

        print(
            f"Transaction={txn['transaction_id']} | "
            f"Amount={txn['amount']} | "
            f"Country={txn['country']} | "
            f"Risk={risk}"
        )

        # Store all transactions
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

        # Store only suspicious transactions
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

        conn.commit()

    except Exception as e:

        print(f"Error processing transaction: {e}")

        conn.rollback()