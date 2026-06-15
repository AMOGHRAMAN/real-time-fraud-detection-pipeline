from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("FraudDetectionPipeline")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "transactions_topic")
    .option("startingOffsets", "earliest")
    .load()
)

transactions = df.selectExpr(
    "CAST(value AS STRING) as transaction_json"
)

query = (
    transactions.writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()