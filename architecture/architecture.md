# System Architecture

## High-Level Architecture

![Architecture](architecture.png)

## Components

### Producer
Generates transaction events and publishes them to Kafka.

### Kafka
Acts as the event streaming backbone.

### Consumer
Consumes transactions and applies fraud scoring rules.

### PostgreSQL
Stores processed transactions and fraud alerts.

### Streamlit
Provides real-time visualization and analytics.
