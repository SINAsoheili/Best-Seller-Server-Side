from flask import Flask, request, abort
from database_config import *
import mysql.connector
import hashlib

app = Flask(__name__)

def passwd_encrypt(passwd):
    passwd = passwd+SALT
    return hashlib.sha256(passwd.encode()).hexdigest()

def connect_to_database():
    database = mysql.connector.connect(host=DB_SERVER, user=DB_USER, password=DB_PASSWD, database=DB_NAME)
    if database.is_connected:
        return database
    else:
        return None

def select_from_db(query):
    db = connect_to_database()
    if db==None:
        abort(500)

    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def delete_from_db(query , params):
    db = connect_to_database()
    if db==None:
        abort(500)

    cursor = db.cursor()
    try:
        cursor.execute(query, params)
        db.commit()
        return True
    except :
        return False

def insert_to_db(query , params):
    db = connect_to_database()
    if db==None:
        abort(500)
    cursor = db.cursor()

    try:
        cursor.execute(query , params)
        db.commit()
        return True
    except :
        return False



@app.route('/get_shop_info' , methods=['GET'])
def get_shop_info():
    id = request.args.get('shop_id', None)

    if id==None :
        abort(400)
    
    query = f"SELECT * FROM {TABLE_SHOP} WHERE {TABLE_SHOP_ID}={id}"

    result = select_from_db(query)
    if len(result) == 1:
        (id, name, address, latitude, longitude, phone, site, description, id_seller, id_category) = result[0]
        return {"find":True , "shop":{"id":id, "name":name, "address":address, "latitude":latitude, "longitude":longitude, "id_seller":id_seller, "id_category":id_category, "site":site , "description":description, "phone":phone}}
    else :
        return {"find":False , "shop":{}}
        
@app.route('/get_seller_info' , methods=['GET'])
def get_seller_info():
    id = request.args.get('seller_id', None)

    if id==None :
        abort(400)

    query = f"SELECT * FROM {TABLE_SELLER} WHERE {TABLE_SELLER_ID}={id}"
    result = select_from_db(query)
        
    if len(result) == 1:
        (id, name, last_name, phone, *_) = result[0]
        return {"find":True , "seller":{"id":id, "name":name, "last_name":last_name , "phone":phone}}
    else:
        return {"find":False , "seller":{}}

@app.route('/get_user_info' , methods=['GET'])
def get_user_info():
    id = request.args.get('user_id', None)

    if id==None :
        abort(400)
    
    query = f"SELECT * FROM {TABLE_USER} WHERE {TABLE_USER_ID}={id}"
    result = select_from_db(query)
        
    if len(result) == 1:
        (id, name, last_name, phone, *_) = result[0]
        return {"find":True , "user":{"id":id, "name":name, "last_name":last_name , "phone":phone}}
    else:
        return {"find":False , "user":{}}



@app.route('/delete_discount' , methods=['GET'])
def delete_discount():
    id_shop = request.args.get('id_shop', None)

    if id_shop==None:
        abort(400)

    query = f"SELECT * FROM {TABLE_DISCOUNT} WHERE {TABLE_DISCOUNT_ID_SHOP}={id_shop}"
    select_result = select_from_db(query)
    if len(select_result) == 0:
        exists = False
    else:
        exists = True

    query = f"DELETE FROM {TABLE_DISCOUNT} WHERE {TABLE_DISCOUNT_ID_SHOP}=%s"
    params = (id_shop,)

    delete_result = delete_from_db(query , params)
    
    if delete_result:
        query = f"SELECT * FROM {TABLE_DISCOUNT} WHERE {TABLE_DISCOUNT_ID_SHOP}={id_shop}"
        select_result = select_from_db(query)
        if len(select_result) == 0 and exists:
            return {"discount_deleted":True}
        else:
            return {"discount_deleted":False}    
    else:
        return {"discount_deleted":False}

