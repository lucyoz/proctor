from django.urls import path
from . import views

app_name = 'indexApp'

urlpatterns = [
    ## path('',views.board_list, name='board_list'),
    path('', views.index2, name='index'),
    #path('notice/', views.notice, name='notice'),
    path('room/',views.waiting_room, name='waiting'),

]