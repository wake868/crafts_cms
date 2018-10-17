from django.contrib import admin
from .models import Company, Schedule, Content, Piece


# Register your models here.
admin.site.register(Company)
admin.site.register(Schedule)
admin.site.register(Content)
admin.site.register(Piece)
