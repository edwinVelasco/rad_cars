FROM python:3.11

WORKDIR /rad_cars

# COPY requirements.txt /rad_cars/

COPY . /rad_cars/

RUN pip3 install -r requirements.txt

# RUN pip3 install django-cors-headers

# CMD python3 manage.py makemigrations && python3 manage.py migrate

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# CMD ["python", "-m","pip3", "install", "django-cors-headers"]
