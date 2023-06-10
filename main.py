# -*- codeing = utf-8 -*-
# @time : 2023/6/10
# @Author : 徐家恩
# @File : main.py
# @Software : PyCharm
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

'''然后在终端中运行以下命令构建和运行Docker容器：
docker build -t todolist-app .
docker run -p 8000:8000 todolist-app
'''