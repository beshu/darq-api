FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt
COPY ./main.py /api/main.py
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY ./app /api/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
