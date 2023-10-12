FROM python:3.8.2
MAINTAINER smoozy.gallardo@gmail.com
RUN pip install telebot psycopg2
WORKDIR /app
COPY main.py /app/main.py
ENV TOKEN = '6294705740:AAFRerVokBR-XTZu2GtBs0hbKpyg3hx9GEA'
ENV DB_NAME='answers'
ENV DB_USER='postgres'
ENV DB_PASSWORD='root'
ENV DB_HOST='localhost'
ENV DB_PORT='5432'
CMD ['python', 'main.py']
