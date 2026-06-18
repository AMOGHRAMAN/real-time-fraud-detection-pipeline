CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    amount NUMERIC,
    country VARCHAR(10),
    risk_level VARCHAR(20),
    created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS fraud_alerts;

CREATE TABLE fraud_alerts (
    transaction_id VARCHAR(50) PRIMARY KEY,
    risk_level VARCHAR(20),
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);