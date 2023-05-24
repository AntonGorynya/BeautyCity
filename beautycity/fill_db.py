import datetime
from beautycity.wsgi import *
from bot.models import Master, Site, Service, MasterSchedule, Shift, Promocode


if __name__ == '__main__':
    Master.objects.get_or_create(name='Татьяна')
    Master.objects.get_or_create(name='Наталья')
    Site.objects.get_or_create(name='Cалон 1', address='Уездный город N ул. ленина 2')
    Service.objects.get_or_create(name='Стрижка', price='700')
    Service.objects.get_or_create(name='Укладка', price='200')
    MasterSchedule.objects.get_or_create(
        date=datetime.date(2023, 6, 1),
        master=Master.objects.get(pk=1),
        site=Site.objects.get(pk=1)
    )
    MasterSchedule.objects.get_or_create(
        date=datetime.date(2023, 6, 2),
        master=Master.objects.get(pk=2),
        site=Site.objects.get(pk=1)
    )
    Shift.objects.get_or_create(
        star_time=datetime.time(9, 0),
        end_time=datetime.time(9,30)
    )
    Shift.objects.get_or_create(
        star_time=datetime.time(9, 30),
        end_time=datetime.time(10, 0)
    )
    Promocode.objects.get_or_create(
        code='Welcome10',
        star_date=datetime.date(2023, 5, 1),
        end_date=datetime.date(2023, 8, 1),
        discount=10)