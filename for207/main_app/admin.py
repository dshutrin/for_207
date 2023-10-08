from django.contrib import admin
from .views import *


# Register your models here.
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
	list_display = ('number', 'user')


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
	list_display = ('name', 'surname', 'likes', 'dislikes')