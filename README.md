# Real-Time Fraud Detection Pipeline

## Overview

A real-time fraud detection platform built using Apache Kafka, Python, PostgreSQL, Docker, and Streamlit.

The system simulates financial transaction events, processes them through a Kafka-based event-driven architecture, applies configurable fraud detection rules, persists results into PostgreSQL, and visualizes fraud metrics through a Streamlit dashboard.

---

## Architecture

Streamlit Dashboard

<img width="1201" height="1309" alt="image" src="https://github.com/user-attachments/assets/f803b2d4-ad8d-4952-ae35-bb198388cfaf" />


## Features

* Event-driven architecture using Apache Kafka
* Real-time transaction ingestion
* Rule-based fraud risk scoring
* PostgreSQL persistence layer
* Fraud alert generation
* Interactive dashboard
* Dockerized infrastructure
* Idempotent processing design

---

## Technology Stack

| Layer            | Technology    |
| ---------------- | ------------- |
| Language         | Python 3.12   |
| Messaging        | Apache Kafka  |
| Database         | PostgreSQL 16 |
| Containerization | Docker        |
| Dashboard        | Streamlit     |
| Version Control  | Git & GitHub  |

---

## Fraud Detection Logic

### Amount Rules

| Amount      | Score |
| ----------- | ----- |
| > 1,000,000 | +70   |
| > 500,000   | +50   |
| > 100,000   | +20   |

### Country Rules

| Country      | Score |
| ------------ | ----- |
| Not IN/US/UK | +30   |

### Risk Classification

| Score | Risk     |
| ----- | -------- |
| >= 80 | CRITICAL |
| >= 50 | HIGH     |
| >= 30 | MEDIUM   |
| < 30  | LOW      |

---

## Running The Project

### Start Infrastructure

docker compose up -d

### Start Consumer

python kafka/consumer.py

### Start Producer

python kafka/producer.py

### Launch Dashboard

streamlit run dashboard/app.py

## Future Enhancements

* Spark Structured Streaming
* Machine Learning Fraud Detection
* Grafana Monitoring
* Airflow Orchestration
* Kubernetes Deployment

---

## Author

Amogh Raman
Data Engineer | Apache Spark | Kafka | Airflow | GCP
