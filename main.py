from fastapi import FastAPI, Depends
from user import get_user

app = FastAPI()

@app.get("/api/")
async def hello():
    return {"msg":"Hello, this is API server"} 


@app.get("/api/me")
async def hello_user(user = Depends(get_user)):
    return {"msg":"Hello, user","uid":user['uid']} 