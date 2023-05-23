# Сервис BeautyCity

Бот который, позволяет автоматизировать запись на процедуры, выбор специалиста, расписание самих специалистов, принимать оплату и чаевые.

### Как установить
Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Создайте базу данных SQLite

```sh
python3 manage.py makemigrations
python3 manage.py migrate
```
Перед установкой создайте файл **.env** вида:
```properties
TG_TOKEN=YOUR_TG_TOKEN
```
- Токен для Телеграм бота вы можете получить https://telegram.me/BotFather Чат ID можно узнать в свойствах канала
- Не забудьте прописать команду `/setinline.`а так же задайте описание бота через `/setdescription`

### Как запустить

```sh
python manage.py runuserbot
```