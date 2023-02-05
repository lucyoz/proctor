from django.contrib import admin
from .models import Test
# Register your models here.
class TestAdmin(admin.ModelAdmin):
    list_display=(
        'test_id',
        'test_name',
        'writer',
        'test_date',
        'start_time',
        'end_time',
        'test_type'
    )
    search_fields = ('test_id','test_name',)

admin.site.register(Test, TestAdmin)
