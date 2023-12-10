import paho.mqtt.client as mqtt
import time

class MqttSubscriber:
    def __init__(self, client_id, broker_address, topic, topic2, topic3):
        self.client_id = client_id
        self.broker_address = broker_address
        self.topic = topic
        self.topic2 = topic2
        self.topic3 = topic3

        self.message01 = None

        # Create an MQTT client
        self.client = mqtt.Client(client_id=self.client_id)

        # Set up callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # Subscribe to the specified topic
        client.subscribe(self.topic)
        client.subscribe(self.topic2)
        client.subscribe(self.topic3)

    def on_message(self, client, userdata, msg):
        # Handle incoming message
        self.message01 = msg.payload.decode()
        print(f"Received message on topic '{msg.topic}': {self.message01}")

    def process_payload(self):
        if self.message01 == 'Pause':
            print("Pausebutton is activated. Message hold")
        else:
            print("No Pause")

    def run(self):
        # Connect to the MQTT broker
        self.client.connect(self.broker_address, 1883, 60)

        # Start the MQTT client loop in a non-blocking way
        self.client.loop_start()

        try:
            while True:
                # You can add other processing logic here if needed
                self.process_payload()
                # Sleep for a short duration to avoid busy-waiting
                time.sleep(0.1)

        except KeyboardInterrupt:
            # Disconnect the MQTT client on keyboard interrupt
            self.client.disconnect()

if __name__ == "__main__":
    # Instantiate the MqttSubscriber
    mqtt_subscriber = MqttSubscriber(
        client_id="Subscriber01",
        broker_address="broker.hivemq.com",
        topic="In/Lights/Location/UserId/Switch",  # Replace with the topic you want to subscribe to
        topic2="In/Lights/Location/UserId/Pause",
        topic3="In/Lights/Location/UserId/Comments"
    )

    # Run the MQTT subscriber
    mqtt_subscriber.run()
