from django.contrib import admin
from .models import *


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location')
    search_fields = ('id', 'user')


admin.site.register(Profile, ProfileAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'topic', 'user', 'created', 'updated')
    search_fields = ('id', 'name', 'created')


admin.site.register(Room, RoomAdmin)
admin.site.register(Topic)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'body', 'created', 'updated')
    search_fields = ('id', 'user', 'body', 'created')


admin.site.register(Message, MessageAdmin)
