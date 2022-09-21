import imp
from unittest import async_case

import firebase_admin
# from routers.task import get_user
import requests
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials, db
from pydantic import BaseModel

cred = credentials.Certificate('./pteracup-firebase-adminsdk-5r6k8-ed8304a9d2.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pteracup-default-rtdb.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})


# def get_idToken(email:str, password:str):
#     url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBNqch4NCLa-dLeCUfKnjktXx4SzBLViOM"

#     para = {
#         "email": email,
#         "password": password,
#         "returnSecureToken":true
#     }

#     return requests.post(url, params=para)

# def get_user(res: Response, cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))):
#     if cred is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Bearer authentication required",
#             headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
#         )
#     try:
#         decoded_token = auth.verify_id_token(cred.credentials)
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Invalid authentication credentials. {err}",
#             headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
#         )
#     res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
#     return decoded_token

diary_ref = db.reference('diary')
users_ref = db.reference('users')

class diary(BaseModel):
    author: str
    title: str
    date: str
    diaryText: str

app = FastAPI()

# @app.get("/api/me")
# async def hello_user(user = Depends(get_user)):
#     return {"msg":"Hello, user","uid":user}


@app.get("/signup")
async def signup(username:str, email:str, password:str):
    cnt = len(users_ref.get().keys())+1
    result = users_ref.push({
        'user_id':cnt,
        'name': username,
        'email': email,
        'password': password
    })
    # result = users_ref.get()

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
        print(val['user_id'])
        if val['user_id'] == user_id:
            keys.append(key)
            data.append(diary_ref.child(key).get())

    return data

# @app.get("/my_diary/{user_id}")
# async def my_diary_list(user_id:int):
#     my_others_diaries = []
#     diaries = diary_ref.get()
#     user_info = users_ref.get()
#     for  val in user_info.values():
#         if user_id == val['user_id']:
#             my_others_diaries=val.others_diary_list
#     vals =[]

#     for my_others_diary in my_others_diaries:
#         for val in diaries.values():
#             if my_others_diary == val.id:
#                 vals.append(val)
#     return vals


@app.get("/diary/create")
async def create(user_id:int, body:str, title:str, date:str):
    result = diary_ref.push({
        'title': title,
        'body': body,
        'user_id': user_id,
        'date': date
    })
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
