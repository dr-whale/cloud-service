FROM python
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
#CMD ["python", "-u", "weather_api.py"]