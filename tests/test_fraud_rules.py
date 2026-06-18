from kafka.fraud_engine import calculate_risk


def test_low_risk_transaction():

    txn = {
        "amount": 5000,
        "country": "IN"
    }

    assert calculate_risk(txn) == "LOW"


def test_high_risk_transaction():

    txn = {
        "amount": 750000,
        "country": "IN"
    }

    assert calculate_risk(txn) == "HIGH"


def test_critical_risk_transaction():

    txn = {
        "amount": 750000,
        "country": "NG"
    }

    assert calculate_risk(txn) == "CRITICAL"