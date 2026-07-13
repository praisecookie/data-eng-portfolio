from confluent_kafka import Consumer, KafkaError
import json

# 1. Configure the Consumer to connect to our local Docker cluster
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'lagos_analytics_group',  # Identifies this consumer group
    # Start reading from the beginning of the queue
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

# 2. Subscribe to our specific ride-share GPS topic
topic = 'driver_gps_data'
consumer.subscribe([topic])

print("📥 Consumer Started. Waiting for live GPS data pings...")

# 3. Infinite loop to constantly poll Kafka for new messages
try:
    while True:
        # Check for new data every 1.0 second
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Reached the end of the partition queue
                continue
            else:
                print(f"❌ Error: {msg.error()}")
                break

        # Decode the raw byte message back into a JSON string, then a dictionary
        raw_data = msg.value().decode('utf-8')
        gps_event = json.loads(raw_data)

        # Print the data out to prove we caught it!
        print(
            f"✅ Consumer Retrieved -> Driver #{gps_event['driver_id']} is at Lat: {gps_event['lat']}, Lon: {gps_event['lon']}")

except KeyboardInterrupt:
    print("\n🛑 Consumer stopped by Data Engineer.")
finally:
    # Close the connection cleanly down
    consumer.close()
