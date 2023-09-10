FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./ get_around_pricing.csv /app/data/
COPY gbr_model.pkl /app/
COPY preprocessor.pkl /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./main.py /app/

CMD gunicorn main:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker