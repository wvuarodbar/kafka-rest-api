import requests
import json

# Kafka REST Proxy URL for creating a consumer
create_consumer_url = 'http://localhost:8082/consumers/my-consumer-group'

# Consumer configuration
consumer_config = {
    "name": "my-consumer",
    "format": "json",
    "auto.offset.reset": "earliest"
}

# Convert the consumer_config dictionary to a JSON string
json_data = json.dumps(consumer_config)

# Corrected Content-Type header for Kafka REST Proxy
headers = {
    'Content-Type': 'application/vnd.kafka.json.v2+json'
}

try:
    # Send the POST request to create a consumer
    response = requests.post(create_consumer_url, data=json_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Consumer created successfully.")
        consumer_info = response.json()  # Getting the consumer details from the response
        print(f"Consumer info: {json.dumps(consumer_info, indent=2)}")  # Pretty print consumer info
    else:
        # Print the error if status code is not 200
        print(f"Failed to create consumer. Status Code: {response.status_code}")
        print(f"Error Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    # Handle any connection errors or request exceptions
    print(f"An error occurred while sending the request: {e}")
