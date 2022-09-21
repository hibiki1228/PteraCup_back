import imp
from unittest import async_case

import firebase_admin
# from routers.task import get_user
import requests
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials, db
from pydantic import BaseModel
import random

cred = credentials.Certificate({
    projectId: FIREBASE_PROJECT_ID,
    clientEmail: GOOGLE_CLIENT_EMAIL,
    privateKey: GOOGLE_PRIVATE_KEY
})

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pteracup-default-rtdb.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

diary_ref = db.reference('diary')
users_ref = db.reference('users')

app = FastAPI()

@app.get("/")
async def hello():
    return {'msg':'hello'}

@app.get("/signup")
async def signup(username:str, email:str, password:str):
    cnt = len(users_ref.get().keys())+1
    result = users_ref.push({
        'user_id':cnt,
        'name': username,
        'email': email,
        'password': password
    })

    return cnt

@app.get("/login")
async def login(email:str, password:str):
    users = users_ref.get()

    for key, val in users.items():
        if val['email'] == email:
            if val['password'] == password:
                return val['user_id']

    return {'msg', 'error! I cannnot found your account.'} # user['uid']

@app.get("/diary/{user_id}")
async def list(user_id:int):
    #ユーザーidが一致する日記をすべて持ってくる
    diaries = diary_ref.get()
    keys = []
    vals = []

    data = []

    for key, val in diaries.items():
        vals.append(val)
        # print(val['user_id'])
        if val['user_id'] == user_id:
            keys.append(key)
            data.append(diary_ref.child(key).get())

    return data


@app.get("/my_diary/{user_id}")
async def my_diary_list(user_id:int):
    my_others_diaries = []
    diaries = diary_ref.get()
    users = users_ref.get()
    others_diary_ids = users["others_diary_ids"]
    for id in others_diary_ids:
        my_others_diaries.append(diaries[id])
    return my_others_diaries

@app.get("/diary/random")
async def rand_diary():
    diaries = diary_ref.get()
    keys = []
    vals = []

    data = []

    for key, val in diaries.items():
        i = random.randint(0,10) % 4
        if i == 0:
            data.append(val)
        
    return data
    



@app.get("/diary/create")
async def create(user_id:int, body:str[256], title:str, date:str):
    cnt = (diary_ref.get().keys())
    result = diary_ref.push({
        'title': title,
        'body': body,
        'user_id': user_id,
        'date': date
    })
    user_diaries=users_ref.get()["my_diary_list"]
    user_diaries +=f",{diary_ref.get()[diary_ref.get().values()[cnt]]}"

    users_ref.child(user_id).update({"my_diary_list":user_diaries})

    return {'msg': 'success!'}

# @app.post("/diary/{user_id}/{diary_id}/delete")
# async def delete():
#     return

# @app.post("/diary/{user_id}/{diary_id}/update")
# async def update():
#     return

# @app.get("/api/add")
# async def add():
#     users_ref = db.reference('/users')
#     users_ref.child('user004').set({
#       'user_id': '4',
#       'name': 'ahi'
#     })


#     return {"msg": "success!"}
