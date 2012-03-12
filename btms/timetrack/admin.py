from django.contrib import admin
from timetrack.models import Status,Task,MyTask

admin.site.register(Status)
admin.site.register(Task)
admin.site.register(MyTask)
