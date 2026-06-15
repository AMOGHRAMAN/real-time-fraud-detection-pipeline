import json
from kafka import KafkaConsumer
import psycopg2

TOPIC_NAME = "transactions_topic"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers="localhost:9092",
    group_id="fraud-consumer-group",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

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

    if amount > 1000000:
        score += 70

    elif amount > 500000:
        score += 50

    elif amount > 100000:
        score += 20

    if country not in ["IN", "US", "UK"]:
        score += 30

    if score >= 80:
        return "CRITICAL"

    elif score >= 50:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    return "LOW"
for message in consumer:

    txn = message.value

    risk = calculate_risk(txn)

    print(
        f"Transaction={txn['transaction_id']} "
        f"Amount={txn['amount']} "
        f"Country={txn['country']} "
        f"Risk={risk}"
    )

    cursor.execute(
    """
    INSERT INTO fraud_alerts(
        transaction_id,
        risk_level
    )
    VALUES (%s,%s)
    ON CONFLICT (transaction_id)
    DO NOTHING
    """,
    (
        txn["transaction_id"],
        risk
    )
)

    if risk in ("HIGH", "CRITICAL"):

        cursor.execute(
    """
    INSERT INTO fraud_alerts(
        transaction_id,
        risk_level
    )
    VALUES (%s,%s)
    ON CONFLICT (transaction_id)
    DO NOTHING
    """,
    (
        txn["transaction_id"],
        risk
    )
)

    conn.commit()