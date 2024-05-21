# 베이스 이미지 설정
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

# 빌드 인자 설정
ARG DEBUG
ARG SECRET_KEY
ARG ENGINE
ARG NAME
ARG USER
ARG PASSWORD
ARG HOST
ARG PORT

# 환경 변수 설정
ENV DEBUG=${DEBUG}
ENV SECRET_KEY=${SECRET_KEY}
ENV ENGINE=${ENGINE}
ENV NAME=${NAME}
ENV USER=${USER}
ENV PASSWORD=${PASSWORD}
ENV HOST=${HOST}
ENV PORT=${PORT}

# 작업 디렉토리 설정
RUN mkdir /app
WORKDIR /app

# 프로젝트 파일 복사
COPY . /app/

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 포트 설정
EXPOSE 8000

# 장고 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]