from django.contrib import admin
from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'phone']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(MasterSchedule)
class MasterScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'master', 'site']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientOffer)
class ClientServiceAdmin(admin.ModelAdmin):
    list_display = ['client', 'master_schedule', 'shift']
    raw_id_fields = ['client']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    raw_id_fields = ['client']