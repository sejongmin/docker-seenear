# 베이스 이미지 설정
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
RUN mkdir /app
WORKDIR /app

# 프로젝트 파일 복사
COPY . /app/

# 의존성 파일 복사 및 설치
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* 
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt