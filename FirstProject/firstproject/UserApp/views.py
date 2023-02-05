from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect
from .models import User
import requests

import requests
import json



# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        user_id = request.POST.get('username', None)
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print("인증성공")
            login(request, user)
            request.session['user'] = user.username
            print(request.session['user'] )

        else:
            print("인증 실패")
    
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("UserApp:login")


def main_log(request):
    return redirect("UserApp:mainpage")


# 마이페이지 구현
def mypage_view(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    context = {
        'user' : user
    }
    return render(request, 'UserApp/mypage.html', context)


def signup_view(request):

    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        # firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        userphone = request.POST["userphone"]
        userrole = request.POST["userrole"]
        email = request.POST["email"]

        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        # user.fist_name = firstname
        user.userrole = userrole
        user.userphone = userphone
        user.save()
        return redirect("UserApp:login")

    return render(request, "signup.html")



# 카카오톡 로그인 함수 #

def index(request):
    _context = {'check': False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'kakao_login/index.html', _context)
# 로그인 html 로 check 보내기?

def kakaoLoginLogic(request):
    # 카카오 디벨로퍼스 앱 생성 후 얻은 키 (로컬에 맞게)
    _restApiKey = '보안필요'
    # 카카오 디벨로퍼스에 등록 필요
    _redirectUrl = 'http://127.0.0.1:8000/auth/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)


def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    print(_qs)
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = '보안' # 프록터 애플리케이션 키
    redirect_uri = 'http://127.0.0.1:8000/auth/kakaoLoginLogicRedirect'
    authorize_code = _qs # 전체 시스템 관리자 인증 코드(6시간마다 바뀜)

    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key, #REST API KEY
        'redirect_uri':redirect_uri,
        'code': authorize_code, #로그인 시 필요한 코드
        }

    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

    filename = 'kakao_json/kakao_code_{}.json'.format(request.session['user'])
    with open(filename,"w+") as fp:
        json.dump(tokens, fp)


    return render(request, 'kakao_login/kakaoLoginSuccess.html')


def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, "indexApp:index")
    else:
        return render(request, 'kakao_login/logoutError.html')
