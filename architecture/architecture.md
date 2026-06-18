# System Architecture

<img width="1201" height="1309" alt="image" src="https://github.com/user-attachments/assets/bb176ffa-76d3-40bc-a1f8-534b91ffbdb8" />


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
