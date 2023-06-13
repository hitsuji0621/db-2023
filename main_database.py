from flask import Flask
import mysql.connector

app = Flask(__name__)

# 資料庫連接設定
config = {
    'host': '140.122.184.125',
    'port': 3307,
    'user': 'team7',  # 請將 xx 替換為您的組別編號
    'password': 'uU8ActkvqhZI9saa',
    'database': 'team7',  # 請將 your_database_name 替換為您的資料庫名稱
    'charset': 'utf8',
}

# 路由示例
@app.route('/')
def index():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # 關閉資料庫連接
    cursor.close()
    connection.close()

    return "連上啦"

if __name__ == '__main__':
    app.run()
