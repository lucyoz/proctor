from django import forms
from .models import Test, Examinee

class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['test_name'].label = '시험과목'
        self.fields['test_name'].widget.attrs.update({
            'placeholder':'시험과목을 입력해주세요.',
            'class':'form-control',
            'autofocus':True,
        })

    class Meta:
        model = Test
        fields = ['test_name','test_date','start_time','end_time', 'test_type','head_count']


class ExamineeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExamineeForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].label = '시험코드'
        self.fields['test_id'].widget.attrs.update({
            'placeholder':'시험코드를 입력해주세요.',
            'class':'form-control',
            'autofocus':True,
        })
    class Meta:
        model = Examinee
        fields = ['test_id']