@app.route('/delete_seller' , methods=['GET'])
def delete_seller():
    id = request.args.get('id_seller', None)

    if id==None:
        abort(400)

    cmd = f"SELECT * FROM {TABLE_SELLER} WHERE {TABLE_SELLER_ID}={id}"
    select_result = select_from_db(cmd)
    if len(select_result) == 0:
        exist=False
    else:
        exist=True

    cmd = f"DELETE FROM {TABLE_SELLER} WHERE {TABLE_SELLER_ID}=%s"
    params = (id,)

    delete_result = delete_from_db(cmd , params)
    if delete_result :
        cmd = f"SELECT * FROM {TABLE_SELLER} WHERE {TABLE_SELLER_ID}={id}"
        select_result = select_from_db(cmd)
        if len(select_result) == 0 and exist:
            return {"seller_deleted":True}
        else :
            return {"seller_deleted":False}        
    else:
        return {"seller_deleted":False}        
    
@app.route('/delete_user' , methods=['GET'])
def delete_user():
    id = request.args.get('id_user', None)

    if id==None:
        abort(400)

    cmd = f"SELECT * FROM {TABLE_USER} WHERE {TABLE_USER_ID}={id}"
    select_result = select_from_db(cmd)
    if len(select_result) == 0:
        exist = False
    else:
        exist = True

    cmd = f"DELETE FROM {TABLE_USER} WHERE {TABLE_USER_ID}=%s"
    params = (id,)

    delete_result = delete_from_db(cmd , params)
    if delete_result :
        cmd = f"SELECT * FROM {TABLE_USER} WHERE {TABLE_USER_ID}={id}"
        select_result = select_from_db(cmd)
        if len(select_result) == 0 and exist:
            return {"user_deleted":True}
        else:
            return {"user_deleted":False}        
    else:
        return {"user_deleted":False}

@app.route('/delete_shop' , methods=['GET'])
def delete_shop():
    id = request.args.get('id_shop', None)

    if id==None:
        abort(400)

    cmd = f"SELECT * FROM {TABLE_SHOP} WHERE {TABLE_SHOP_ID}={id}"
    select_result = select_from_db(cmd)
    if len(select_result) == 0:
        exist = False
    else:
        exist = True

    cmd = f"DELETE FROM {TABLE_SHOP} WHERE {TABLE_SHOP_ID}=%s"
    params = (id,)

    delete_result = delete_from_db(cmd , params)
    if delete_result :
        cmd = f"SELECT * FROM {TABLE_SHOP} WHERE {TABLE_SHOP_ID}={id}"
        select_result = select_from_db(cmd)
        if len(select_result) == 0 and exist:
            return {"shop_deleted":True}
        else:
            return {"shop_deleted":False}        
    else:
        return {"shop_deleted":False}



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

    cmd = f"INSERT INTO {TABLE_SELLER} ({TABLE_SELLER_NAME}, {TABLE_SELLER_LAST_NAME}, {TABLE_SELLER_PHONE}, {TABLE_SELLER_PASSWD}) VALUES (%s, %s, %s, %s)"
    params = (name, last_name, phone, passwd)


    insert_result = insert_to_db(cmd , params)
    if insert_result:
        cmd = f"SELECT * FROM {TABLE_SELLER} WHERE {TABLE_SELLER_PHONE}={phone}"
        select_result = select_from_db(cmd)
        if len(select_result) == 1:
            id,name,last_name,phone,*_ = select_result[0]
            return {"status_register":True , "seller":{"id":id, "name":name , "last_name":last_name , "phone":phone}}
        else:
            return {"status_register":False , "seller":{}}
    else:
        return {"status_register":False , "seller":{}}   

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

    cmd = f"INSERT INTO {TABLE_SHOP} ({TABLE_SHOP_NAME}, {TABLE_SHOP_ADDRESS}, {TABLE_SHOP_LATITUDE}, {TABLE_SHOP_LONGITUDE}, {TABLE_SHOP_ID_SELLER}, {TABLE_SHOP_ID_CATEGORY}, {TABLE_SHOP_SITE}, {TABLE_SHOP_DESCRIPTION}, {TABLE_SHOP_PHONE} ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (name, address, latitude, longitude, id_seller, id_category, site, description, phone)
    
    insert_result = insert_to_db(cmd , params)
    if insert_result :
        cmd = f"SELECT * FROM {TABLE_SHOP} WHERE {TABLE_SHOP_ID_SELLER}={id_seller}"
        select_result = select_from_db(cmd)
        if len(select_result) == 1:
            id, name, address, latitude, longitude, id_seller, id_category, site, description, phone = select_result[0]
            return {"status_register":True , "shop":{"id":id, "name":name, "address":address, "latitude":latitude, "longitude":longitude, "id_seller":id_seller, "id_category":id_category, "site":site , "description":description, "phone":phone}}
        else:
            return {"status_register":False , "shop":{}}
    else:
        return {"status_register":False , "shop":{}}

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

    cmd = f"INSERT INTO {TABLE_USER} ({TABLE_USER_NAME}, {TABLE_USER_LAST_NAME}, {TABLE_USER_PHONE}, {TABLE_USER_PASSWD}) VALUES (%s, %s, %s, %s)"
    params = (name, last_name, phone, passwd)

    insert_result = insert_to_db(cmd , params)
    if insert_result:
        cmd = f"SELECT * FROM {TABLE_USER} WHERE {TABLE_USER_PHONE}={phone}"
        select_result = select_from_db(cmd)
        if len(select_result) == 1:
            id, name, last_name, phone, *_ = select_result[0]
            return {"status_register":True , "user":{"id":id, "name":name , "last_name":last_name , "phone":phone}}
        else:
            return {"status_register":False , "user":{}}
    else:
        return {"status_register":False , "user":{}}

