from datetime import date
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings

# Create your models here.

# 시험 목록
class Test(models.Model):
    test_id = models.AutoField(primary_key=True, verbose_name='시험 코드')
    test_name = models.CharField(max_length=128, verbose_name='시험 과목')
    test_date = models.DateField(null=True, verbose_name='시험날짜')
    start_time = models.TimeField(verbose_name='시작시간')
    end_time = models.TimeField(verbose_name='종료시간')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    test_type = models.CharField(default="paper", db_column='test_type', max_length=10)
    head_count = models.IntegerField(verbose_name='인원수', default=0)
    
    def __str__(self):
        return self.test_name
    
    class Meta:
        db_table='testTable'
        verbose_name='testTable'
        verbose_name_plural='testTable'



# 응시자 목록: 입장 목록
class Examinee(models.Model):
    test_id = models.IntegerField(verbose_name='시험 코드')
    admin_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='admin_id', verbose_name='감독관id')
    examinee_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='examinee_id', verbose_name='응시자 아이디')
    entry_time = models.DateTimeField(auto_now_add=True, verbose_name='입장시간')
    test_type = models.CharField(default="paper", db_column='test_type', max_length=10)

    class Meta:
        db_table='Examinee'
