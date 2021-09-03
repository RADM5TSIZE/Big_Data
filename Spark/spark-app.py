from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StringType, DateType, BooleanType, StructType, TimestampType
import mysqlx
import sys

dbOptions = {"host": "my-app-mysql-service", 'port': 33060, "user": "root", "password": "root"}
dbSchema = 'crimes'
slidingDuration = '1 minute'


# Create a spark session
spark = SparkSession.builder \
    .appName("Structured Streaming").getOrCreate()

# Set log level
spark.sparkContext.setLogLevel('ERROR')

# Read messages from Kafka
kafkaMessages = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "my-cluster-kafka-bootstrap:9092").option("subscribe", "big_data_demo").option("startingOffsets", "earliest").load()  
    

# Define schema of crime data
crimeSchema = StructType() \
    .add("id", IntegerType()) \
    .add("CaseNumber", StringType()) \
    .add("Date", DateType()) \
    .add("Block", StringType()) \
    .add("IUCR", IntegerType()) \
    .add("PrimaryType", StringType()) \
    .add("Description", StringType()) \
    .add("LocationDescription", StringType()) \
    .add("Arrest", BooleanType()) \
    .add("Domestic", StringType()) \
    .add("Beat", StringType()) \
    .add("District", StringType()) \
    .add("Ward", StringType()) \
    .add("CommunityArea", StringType()) \
    .add("FBICode", IntegerType()) \
    .add("XCoordinate", IntegerType()) \
    .add("YCoordinate", IntegerType()) \
    .add("YEAR", IntegerType()) \
    .add("UpdatedOn", StringType()) \
    .add("Latitude", IntegerType()) \
    .add("Longitude", IntegerType()) \
    .add("LOCATION", StringType())



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
    .withColumnRenamed('json.CaseNumber', 'casenumber') \
    .withColumnRenamed('json.Date', 'date') \
    .withColumnRenamed('json.Block', 'block') \
    .withColumnRenamed('json.IUCR', 'iucr') \
    .withColumnRenamed('json.PrimaryType', 'primarytype') \
    .withColumnRenamed('json.Description', 'description') \
    .withColumnRenamed('json.LocationDescription', 'locationdescription') \
    .withColumnRenamed('json.Arrest', 'arrest') \
    .withColumnRenamed('json.Domestic', 'domestic') \
    .withColumnRenamed('json.Beat', 'beat') \
    .withColumnRenamed('json.District', 'district') \
    .withColumnRenamed('json.Ward', 'ward') \
    .withColumnRenamed('json.CommunityArea', 'communityarea') \
    .withColumnRenamed('json.FBICode', 'fbicode') \
    .withColumnRenamed('json.XCoordinate', 'xcoordinate') \
    .withColumnRenamed('json.YCoordinate', 'ycoordinate') \
    .withColumnRenamed('json.YEAR', 'year') \
    .withColumnRenamed('json.UpdatedOn', 'updatedon') \
    .withColumnRenamed('json.Latitude', 'latitude') \
    .withColumnRenamed('json.Longitude', 'longitude') \
    .withColumnRenamed('json.LOCATION', 'location') \
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

#print(crimeMessages)

crimesperyear = crimeMessages.groupBy(
    column("year")
).count().withColumnRenamed('count', 'yearcount')

#print(crimesperyear.show())


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
        session.sql("USE crimes").execute()  # Spark DataFrame mit Verhaftungen nutzen


        for row in iterator:
                   
            # Run upsert (insert or update existing)
            sql = session.sql("INSERT INTO Crime_Year "
                              "(YEAR, COUNT) VALUES (?, ?) "
                              "ON DUPLICATE KEY UPDATE COUNT=?")
            sql.bind(row.year, row.yearcount, row.yearcount).execute()

        session.close()

    # Perform batch UPSERTS per data partition
    print(batchDataframe)
    batchDataframe.foreachPartition(save_to_db)
    print('Query Done')

# Example Part 7


dbInsertStream = crimesperyear.writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .foreachBatch(saveToDatabase) \
    .start()


# Wait for termination
spark.streams.awaitAnyTermination()

