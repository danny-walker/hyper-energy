HYPER ENERGY - проект, реализующий логику блога с возможностью регистрации пользователей, редактирования пользовательского профиля, сброса-восстановления пользовательского пароля с уведомлением по e-mail, добавления-редактирования-удаления-рекомендации пользователями постов, выставление оценки, тэгами, поисковой системой, sitemap, а также дополнительного функционала в виде возможности расчета ветроэнергетической установки / солнечной электростанции / биоэнергетического комплекса c визуализацией данных.

### Установка и запуск локально
1. Клонируйте репозиторий:
```bash
git clone https://github.com/danny-walker/hyper-energy.git
```
2. Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```
3. В settings.py замените значения следующих параметров на собственные:
```bash
SECRET_KEY
DEBUG
DATABASES
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
в CACHES для default и select2 параметры LOCATION и PASSWORD
```
4. Запустите сервер:
```bash
python manage.py runserver
```
5. Проект доступен на 127.0.0.1:8000.
6. Настройка Solr+Haystack: 
```bash
https://stackoverflow.com/questions/61939043/django-haystack-and-solr-8-5-1
```