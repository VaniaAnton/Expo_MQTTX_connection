import paho.mqtt.client as mqtt
from imdb import imdb_search
import json
import webbrowser

# Check MQTT version
import paho.mqtt.client as mqtt

# Configuration
MQTT_TOPIC_SUBSCRIBE = "Movies/test"
MQTT_TOPIC_PUBLISH = "Movies/content"
MQTT_BROKER = "172.20.10.2"  # My VirtualBox VM IP address
MQTT_PORT = 1883

# Decide which API version to use based on the installed version
if hasattr(mqtt.Client, 'CallbackAPIVersion'):
    # For version 2.x
    print("Using MQTT Client with VERSION2 callback API")
    
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"Connected to MQTT Broker: {MQTT_BROKER}")
            client.subscribe(MQTT_TOPIC_SUBSCRIBE)
            print(f"Subscribed to {MQTT_TOPIC_SUBSCRIBE}")
        else:
            print(f"Failed to connect to MQTT Broker. Return code: {rc}")
    
    def on_message(client, userdata, message, properties=None):
        try:
            msg = message.payload.decode("utf-8").strip()
            print(f"Received message: {msg}")
            
            if len(msg) > 0:
                print(f"Searching IMDb for: {msg}")
                
                # Search for the movie on IMDb
                content = imdb_search(msg)
                
                # Convert to JSON for MQTT transmission
                json_content = json.dumps(content)
                
                # Publish result back to MQTT
                client.publish(MQTT_TOPIC_PUBLISH, json_content)
                print(f"Published movie data to {MQTT_TOPIC_PUBLISH}")
                
                # Open the URL in a browser window (fulfilling assignment requirement)
                if 'url_content' in content:
                    print(f"Opening URL: {content['url_content']}")
                    webbrowser.open(content['url_content'])
        except Exception as e:
            print(f"Error processing message: {e}")
    
    # Create client with VERSION2 API
    from paho.mqtt.client import CallbackAPIVersion
    client = mqtt.Client(
        client_id="Sniffer",
        callback_api_version=CallbackAPIVersion.VERSION2
    )
else:
    # For version 1.x
    print("Using MQTT Client with VERSION1 callback API")
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker: {MQTT_BROKER}")
            client.subscribe(MQTT_TOPIC_SUBSCRIBE)
            print(f"Subscribed to {MQTT_TOPIC_SUBSCRIBE}")
        else:
            print(f"Failed to connect to MQTT Broker. Return code: {rc}")
    
    def on_message(client, userdata, message):
        try:
            msg = message.payload.decode("utf-8").strip()
            print(f"Received message: {msg}")
            
            if len(msg) > 0:
                print(f"Searching IMDb for: {msg}")
                
                # Search for the movie on IMDb
                content = imdb_search(msg)
                
                # Convert to JSON for MQTT transmission
                json_content = json.dumps(content)
                
                # Publish result back to MQTT
                client.publish(MQTT_TOPIC_PUBLISH, json_content)
                print(f"Published movie data to {MQTT_TOPIC_PUBLISH}")
                
                # Open the URL in a browser window (fulfilling assignment requirement)
                if 'url_content' in content:
                    print(f"Opening URL: {content['url_content']}")
                    webbrowser.open(content['url_content'])
        except Exception as e:
            print(f"Error processing message: {e}")
    
    # Create client with VERSION1 API
    client = mqtt.Client("Sniffer")

def main():
    # Set callbacks based on the version-specific functions defined above
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Connect to broker
    try:
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Start network loop
        print("Starting MQTT loop... Press Ctrl+C to exit")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        client.disconnect()
        print("Disconnected. Exiting...")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

if __name__ == "__main__":
    main()