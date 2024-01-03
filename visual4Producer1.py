import matplotlib.pyplot as plt
import pymongo  
import datetime
import time

# Kết nối với MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
database = client["bigDataProject"]
collection = database["bus_data"]

plt.ion()  # Bật chế độ interactive của matplotlib

fig, ax = plt.subplots()
line, = ax.plot([], [])  # Khởi tạo đường line trên biểu đồ

# truy vấn cho xe 1
query = {"unit": 1}

while True:
    # Lấy dữ liệu từ MongoDB (ví dụ: 'datetime' và 'value' là các trường trong collection)
    cursor = collection.find(query).sort('_id', -1).limit(10)  # Lấy 10 dòng dữ liệu mới nhất

    timestamps = []
    values = []

    for document in cursor:
        timestamps.append(document['datetime'])
        values.append(document['fuel'])

    # Chuyển đổi timestamps sang đối tượng datetime
    converted_timestamps = [datetime.datetime.strptime(ts , '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    # Cập nhật dữ liệu trên biểu đồ
    line.set_xdata(converted_timestamps)
    line.set_ydata(values)

    ax.relim()
    ax.autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()

    time.sleep(2)  # Đợi 2 giây trước khi cập nhật lại biểu đồ
