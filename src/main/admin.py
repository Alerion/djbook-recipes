from django.contrib import admin
from main.models import Project, Task, Version, Comment

admin.site.register((Project, Task, Version, Comment))