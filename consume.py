import requests
import json

# Kafka REST Proxy URL for creating a consumer
create_consumer_url = 'http://localhost:8082/consumers/my-consumer-group'

# Consumer configuration
consumer_config = {
    "name": "my-consumer-4",
    "format": "json",
    "auto.offset.reset": "earliest"
}

# Corrected Content-Type header for Kafka REST Proxy
headers = {
    'Content-Type': 'application/vnd.kafka.json.v2+json'
}

def create_consumer():
    try:
        # Convert the consumer_config dictionary to a JSON string
        json_data = json.dumps(consumer_config)

        # Send the POST request to create a consumer
        response = requests.post(create_consumer_url, data=json_data, headers=headers)

        if response.status_code == 200:
            print("Consumer created successfully.")
            consumer_info = response.json()  # Getting the consumer details from the response
            print(f"Consumer info: {json.dumps(consumer_info, indent=2)}")  # Pretty print consumer info
            return consumer_info
        else:
            print(f"Failed to create consumer. Status Code: {response.status_code}")
            print(f"Error Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while creating the consumer: {e}")
        return None


def subscribe_consumer(consumer_info, topic_name):
    subscribe_url = f'http://localhost:8082/consumers/my-consumer-group/instances/my-consumer-4/topics/{topic_name}'

    try:
        # Send the request to subscribe the consumer to a topic
        response = requests.post(subscribe_url, headers=headers)

        if response.status_code == 200:
            print(f"Consumer subscribed to topic: {topic_name}")
        else:
            print(f"Failed to subscribe to topic. Status Code: {response.status_code}")
            print(f"Error Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error while subscribing to the topic: {e}")


def consume_messages():
    consume_url = f'http://localhost:8082/consumers/my-consumer-group/instances/my-consumer-4/records'

    try:
        # Send the GET request to consume messages
        response = requests.get(consume_url, headers=headers)

        if response.status_code == 200:
            messages = response.json()  # Assuming the messages are in JSON format
            print(f"Consumed messages: {json.dumps(messages, indent=2)}")
        else:
            print(f"Failed to consume messages. Status Code: {response.status_code}")
            print(f"Error Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error while consuming messages: {e}")


def commit_offsets(topic_name, partition, offset):
    commit_url = f'http://localhost:8082/consumers/my-consumer-group/instances/my-consumer-4/offsets'

    offsets = {
        "partitions": [
            {
                "topic": topic_name,
                "partition": partition,  # Replace with your actual partition number
                "offset": offset  # Replace with the offset you want to commit
            }
        ]
    }

    try:
        # Send the POST request to commit offsets
        response = requests.post(commit_url, data=json.dumps(offsets), headers=headers)

        if response.status_code == 200:
            print("Offsets committed successfully.")
        else:
            print(f"Failed to commit offsets. Status Code: {response.status_code}")
            print(f"Error Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error while committing offsets: {e}")


def shutdown_consumer(consumer_info):
    shutdown_url = f'http://localhost:8082/consumers/my-consumer-group/instances/my-consumer-4'

    try:
        # Send the DELETE request to shut down the consumer
        response = requests.delete(shutdown_url, headers=headers)

        if response.status_code == 200:
            print("Consumer shut down successfully.")
        else:
            print(f"Failed to shut down consumer. Status Code: {response.status_code}")
            print(f"Error Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error while shutting down the consumer: {e}")


def main():
    consumer_info = create_consumer()
    if not consumer_info:
        return

    topic_name = 'test-topic'  # Replace with your actual topic name
    subscribe_consumer(consumer_info, topic_name)

    # Consume messages
    consume_messages()

    # Example of committing offsets (adjust partition and offset)
    commit_offsets(topic_name, partition=0, offset=100)

    # Shutdown the consumer once done
    shutdown_consumer(consumer_info)


if __name__ == '__main__':
    main()
