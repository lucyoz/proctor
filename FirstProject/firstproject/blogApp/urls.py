from django.urls import path
from . import views

urlpatterns = [
    path('',views.board_list, name='board_list'),
    path('write/',views.board_write, name='board_write'),


    # 2번째 방법
    path('list2/', views.board_list2),
    path('write2/',views.board_write2),
    path('detail2/<int:pk>/',views.board_detail2),

    path('list3/',views.board_list3),

    path('noticeBoard/',views.view_list),
    path('detailBoard/<int:pk>/',views.view_detail),
    path('noticeBoard2/',views.view_list2),

    path('write21/', views.board_write2, name='board_write'),

    path('notice_list',views.NoticeListView.as_view(), name='notice_list'),
    path('<int:pk>/',views.notice_detail_view, name='notice_detail'),
    path('notice_write/',views.notice_write_view, name='notice_write'),

]