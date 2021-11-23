from django.contrib import admin
from .models import Message, Room, Topic, User

# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(User)