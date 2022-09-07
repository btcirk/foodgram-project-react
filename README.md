# Проект "Foodgram"

![example workflow](https://github.com/btcirk/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

Онлайн-сервис «Продуктовый помощник» позволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Как запустить проект

### Подготовка сервера для развертывания 

- Установите Docker и Docker Compose на сервер:
```
 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
 ```
 Более подробная инструкция по установке для различных типов операционных систем доступна в официальной документации [Docker](https://docs.docker.com/compose/install/)

 - Скопируйте файлы `docker-compose.yml` и `default.conf` из директории `infra` на сервер:
 ```
 scp infra/docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
 scp infra/nginx.conf <username>@<host>:/home/<username>/nginx.conf
 ```

- Создайте файл .env и укажите в нем переменные окружения:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
DJANGO_SECRET_KEY=<секретный ключ Django>
HOST=<IP-адрес сервера>
```

- В конфигурационном файле nginx.conf в строке server_name укажите IP-адрес своего сервера:
```
Пример:     server_name 127.0.0.1;
```



