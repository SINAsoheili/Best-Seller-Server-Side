from flask import Flask, request, abort
from database_config import TABLE_SELLER, DB_SERVER, DB_USER, DB_PASSWD, DB_NAME, TABLE_SHOP
import mysql.connector

app = Flask(__name__)

def connect_to_database():
    database = mysql.connector.connect(host=DB_SERVER, user=DB_USER, password=DB_PASSWD, database=DB_NAME)
    if database.is_connected:
        return database
    else:
        return None

@app.route('/register_seller' , methods=['GET'])
def registar_seller():
    name = request.args.get('name', None)
    last_name = request.args.get('last_name', None)
    phone = request.args.get('phone', None)
    passwd = request.args.get('passwd', None)

    if name==None or last_name==None or phone==None or passwd==None:
        abort(400)

    #TODO: chek phone is valid
    #TODO: encrypt passwd

    cmd = f"INSERT INTO {TABLE_SELLER} (name, last_name, phone, passwd) VALUES (%s, %s, %s, %s)"
    params = (name, last_name, phone, passwd)

    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    cursor.execute(cmd , params)
    try:
        db.commit()
        
        cmd = f"SELECT * FROM {TABLE_SELLER} WHERE phone={phone}"
        cursor.execute(cmd)
        result = cursor.fetchall()
        if len(result) != 1:
            abort(500)
        else :
            id = result[0][0]
            return {"id":id, "name":name , "last_name":last_name , "phone":phone , "passwd":passwd}
            
    except e as Exception:
        abort(503)    

@app.route('/register_shop' , methods=['GET'])
def registar_shop():
    name = request.args.get('name', None)
    address = request.args.get('address', None)
    latitude = request.args.get('latitude', None)
    longitude = request.args.get('longitude', None)
    id_seller = request.args.get('id_seller', None)
    id_category = request.args.get('id_category', None)
    #optional 
    site = request.args.get('site', None)
    description = request.args.get('description', None)
    phone = request.args.get('phone', None)

    if name==None or address==None or latitude==None or longitude==None or id_seller==None or id_category==None :
        abort(400)

    cmd = f"INSERT INTO {TABLE_SHOP} (name, address, latitude, longitude, id_seller, id_category, site, description, phone ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (name, address, latitude, longitude, id_seller, id_category, site, description, phone)
    
    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    cursor.execute(cmd , params)
    try:
        db.commit()
        cmd = f"SELECT * FROM {TABLE_SHOP} WHERE id_seller={id_seller}"
        cursor.execute(cmd)
        result = cursor.fetchall()
        if len(result) != 1:
            abort(500)
        else :
            id = result[0][0]
            return {"id":id, "name":name, "address":address, "latitude":latitude, "longitude":longitude, "id_seller":id_seller, "id_category":id_category, "site":site , "description":description, "phone":phone}
            
    except e as Exception:
        abort(503)    

if __name__ == "__main__":
    app.run("localhost" , 5000 , True)