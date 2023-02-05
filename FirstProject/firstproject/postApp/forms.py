from django.forms import ModelForm
from .models import FileUpload

class FileUploadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = '내용'
        self.fields['content'].widget.attrs.update({
            'placeholder':'포착된 시간, 기타 내용 등을 기입해주세요.',
            'class':'form-control',
            'autofocus':True,
        })

    class Meta:
        model = FileUpload
        fields = ['test_name', 'content', 'imgfile']
