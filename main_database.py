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
    #
    # # 讀取 SQL 檔案
    # with open('final.sql', 'r') as file:
    #     sql_statements = file.read()
    #
    # # 以分號為分隔符號拆分指令
    # statements = sql_statements.split(';')
    #
    # # 執行每個 SQL 指令
    # for statement in statements:
    #     if statement.strip() != '':
    #         cursor.execute(statement)
    # 提交事務
    connection.commit()

    # 關閉資料庫連接
    cursor.close()
    connection.close()

    return "DDL 已匯入到資料庫"

if __name__ == '__main__':
    app.run()
