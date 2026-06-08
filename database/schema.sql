CREATE TABLE transactions(
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    amount NUMERIC(15,2),
    country VARCHAR(20),
    merchant_type VARCHAR(50),
    event_time TIMESTAMP
);

CREATE TABLE fraud_alerts(
    alert_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    risk_level VARCHAR(20),
    alert_time TIMESTAMP
);