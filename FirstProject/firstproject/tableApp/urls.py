from django.urls import path
from . import views
app_name = 'tableApp'

urlpatterns = [
    
    path('addTest/',views.add_testInfo, name="add_testInfo"), #시험목록 작성
    path('',views.TestListView.as_view(), name='test_list'),  #시험목록 list로 보기
    
    path('room/',views.add_examineeInfo, name='add_examinee'),                      #응시자 정보 DB에 넣기
    path('enter/',views.ExamineeListView.as_view(), name='examinee_list'),    #응시자목록 보기
]