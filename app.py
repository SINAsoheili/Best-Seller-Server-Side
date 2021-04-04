from flask import Flask
from database_config import DB_SERVER , DB_USER , DB_PASSWD , DB_NAME
import mysql.connector

app = Flask(__name__)

database = mysql.connector.connect(host=DB_SERVER, user=DB_USER, password=DB_PASSWD, database=DB_NAME)

if __name__ == "__main__":
    app.run("localhost" , 5000 , True)