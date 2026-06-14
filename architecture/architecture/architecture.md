+----------------------+
| Transaction Generator|
+----------+-----------+
           |
           v
+----------------------+
|       Kafka          |
| transactions_topic   |
+----------+-----------+
           |
           v
+----------------------+
| Spark Structured     |
| Streaming Consumer   |
+----------+-----------+
           |
           v
+----------------------+
| Fraud Detection      |
| Rules Engine         |
+----------+-----------+
           |
           v
+----------------------+
| PostgreSQL           |
| fraud_alerts         |
| transactions         |
+----------+-----------+
           |
           v
+----------------------+
| Dashboard / Reports  |
+----------------------+