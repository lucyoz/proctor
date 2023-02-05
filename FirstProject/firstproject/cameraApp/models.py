import os
from django.conf import settings
from django.db import models


class Cheating(models.Model):
    examinee_id = models.CharField(max_length=24, verbose_name="응시자id", default="id")
    examinee_name = models.CharField(max_length=24, verbose_name="응시자이름", default="name" )
    test_id = models.CharField(max_length=24, verbose_name="시험번호", db_column="testid")
    test_name = models.CharField(max_length=128, verbose_name='시험 과목', db_column='testname', default='테스트')
    admin_id = models.CharField(max_length=24, verbose_name="관리자id",default="id")
    cheating_time = models.DateTimeField(auto_now_add=True, verbose_name='시간', null=True)
    cheating_type = models.TextField(db_column="cheating_type", verbose_name="부정행위유형")

