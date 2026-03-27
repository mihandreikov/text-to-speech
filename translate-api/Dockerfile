FROM alpine:latest 

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir fastapi num2words gtts uvicorn

EXPOSE 3002

CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "3002"]