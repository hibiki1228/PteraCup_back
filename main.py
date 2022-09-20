import imp
from fastapi import FastAPI, Depends
# from routers.task import get_user
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
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

app = FastAPI()

@app.get("/login/")
async def login():
    return

@app.get("/diary/{user_id}")
async def list(user_id:str):
    # data =diary_ref.child(user_id).get('body')
    result = users_ref.child('user004').get('name')
    return  result

@app.get("/diary/{user_id}/{diary_id}")
async def select():
    return 

@app.post("/diary/{user_id}/create")
async def create(user_id:str, body:str):
    data = {}
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