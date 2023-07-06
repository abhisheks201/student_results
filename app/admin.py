from django.contrib import admin
from django import forms
from .models import User, Marks





class MarksAdmin(admin.ModelAdmin):
    list_display = ['user', 'telugu', 'hindi', 'english', 'maths', 'science', 'social']


admin.site.register(User)
admin.site.register(Marks, MarksAdmin)

