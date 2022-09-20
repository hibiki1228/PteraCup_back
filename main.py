import imp
from fastapi import FastAPI, Depends
# from routers.task import get_user
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase

# cred = credentials.Certificate('./pteracup-firebase-adminsdk-5r6k8-ed8304a9d2.json')

# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://pteracup-default-rtdb.firebaseio.com',
#     'databaseAuthVariableOverride': {
#         'uid': 'my-service-worker'
#     }
# })

PRJ_ID = "pteracup"
API_KEY = "AIzaSyBNqch4NCLa-dLeCUfKnjktXx4SzBLViOM"
config = {
  "apiKey": API_KEY,
  "authDomain": PRJ_ID + ".firebaseapp.com",
  "databaseURL": "https://" + PRJ_ID + ".firebaseio.com/",
  "storageBucket": PRJ_ID + ".appspot.com"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()

app = FastAPI()

@app.get("/login/")
async def login():
    return

@app.get("/diary/{user_id}")
async def list(user_id:str):
    #ユーザーidが一致する日記をすべて持ってくる
    data = db.child(user_id).get(user['idToken'])
    return  data

@app.get("/diary/{user_id}/{diary_id}")
async def select():
    return 

@app.post("/diary/{user_id}/create")
async def create():
    return

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