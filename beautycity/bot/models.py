from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Client(models.Model):
    nickname = models.CharField(max_length=500, verbose_name='Никнейм клиента')
    name = models.CharField(max_length=40, verbose_name='Имя клиента', null=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True)
    personal_data_consent = models.BooleanField(verbose_name='Согласие на ОПД', default=False)

    def __str__(self):
        return f'{self.name} {self.phone}'


class Master(models.Model):
    name = models.CharField(max_length=40, verbose_name='Имя мастера')

    def __str__(self):
        return f'{self.name}'


class Site(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название салона')
    address = models.CharField(max_length=40, verbose_name='адрес салона')

    def __str__(self):
        return f'{self.name} {self.address}'


class Service(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название услуги')
    price = models.IntegerField(
        validators=[
            MaxValueValidator(10000),
            MinValueValidator(1)
        ],
        verbose_name='Цена'
    )

    def __str__(self):
        return f'{self.name} {self.price} руб'


class MasterSchedule(models.Model):
    date = models.DateField(verbose_name='Date')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='schedule')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='schedule')

    def __str__(self):
        return f'{self.date} {self.master} {self.site}'


class Shift(models.Model):
    start_time = models.TimeField(verbose_name='star_time')
    end_time = models.TimeField(verbose_name='end_time')

    def __str__(self):
        return f'{self.star_time} {self.end_time}'


class Promocode(models.Model):
    code = models.CharField(max_length=10, verbose_name='promocode')
    star_date = models.DateField(verbose_name='Действует от')
    end_date = models.DateField(verbose_name='Действует до')
    discount = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Скидка %'
    )
    limit = models.IntegerField(default=1, verbose_name='Количество использовании')

    def __str__(self):
        return f'{self.code}'


class Feedback(models.Model):
    text = models.CharField(max_length=120, verbose_name='Feedback')
    client = models.ManyToManyField(Client, related_name='feedbacks')
    master = models.ManyToManyField(Master, related_name='feedbacks')
    date = models.DateField(verbose_name='Дата отзыва')

    def __str__(self):
        return f'{self.client} {self.master} {self.date}'


class ClientOffer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='offer')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offer')
    master_schedule = models.ForeignKey(MasterSchedule, on_delete=models.CASCADE, related_name='offer')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='offer')
    promocode = models.ManyToManyField(Promocode, related_name='offer', blank=True)

    def __str__(self):
        return f'{self.client} {self.service} {self.master_schedule} {self.shift}'
