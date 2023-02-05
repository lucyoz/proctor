from django.urls import path
from . import views

app_name = "UserApp"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("<int:pk>/", views.mypage_view, name="mypage"),
    path("kakao", views.index, name="index"),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),
    # path('kakaoLoginLogicRedirect/kakaoLogout', views.kakaoLogout)
]
