FROM continuumio/miniconda3

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD streamlit run --server.port $PORT app.py
