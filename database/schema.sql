CREATE TABLE transactions(
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    amount NUMERIC(15,2),
    country VARCHAR(10),
    risk_level VARCHAR(20),
    processed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fraud_alerts(
    alert_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    risk_level VARCHAR(20),
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);