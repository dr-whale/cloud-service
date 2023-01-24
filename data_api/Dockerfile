FROM python
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
#CMD ["python", "web_app.py"]