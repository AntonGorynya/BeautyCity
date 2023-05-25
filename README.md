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
Создайте суперпользователя
```sh
python3 manage.py createsuperuser
```

Перед установкой создайте файл **.env** вида:
```properties
TG_TOKEN=YOUR_TG_TOKEN
PAYMENTS_TOKEN=PAYMENTS_TOKEN
```
- Токен для Телеграм бота вы можете получить https://telegram.me/BotFather Чат ID можно узнать в свойствах канала
- Не забудьте прописать команду `/setinline.`а так же задайте описание бота через `/setdescription`
- Подключите оплату в настройках бота через BotFather

### Как запустить
Для запуска бота используйте команду
```sh
python manage.py runuserbot
```

Для запуска админки используйте команду
```sh
python manage.py runserver
```

### Вспомогательные интрументы
В репозитории присутсвует скрипт заполнения БД тестовыми данными. Для его запуска воспользуйтесь командой
```sh
python fill_db.py
```