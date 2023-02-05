"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from cameraApp import views
from accounts.views import blog, posting

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("",views.index,name="index"),
    # path("users/",views.user_view, name='users'),
    # path("signup/",views.signup, name="signup"),
    #path("board/",views.PostLV.as_view(), name='post_list'), #앱과의 연결을 위하여 include 사용
    #path("board/",include('accounts.urls')),
    #path('blog/', blog, name='blog'),
    #path('blog/<int:pk>',posting, name="posting"),

    #path('waiting/',include('accounts.urls')),
    #path('waiting/test/', views.cameraTest, name='cameraTest'),


    # blogApp에서 공지사항 페이지 url -> post
    path('board/', include('blogApp.urls')),

    # tableApp에서 각 보드 Table 볼 수 있음
    path('table/',include('tableApp.urls')),

    path('mainpage/', include('indexApp.urls')),
    
    path('camera/',include('cameraApp.urls')),
    
    path('summernote/',include('django_summernote.urls')),

    path('table/',include('tableApp.urls')),
    path('auth/',include('UserApp.urls')),

    path('room/paper',views.exam_paper, name='exam_paper'),
    path('room/digital',views.exam_digital, name='exam_digital'),
    path('cheating/',views.CheatingListViewByUserId.as_view(), name='exam_result'),
    path('table/cheating',views.CheatingListView.as_view(), name='cheating_list'),    #응시자목록 보기
    
    path('post/',include('postApp.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
