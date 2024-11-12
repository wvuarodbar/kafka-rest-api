
import requests
import json

# Kafka REST Proxy URL
url = 'http://localhost:8082/topics/test-topic'

# Message to send
message = {
    "records": [
        {"value": {"key": "value", "message": "Hello from Python!"}}
    ]
}

# Headers
headers = {
    'Content-Type': 'application/vnd.kafka.json.v2+json'
}

# Send the request
response = requests.post(url, headers=headers, data=json.dumps(message))

# Print the response
print(response.status_code)
print(response.text)
