# -*- codeing = utf-8 -*-
# @time : 2023/6/9
# @Author : 徐家恩
# @File : todolist2.py
# @Software : PyCharm
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
import uvicorn

# 创建FastAPI实例
app = FastAPI()

# 创建数据库连接
engine = create_engine("mysql+pymysql://root:xje981210@localhost/dbname")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 定义数据库模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))


class TodoItem(Base):
    __tablename__ = "todo_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String(100))
    description = Column(Text)
    attachment = Column(Text)


# 创建数据库表
Base.metadata.create_all(bind=engine)


# 定义请求和响应模型
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TodoItemCreate(BaseModel):
    title: str
    description: str
    attachment: str = None


class TodoItemUpdate(BaseModel):
    title: str
    description: str
    attachment: str = None


class TodoItemResponse(BaseModel):
    id: int
    title: str
    description: str
    attachment: str = None


# 用户注册
@app.post("/users/register")
def register(user: UserCreate):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


# 用户登录
@app.post("/users/login")
def login(user: UserLogin):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user or existing_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}


# 创建待办事项
@app.post("/todo_items")
def create_todo_item(item: TodoItemCreate):
    db = SessionLocal()
    new_item = TodoItem(title=item.title, description=item.description, attachment=item.attachment)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Todo item created successfully"}


# 获取所有待办事项
@app.get("/todo_items")
def get_todo_items():
    db = SessionLocal()
    items = db.query(TodoItem).all()
    return items


# 获取单个待办事项
@app.get("/todo_items/{item_id}")
def get_todo_item(item_id: int):
    db = SessionLocal()
    item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# 更新待办事项
@app.put("/todo_items/{item_id}")
def update_todo_item(item_id: int, item: TodoItemUpdate):
    db = SessionLocal()
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.title = item.title
    db_item.description = item.description
    db_item.attachment = item.attachment
    db.commit()
    db.refresh(db_item)
    return {"message": "Todo item updated successfully"}


# 删除待办事项
@app.delete("/todo_items/{item_id}")
def delete_todo_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Todo item deleted successfully"}


# 附件上传
@app.post("/attachments")
def upload_attachment(file: UploadFile = File(...)):
    # 这里可以添加文件存储逻辑，比如将文件保存到本地或云存储，并返回文件的访问链接
    return {"filename": file.filename}


# 运行应用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
