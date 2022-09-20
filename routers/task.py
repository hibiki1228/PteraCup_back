from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from db import Diary, engine

# DB接続用のセッションクラス インスタンスが作成されると接続する
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class DiaryIn(BaseModel):
    title: str
    done: bool

# 単一のTodoを取得するためのユーティリティ
def get_diary(db_session: Session, diary_id: int):
    return db_session.query(Diary).filter(Diary.id == diary_id).first()

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# このインスタンスをアノテーションに利用することでエンドポイントを定義できる
app = FastAPI()

# Todoの全取得
@app.get("/diaries/")
def read_diaries(db: Session = Depends(get_db)):
    diaries = db.query(Diary).all()
    return diaries

# 単一のTodoを取得
@app.get("/diaries/{diary_id}")
def read_diary(diary_id: int, db: Session = Depends(get_db)):
    diary = get_diary(db, diary_id)
    return diary

# Todoを登録
@app.post("/diaries/")
async def create_diary(diary_in: DiaryIn,  db: Session = Depends(get_db)):
    todo = Diary(title=diary_in.title, done=False)
    db.add(diary)
    db.commit()
    todo = get_diary(db, diary.id)
    return diary

# Todoを更新
@app.put("/diaries/{diary_id}")
async def update_diary(diary_id: int, diary_in: DiaryIn, db: Session = Depends(get_db)):
    diary = get_diary(db, diary_id)
    diary.title = diary_in.title
    diary.done = diary_in.done
    db.commit()
    diary = get_diary(db, diary_id)
    return diary

# Todoを削除
@app.delete("/diaries/{diary_id}")
async def delete_diary(diary_id: int, db: Session = Depends(get_db)):
    diary = get_diary(db, diary_id)
    db.delete(diary)
    db.commit()

# リクエストの度に呼ばれるミドルウェア DB接続用のセッションインスタンスを作成
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    