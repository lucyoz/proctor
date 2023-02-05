from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

# Create your models here.
class FileUpload(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    test_name = models.CharField(max_length=40, null=True, verbose_name='과목명')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    content = models.TextField(verbose_name='내용', null=True)
    imgfile = ProcessedImageField(null=True, upload_to="postings/",blank=True, processors=[ResizeToFit(width=580)])

    def __str__(self):
        return self.test_name