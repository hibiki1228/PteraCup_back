from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()

# Todoテーブルの定義
class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key = True)
    user = Column('user', String(25))
    

class Diary(Base):
    __tablename__ = 'diaries'
    id = Column('id', Integer, primary_key = True)
    user_id = Column('user_id', Integer)
    body = Column('body', String(200))


# テーブル作成
Base.metadata.create_all(bind=engine)