import confluent_kafka
import pymongo
import json

# Khởi tạo một đối tượng consumer Kafka
consumer = confluent_kafka.Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id" : "unit"
})

# Khởi tạo một đối tượng collection MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
database = client["bigDataProject"]
collection = database.get_collection("bus_data")

# Hàm xử lý các bản ghi Kafka
def handle_record(record):
    # Lấy giá trị của bản ghi
    value = json.loads(record.value())

    # Lưu giá trị vào MongoDB
    collection.insert_one(value)

# Đăng ký lắng nghe topic Kafka
consumer.subscribe(["bus_topic"])

# Lặp lại không ngừng để lắng nghe các bản ghi từ topic Kafka
while True:
    # Đọc một bản ghi từ Kafka
    record = consumer.poll(0)

    # Nếu có bản ghi mới, hãy xử lý nó
    if record:
        handle_record(record)




# collection.drop()