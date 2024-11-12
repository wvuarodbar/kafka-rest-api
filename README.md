docker-compuse up -d

run python kafka-rest.py
run python kafka-consumer.py

you will have to create the index in kibana dev tools by using:
PUT /test-index
{
  "mappings": {
    "properties": {
      "key": {
        "type": "text"
      },
      "message": {
        "type": "text"
      }
    }
  }
}

run docker logs -f devnifi
# get the username and password just scroll up or search to find it

# goto localhost:8443/nifi
#login

#Processor top left corner
insert consumekafkarecord_1_0

use the docker networks kafka ip address
Topic Name "your topic name" <- test-topic
Topic Name Format - names
Record Reader JSON Tree Reader
        -Json TREE READER Config
            -schema access strategy = infer schema
            - everything else stays no value set

record writer JSONRECORDSETWRITER
        - config
                -Do not write schema
                - inhereit record schema
                - pretty print True 
                - never suppress null values
                - output grouping Array
                - compression format = None
Honor transactions True
security protocol PLAINTEXT
Group ID = "your group id" <- our case it is test-group
offset reset = latest


Processor EvaluateJsonPath
Destination - flowfile-Content
return type auto-detect
path not found behavior ignore
null value representation = empty string
add property: Propert name = $ Value = json

Processor PutElasticRecord
Index operation - index
Index - "your index"
Client Service = ElasticSearchClientServiceImpl
    - config settings 
        - http host = http://elasticsearch:9200
        - keep all others as default
        - 5000
        -60000
        -60000
        -UTF-8
        -Never Suppress Null/Empty

Record Reader = JsonTreeReader

BatchSize = 100

The end result will be the record will be sent over this config 
and be placed in elastic search just check the localhost:9200/"your index"/_search
to check on if it is running.
