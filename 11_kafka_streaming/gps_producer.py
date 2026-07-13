import json
import time
import random
from confluent_kafka import Producer

# 1. Configure the Kafka Producer to talk to our local Docker server
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

# A 'Topic' is the specific channel we are sending data to
topic = 'driver_gps_data'

print("🚕 Starting Ride-Share GPS Stream...")

# 2. Infinite Loop to Simulate Live Streaming
try:
    while True:
        # Generate fake driver data in Lagos, Nigeria
        driver_id = random.randint(1000, 9999)
        latitude = round(random.uniform(6.4, 6.6), 5)
        longitude = round(random.uniform(3.3, 3.5), 5)

        payload = {
            "driver_id": driver_id,
            "lat": latitude,
            "lon": longitude,
            "status": "driving"
        }

        # Convert the dictionary to a JSON string, then encode it to bytes
        json_payload = json.dumps(payload).encode('utf-8')

        # 3. Send to Kafka!
        producer.produce(topic, value=json_payload)
        producer.flush()  # Force the message out immediately

        print(f"📡 Sent to Kafka: {payload}")

        # Wait 1 second before sending the next ping
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Stream stopped by Data Engineer.")
