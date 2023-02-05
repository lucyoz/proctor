from django.contrib import admin
from .models import Board, Notice
from django_summernote.admin import SummernoteModelAdmin

# python -m pip install django-summernote 수행함.

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'contents', 'write_dttm', 'update_dttm')

admin.site.register(Board, BoardAdmin)

class NoticeAdmin(admin.ModelAdmin):
    list_display=(
        'title',
        'writer',
        'registered_date'
    )
    search_fields = ('title','content', 'writer__user_id',)

admin.site.register(Notice, NoticeAdmin)