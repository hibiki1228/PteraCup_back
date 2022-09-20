from fastapi import FastAPI, Depends
# from routers.task import get_user
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./pteracup-firebase-adminsdk-5r6k8-ed8304a9d2.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pteracup-default-rtdb.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})



app = FastAPI()

@app.get("/api/")
async def hello():
    return {"msg":"Hello, this is API server"} 


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