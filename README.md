editar el docker-compose.yaml.

este archivo tiene dos lineas importantes

las cuales son:

    command: python manage.py migrate
    command: python manage.py runserver 0.0.0.0:8000

solo una debe estar activa.

la primera crea las migraciones en la base de datos, es el primer paso para desplegar.

la segunda ejecuta el proyecto.

Estos dos comandos no se pueden ejecutar al mismo tiempo y si se estan ejecutando migraciones se debe comentariar la ejecución con #

Para crear las migraciones debe estar así.

    command: python manage.py migrate
    # command: python manage.py runserver 0.0.0.0:8000

Para ejecutar el servidor debe estar así.

    # command: python manage.py migrate
    command: python manage.py runserver 0.0.0.0:8000

