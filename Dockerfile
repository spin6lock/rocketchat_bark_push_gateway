FROM python:3.10-alpine
LABEL author="spin6lock"
WORKDIR /app
ADD . /app
EXPOSE 5050
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python3 /app/push.py
