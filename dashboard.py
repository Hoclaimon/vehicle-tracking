import dash
import dash_core_components as dcc
import dash_html_components as html
import pymongo

# Tạo kết nối với MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
database = client["bigDataProject"]
collection = database["bus_data"]

# Tạo vòng lặp để đọc dữ liệu từ MongoDB
def update_data():
    # Đọc dữ liệu mới nhất từ MongoDB
    new_data = collection.find().sort("key").sort("unit")

    # Cập nhật dữ liệu cho biểu đồ
    try:
        doc = new_data.next()  # Lấy tài liệu đầu tiên
        data = [{"x": doc["datetime"], "y": doc["fuel"]}]
    except StopIteration:
        data = []
        
    return data

# Tạo biểu đồ
app = dash.Dash()
app.layout = html.Div(children=[
    dcc.Graph(
        id="my-graph",
        figure={
            "data": [
                {
                    "x": update_data()[0]['x'],
                    "y": update_data()[0]['y'],
                    "type": "line"
                }
            ],
            "layout": {
                "title": "Biểu đồ thời gian thực theo nhiên liệu"
            }
        }
    )
])

# Chạy ứng dụng
app.run_server(debug=True)
