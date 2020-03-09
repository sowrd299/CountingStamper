from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Player)
admin.site.register(Question)
admin.site.register(Queue)
admin.site.register(QuestionInQueue)
admin.site.register(Board)
admin.site.register(Cell)
