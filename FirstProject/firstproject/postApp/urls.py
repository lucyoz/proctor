from django.urls import path
from . import views
app_name = 'postApp'

urlpatterns = [
    
    path('write/',views.fileUpload, name="fileUpload"),
    path('',views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/',views.post_detail_view, name='post_detail'),

]