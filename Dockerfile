FROM python:3.11

WORKDIR /rad_cars

# COPY requirements.txt /rad_cars/

COPY . /rad_cars/

RUN pip3 install -r requirements.txt

# RUN pip3 install django-cors-headers

CMD python manage.py makemigrations && python manage.py migrate

# RUN python manage.py makemigrations
# RUN python manage.py migrate

# CMD ["python", "-m","pip3", "install", "django-cors-headers"]
