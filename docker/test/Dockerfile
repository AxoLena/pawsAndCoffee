FROM python:3.12

ENV DJANGO_SETTINGS_MODULE=pawsAndCoffee.settings
ENV APP=/app
WORKDIR $APP

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

CMD [ "pytest", "tests"]