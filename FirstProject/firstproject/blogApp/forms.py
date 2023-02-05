from django import forms
from .models import Board, Notice
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class BoardWriteForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'placeholder':'게시글 제목'
            }),
        required=True,
    )

    contents = SummernoteTextField()
    filed_order=[
        'title',
        'contents'
    ]


    class Meta:
        model = Board
        fields = [
            'title',
            'contents'
        ]
        widgets = {
            'contents' : SummernoteWidget()
        }


    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title','')
        contents = cleaned_data.get('contents','')
        
        if title == '':
            self.add_error('title','글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents','글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents


class BoardForm(forms.Form):
    title = forms.CharField(error_messages={'required':'제목을 입력하세요'},max_length=100, label='게시글 제목')
    contents = forms.CharField(error_messages={'required':'내용을 입력하세요.'},widget=forms.Textarea, label='게시글 내용')



class NoticeWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NoticeWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder':'제목을 입력해주세요.',
            'class':'form-control',
            'autofocus':True,
        })

    class Meta:
        model = Notice
        fields = ['title', 'contents']
        widgets = {
            'contents': SummernoteWidget(),
        }