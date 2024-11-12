"""
from elasticsearch import Elasticsearch
from datetime import datetime
import random
import time

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define the number of topics (indices)
num_topics = 18

# Create indices for each topic if they don't exist
for i in range(1, num_topics + 1):
    index_name = f"topic_{i}"
    if not es.indices.exists(index=index_name):
        # Define index settings and mapping for geospatial data
        es.indices.create(
            index=index_name,
            body={
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "user_id": {"type": "integer"},
                        "message": {"type": "text"},
                        "status": {"type": "keyword"},
                        "location": {"type": "geo_point"}  # Geospatial field
                    }
                }
            }
        )

# Function to generate a random message with geospatial data
def generate_message():
    return {
        "timestamp": datetime.now().isoformat(),
        "user_id": random.randint(1, 100),
        "message": f"Test message {random.randint(1, 1000)}",
        "status": random.choice(["sent", "received", "error"]),
        "location": {  # Random geospatial data
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6)
        }
    }

# Function to send messages to multiple indices
def send_messages(es, num_topics, messages_per_index=10, delay=1):
    for topic in range(1, num_topics + 1):
        index_name = f"topic_{topic}"
        for _ in range(messages_per_index):
            # Generate a message
            message = generate_message()
            
            # Index the message in the specified topic index
            response = es.index(index=index_name, document=message)
            print(f"Indexed document ID {response['_id']} in {index_name} - {message}")
            
            # Optional delay to simulate real-time data ingestion
            time.sleep(delay)

# Function to perform a multi-search query across all indices
def multi_search(es, num_topics):
    # Define queries for each index in the multi-search
    body = []
    for topic in range(1, num_topics + 1):
        index_name = f"topic_{topic}"
        # Add a search for each index
        body.append({"index": index_name})
        body.append({"query": {"match_all": {}}})  # Adjust query as needed

    # Execute the multi-search request
    response = es.msearch(body=body)
    for idx, res in enumerate(response['responses']):
        print(f"Results from topic_{(idx // 2) + 1}:")
        for hit in res['hits']['hits']:
            print(hit["_source"])

# Send messages to all topics
send_messages(es, num_topics=num_topics, messages_per_index=10, delay=0.5)

# Perform a multi-search across all indices
multi_search(es, num_topics=num_topics)
"""
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests
import json
import random

# Function to generate a random date within a given range
def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_time = start_date + timedelta(days=random_days, hours=random.randint(0, 23),
                                         minutes=random.randint(0, 59), seconds=random.randint(0, 59))
    return random_time.isoformat() + "Z"

# Function to generate a CoT message and convert it into JSON for Elasticsearch
def generate_cot_message(index_number, start_date, end_date):
    current_time = generate_random_date(start_date, end_date)
    
    # Create a CoT message (XML structure)
    cot = ET.Element("CoT", xmlns="http://www.opengis.net/cot/1.0", version="2.0")
    
    # Create the <meta> element with relevant data
    meta = ET.SubElement(cot, "meta", version="2.0", type="a-f-G-U-C", time=current_time,
                         uid=f"random-uid-{random.randint(1000, 9999)}", relevance=random.choice(["High", "Medium", "Low"]))
    
    # Create the <point> element with geospatial data
    point = ET.SubElement(cot, "point", lat=str(37.7749 + random.uniform(-0.5, 0.5)), 
                          lon=str(-122.4194 + random.uniform(-0.5, 0.5)), hae=str(random.randint(50, 300)),
                          ce=str(random.randint(10, 30)), le=str(random.randint(10, 30)))
    
    # Create <detail> element and add child elements
    detail = ET.SubElement(cot, "detail")
    ET.SubElement(detail, "contact", callsign=f"Vehicle-{index_number}", operator=f"Operator {random.choice(['A', 'B', 'C'])}")
    ET.SubElement(detail, "type", x="TacName").text = f"VehicleType-{index_number}"
    ET.SubElement(detail, "status", x="Mode").text = random.choice(["Moving", "Stopped", "Idle"])
    ET.SubElement(detail, "status", x="Speed").text = str(random.randint(0, 80))
    ET.SubElement(detail, "status", x="Heading").text = str(random.randint(0, 360))
    ET.SubElement(detail, "status", x="FuelLevel").text = str(random.randint(10, 100))
    ET.SubElement(detail, "status", x="EngineStatus").text = random.choice(["On", "Off"])
    ET.SubElement(detail, "time", x="LastMaintenance").text = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    ET.SubElement(detail, "location", x="CurrentLocation").text = f"Location-{random.randint(1, 10)}"
    ET.SubElement(detail, "mission", x="OperationName").text = f"Operation {random.choice(['Alpha', 'Bravo', 'Charlie'])}"
    ET.SubElement(detail, "group", x="TacticalGroup").text = f"Tactical Group {random.randint(1, 5)}"

    # Parse the XML structure and extract data to JSON format
    cot_json = {
        "timestamp": current_time,
        "meta": {
            "uid": meta.get("uid"),
            "version": meta.get("version"),
            "type": meta.get("type"),
            "time": meta.get("time"),
            "relevance": meta.get("relevance"),
        },
        "point": {
            "lat": float(point.get("lat")),
            "lon": float(point.get("lon")),
            "hae": int(point.get("hae")),
            "ce": int(point.get("ce")),
            "le": int(point.get("le"))
        },
        "detail": {
            "contact": {
                "callsign": detail.find("contact").get("callsign"),
                "operator": detail.find("contact").get("operator")
            },
            "type": {
                "tac_name": detail.find("type").text
            },
            "status": {
                "mode": detail.find("status[@x='Mode']").text,
                "speed": int(detail.find("status[@x='Speed']").text),
                "heading": int(detail.find("status[@x='Heading']").text),
                "fuel_level": int(detail.find("status[@x='FuelLevel']").text),
                "engine_status": detail.find("status[@x='EngineStatus']").text
            },
            "time": {
                "last_maintenance": detail.find("time[@x='LastMaintenance']").text
            },
            "location": {
                "current_location": detail.find("location[@x='CurrentLocation']").text
            },
            "mission": {
                "operation_name": detail.find("mission[@x='OperationName']").text
            },
            "group": {
                "tactical_group": detail.find("group[@x='TacticalGroup']").text
            }
        }
    }

    return cot_json

# Function to send CoT message to Elasticsearch
def send_cot_message_to_es(cot_message, index_name):
    # Elasticsearch server URL (adjust the URL if needed)
    es_url = f"http://localhost:9200/{index_name}/_doc"
    
    # Headers for the HTTP request (Elasticsearch expects JSON)
    headers = {"Content-Type": "application/json"}
    
    # Send the CoT message to Elasticsearch via HTTP POST request
    response = requests.post(es_url, json=cot_message, headers=headers)
    
    # Check if the message was successfully sent
    if response.status_code == 201:
        print(f"CoT message sent successfully to Elasticsearch ({index_name})!")
    else:
        print(f"Failed to send CoT message to Elasticsearch ({index_name}). Status code: {response.status_code}")
        print(response.text)

# Main function to generate and send 100 CoT messages to each of 18 indexes
def send_multiple_cot_messages():
    # Define the start and end date for the timeframe
    start_date = datetime(2024, 11, 4)
    end_date = datetime(2024, 11, 10)
    
    # Loop over 18 indexes
    for index_number in range(1, 19):
        index_name = f"cot-index-{index_number}"
        
        # Send 100 CoT messages to each index
        for _ in range(100):
            cot_message = generate_cot_message(index_number, start_date, end_date)
            send_cot_message_to_es(cot_message, index_name)

if __name__ == "__main__":
    send_multiple_cot_messages()
