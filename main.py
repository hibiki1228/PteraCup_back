import imp
from unittest import async_case
from fastapi import FastAPI, Depends
# from routers.task import get_user
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pydantic import BaseModel
# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://pteracup-default-rtdb.firebaseio.com', None)
# result = firebase.get('/users', None)
# print

cred = credentials.Certificate('./pteracup-firebase-adminsdk-5r6k8-ed8304a9d2.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pteracup-default-rtdb.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

# PRJ_ID = "pteracup"
# API_KEY = "AIzaSyBNqch4NCLa-dLeCUfKnjktXx4SzBLViOM"
# config = {
#   "apiKey": API_KEY,
#   "authDomain": PRJ_ID + ".firebaseapp.com",
#   "databaseURL": "https://" + PRJ_ID + ".firebaseio.com/",
#   "storageBucket": PRJ_ID + ".appspot.com"
# }
# firebase = pyrebase.initialize_app(config)

# db = firebase.database()

# ID = "test@example.com"
# PW = "your password"

# auth = firebase.auth()
# user = auth.sign_in_with_email_and_password(ID, PW)

diary_ref = db.reference('diary')
users_ref = db.reference('users')

class diary(BaseModel):
    author: str
    title: str
    date: str
    diaryText: str
    
app = FastAPI()

@app.get("/signup")
async def signup(username:str, email:str, password:str):
    result = users_ref.push({
        'name': username,
        'email': email,
        'password': password
    })
    result = users_ref.get()

    for key, val in result.items():
        if key == "name":
            if val == username:
                return 
    return 

@app.get("/login")
async def login():
    return

@app.get("/diary/{user_id}")
async def list(user_id:str):
    #ユーザーidが一致する日記をすべて持ってくる
    result = users_ref.get()
    keys = []
    vals = []
    for key, val in result.items():
        keys.append(key)
        vals.append(val)
        
    return  vals['user_id']

@app.get("/diary/{user_id}/{title}")
async def select():
    return 

@app.get("/diary/create")
async def create(user_id:int, body:str, title:str, date:str):
    result = diary_ref.push({
        'title': title,
        'body': body,
        'user_id': user_id,
        'date': date
    })
    return {'msg': 'success!'}

@app.post("/diary/{user_id}/{diary_id}/delete")
async def delete():
    return

@app.post("/diary/{user_id}/{diary_id}/update")
async def update():
    return


# @app.get("/api/me")
# async def hello_user(user = Depends(get_user)):
#     return {"msg":"Hello, user","uid":user['uid']} 

@app.get("/api/add")
async def add():
    users_ref = db.reference('/users')
    users_ref.child('user004').set({
      'user_id': '4',
      'name': 'ahi'
    })


    return {"msg": "success!"}