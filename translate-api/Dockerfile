FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

EXPOSE 3002

CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "3002"]