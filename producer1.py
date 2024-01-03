from pykafka import KafkaClient
import json
import time

#READ COORDINATES FROM GEOJSON
input_file = open('./data/bus1.json')
json_array = json.load(input_file)
coordinates = json_array['data']

#KAFKA PRODUCER
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['bus_topic']
producer = topic.get_sync_producer()

#CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}
data['service'] = 'HanoiBus1'


def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = i
        data['datetime'] = coordinates[i]['datetime']
        data['unit'] = coordinates[i]['unit']
        data['latitude'] = coordinates[i]['coordinates'][1]
        data['longitude'] = coordinates[i]['coordinates'][0]
        data['fuel'] = coordinates[i]['fuel']
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)

        #if bus reaches last coordinate, start from beginning
        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)