@app.route('/register_discount' , methods=['GET'])
def registar_discount():
    name = request.args.get('name', None)
    amount = request.args.get('amount', None)
    id_shop = request.args.get('id_shop', None)

    if name==None or amount==None or id_shop==None:
        abort(400)

    cmd = f"INSERT INTO {TABLE_DISCOUNT} ({TABLE_DISCOUNT_ID_SHOP}, {TABLE_DISCOUNT_NAME}, {TABLE_DISCOUNT_AMOUNT}) VALUES (%s, %s, %s)"
    params = (id_shop, name, amount)

    insert_result = insert_to_db(cmd, params)
    if insert_result:
        cmd = f"SELECT * FROM {TABLE_DISCOUNT} WHERE {TABLE_DISCOUNT_ID_SHOP}={id_shop}"
        select_result = select_from_db(cmd)
        if len(select_result) == 1:
            id_shop,name,amount = select_result[0]
            return {"status_register":True, "discount":{"id_shop":id_shop ,"name":name , "amount":amount }}
        else:
            return {"status_register":False, "discount":{}}
    else:
        return {"status_register":False, "discount":{}}

@app.route('/register_user_message' , methods=['GET'])
def registar_user_message():
    id_user = request.args.get('id_user', None)
    id_shop = request.args.get('id_shop', None)
    text = request.args.get('text', None)

    if id_user==None or id_shop==None or text==None:
        abort(400)

    cmd = f"INSERT INTO {TABLE_MESSAGE} ({TABLE_MESSAGE_ID_USER}, {TABLE_MESSAGE_ID_SHOP}, {TABLE_MESSAGE_TEXT}) VALUES (%s, %s, %s)"
    params = (id_user, id_shop, text)

    insert_result = insert_to_db(cmd, params)
    if insert_result:
        cmd = f"SELECT * FROM {TABLE_MESSAGE} WHERE {TABLE_MESSAGE_ID_SHOP}={id_shop} AND {TABLE_MESSAGE_ID_USER}={id_user}"
        select_result = select_from_db(cmd)
        if len(select_result) == 1:
            id_user,id_shop,text = select_result[0]
            return {"message_register":True, "message":{"id_user":id_user ,"id_shop":id_shop , "text":text }}
        else:
            return {"message_register":False, "message":{}}
    else:
        return {"message_register":False, "message":{}}




if __name__ == "__main__":
    app.run("localhost" , 5000 , True)