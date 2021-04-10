from flask import Flask, request, abort
from database_config import DB_SERVER, DB_USER, DB_PASSWD, DB_NAME, TABLE_SHOP, TABLE_SELLER, TABLE_USER, TABLE_DISCOUNT, SALT
import mysql.connector
import hashlib

app = Flask(__name__)

def connect_to_database():
    database = mysql.connector.connect(host=DB_SERVER, user=DB_USER, password=DB_PASSWD, database=DB_NAME)
    if database.is_connected:
        return database
    else:
        return None

def passwd_encrypt(passwd):
    passwd = passwd+SALT
    return hashlib.sha256(passwd.encode()).hexdigest()

@app.route('/register_seller' , methods=['GET'])
def registar_seller():
    name = request.args.get('name', None)
    last_name = request.args.get('last_name', None)
    phone = request.args.get('phone', None)
    passwd = request.args.get('passwd', None)

    if name==None or last_name==None or phone==None or passwd==None:
        abort(400)

    #TODO: chek phone is valid

    passwd = passwd_encrypt(passwd)

    cmd = f"INSERT INTO {TABLE_SELLER} (name, last_name, phone, passwd) VALUES (%s, %s, %s, %s)"
    params = (name, last_name, phone, passwd)

    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    
    try:
        cursor.execute(cmd , params)
        db.commit()
        
        cmd = f"SELECT * FROM {TABLE_SELLER} WHERE phone={phone}"
        cursor.execute(cmd)
        result = cursor.fetchone()
        id = result[0]
        return {"id":id, "name":name , "last_name":last_name , "phone":phone}
            
    except :
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
    try:
        cursor.execute(cmd , params)
        db.commit()
        cmd = f"SELECT * FROM {TABLE_SHOP} WHERE id_seller={id_seller}"
        cursor.execute(cmd)
        result = cursor.fetchone()
        id = result[0]
        return {"id":id, "name":name, "address":address, "latitude":latitude, "longitude":longitude, "id_seller":id_seller, "id_category":id_category, "site":site , "description":description, "phone":phone}
            
    except:
        abort(503)    

@app.route('/register_user' , methods=['GET'])
def registar_user():
    name = request.args.get('name', None)
    last_name = request.args.get('last_name', None)
    phone = request.args.get('phone', None)
    passwd = request.args.get('passwd', None)

    if name==None or last_name==None or phone==None or passwd==None:
        abort(400)

    #TODO: chek phone is valid
     
    passwd = passwd_encrypt(passwd)

    cmd = f"INSERT INTO {TABLE_USER} (name, last_name, phone, passwd) VALUES (%s, %s, %s, %s)"
    params = (name, last_name, phone, passwd)

    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    try:
        cursor.execute(cmd , params)
        db.commit()
        
        cmd = f"SELECT * FROM {TABLE_USER} WHERE phone={phone}"
        cursor.execute(cmd)
        result = cursor.fetchone()
        id = result[0]
        return {"id":id, "name":name , "last_name":last_name , "phone":phone}
            
    except :
        abort(503) 

@app.route('/get_shop_info' , methods=['GET'])
def get_shop_info():
    id = request.args.get('shop_id', None)

    if id==None :
        abort(400)
    
    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    cmd = f"SELECT * FROM {TABLE_SHOP} WHERE id={id}"
    cursor.execute(cmd)
    result = cursor.fetchall()
    if len(result) == 0:
        return {"find":False , "shop":{}}
    elif len(result) == 1:
        (id, name, address, latitude, longitude, phone, site, description, id_seller, id_category) = result[0]
        return {"find":True , "shop":{"id":id, "name":name, "address":address, "latitude":latitude, "longitude":longitude, "id_seller":id_seller, "id_category":id_category, "site":site , "description":description, "phone":phone}}
    else:
        abort(500)

@app.route('/get_seller_info' , methods=['GET'])
def get_seller_info():
    id = request.args.get('seller_id', None)

    if id==None :
        abort(400)
    
    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    cmd = f"SELECT * FROM {TABLE_SELLER} WHERE id={id}"
    cursor.execute(cmd)
    result = cursor.fetchall()
    if len(result) == 0:
        return {"find":False , "seller":{}}
    elif len(result) == 1:
        (id, name, last_name, phone, *_) = result[0]
        return {"find":True , "seller":{"id":id, "name":name, "last_name":last_name , "phone":phone}}
    else:
        abort(500)

@app.route('/get_user_info' , methods=['GET'])
def get_user_info():
    id = request.args.get('user_id', None)

    if id==None :
        abort(400)
    
    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    cmd = f"SELECT * FROM {TABLE_USER} WHERE id={id}"
    cursor.execute(cmd)
    result = cursor.fetchall()
    if len(result) == 0:
        return {"find":False , "user":{}}
    elif len(result) == 1:
        (id, name, last_name, phone, *_) = result[0]
        return {"find":True , "user":{"id":id, "name":name, "last_name":last_name , "phone":phone}}
    else:
        abort(500)












@app.route('/register_discount' , methods=['GET'])
def registar_discount():
    name = request.args.get('name', None)
    amount = request.args.get('amount', None)
    id_shop = request.args.get('id_shop', None)

    if name==None or amount==None or id_shop==None:
        abort(400)

    cmd = f"INSERT INTO {TABLE_DISCOUNT} (id_shop, name, amount) VALUES (%s, %s, %s)"
    params = (id_shop, name, amount)

    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()
    try:
        cursor.execute(cmd , params)
        db.commit()
        
        cmd = f"SELECT * FROM {TABLE_DISCOUNT} WHERE id_shop={id_shop}"
        cursor.execute(cmd)
        result = cursor.fetchone()
        if result==None:
            return {"discount_registered":False}
        else:
            return {"discount_registered":True}        
    except :
        abort(503) 














if __name__ == "__main__":
    app.run("localhost" , 5000 , True)