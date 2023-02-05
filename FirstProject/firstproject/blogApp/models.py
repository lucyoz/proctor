from tabnanny import verbose
from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=64, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    #writer = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='작성자')
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    update_dttm = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'

class Notice(models.Model):
    writer = '임시'
    title = models.CharField(max_length=128, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    #hits = models.PositiveBigIntegerField(verbose_name='조회수', default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    update_date = models.DateField(auto_now=True, verbose_name='수정일')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table='NoticeBoard'
        verbose_name='NoticeBoard'
        verbose_name_plural='NoticeBoard'


        