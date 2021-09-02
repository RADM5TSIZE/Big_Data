from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StringType, DateType, BooleanType, StructType, TimestampType
import mysqlx

dbOptions = {"host": "my-app-mysql-service", 'port': 3306, "user": "root", "password": "root"}
dbSchema = 'crimes'
slidingDuration = '1 minute'


# Create a spark session
spark = SparkSession.builder \
    .appName("Structured Streaming").getOrCreate()

# Set log level
spark.sparkContext.setLogLevel('ERROR')

# Read messages from Kafka
kafkaMessages = spark \ 
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", \
            "my-cluster-kafka-bootstrap:9091") \
    .option("subscribe", "crime-topic") \
    .option("startingOffsets", "earliest") \
    .load()    

print("test123", kafkaMessages)

# Define schema of crime data
crimeSchema = StructType() \
    .add("id", IntegerType()) \
    .add("casenumber", StringType()) \
    .add("date", DateType()) \
    .add("block", StringType()) \
    .add("iucr", IntegerType()) \
    .add("primarytype", StringType()) \
    .add("description", StringType()) \
    .add("locationdescription", StringType()) \
    .add("arrest", BooleanType()) \
    .add("domestic", StringType()) \
    .add("beat", StringType()) \
    .add("district", StringType()) \
    .add("ward", StringType()) \
    .add("communityarea", StringType()) \
    .add("fbicode", IntegerType()) \
    .add("xcoordinate", IntegerType()) \
    .add("ycoordinate", IntegerType()) \
    .add("year", IntegerType()) \
    .add("updatedon", StringType()) \
    .add("latitude", IntegerType()) \
    .add("longitude", IntegerType()) \
    .add("location", StringType())

#Parse JSON messages 
crimeMessages = kafkaMessages.select(
    # Extract 'value' from Kafka message (i.e., the tracking data)
    from_json(
        column("value").cast("string"),
        crimeSchema
    ).alias("json")
).select(
    # Select all JSON fields
    column("json.*")
) \
    .withColumnRenamed('json.id', 'id') \
    .withColumnRenamed('json.casenumber', 'casenumber') \
    .withColumnRenamed('json.date', 'date') \
    .withColumnRenamed('json.block', 'block') \
    .withColumnRenamed('json.iucr', 'iucr') \
    .withColumnRenamed('json.primarytype', 'primarytype') \
    .withColumnRenamed('json.dscription', 'description') \
    .withColumnRenamed('json.locationdescription', 'locationdescription') \
    .withColumnRenamed('json.arrest', 'arrest') \
    .withColumnRenamed('json.domestic', 'domestic') \
    .withColumnRenamed('json.beat', 'beat') \
    .withColumnRenamed('json.district', 'district') \
    .withColumnRenamed('json.ward', 'ward') \
    .withColumnRenamed('json.communityarea', 'communityarea') \
    .withColumnRenamed('json.fbicode', 'fbicode') \
    .withColumnRenamed('json.xcoordinate', 'xcoordinate') \
    .withColumnRenamed('json.ycoordinate', 'ycoordinate') \
    .withColumnRenamed('json.year', 'year') \
    .withColumnRenamed('json.updatedon', 'updatedon') \
    .withColumnRenamed('json.latitude', 'latitude') \
    .withColumnRenamed('json.longitude', 'longitude') \
    .withColumnRenamed('json.location', 'location') \
    #.withWatermark("parsed_timestamp", windowDuration)

"""
# Example Part 4
# Compute most popular slides
popular = trackingMessages.groupBy(
    window(
        column("parsed_timestamp"),
        windowDuration,
        slidingDuration
    ),
    column("mission")
).count().withColumnRenamed('count', 'views')
"""
#INS Miguel: Group by year

crimesperyear = crimeMessages.groupBy(
    column("year")
).count().withColumnRenamed('count', 'yearcount')




# Example Part 5
# Start running the query; print running counts to the console
consoleDump = crimesperyear \
    .writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Example Part 6


def saveToDatabase(batchDataframe, batchId):
    # Define function to save a dataframe to mysql
    def save_to_db(iterator):
        # Connect to database and use schema
        session = mysqlx.get_session(dbOptions)
        session.sql("USE crimesperyear").execute()  # Spark DataFrame mit Verhaftungen nutzen

        for row in iterator:
            # Run upsert (insert or update existing)
            sql = session.sql("INSERT INTO Crime_Year "
                              "(YEAR, COUNT) VALUES (?, ?) "
                              "ON DUPLICATE KEY UPDATE COUNT=?")
            sql.bind(row.year, row.count, row.count).execute()

        session.close()

    # Perform batch UPSERTS per data partition
    batchDataframe.foreachPartition(save_to_db)

# Example Part 7


dbInsertStream = crimesperyear.writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .foreachBatch(saveToDatabase) \
    .start()


# Wait for termination
spark.streams.awaitAnyTermination()
