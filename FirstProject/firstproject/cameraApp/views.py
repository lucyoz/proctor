# from time import timezone
from django.shortcuts import render
import cv2
import os
from .detection.Digital_test import eyeTracking, anglesOfHead, detectAndDisplay
from .detection.Paper_test import detectAndDisplay2
import datetime
from .models import Cheating
from UserApp.models import User
from tableApp.models import Examinee, Test
from django.views.generic import ListView
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .kakao import Kakao


def db_to_list(admin_str):

    cheating = Cheating.objects.filter(admin_id=admin_str).latest('cheating_time') #admin.username
    print(cheating.examinee_id)
    print(cheating.test_name)
    print(cheating.admin_id)
    print(cheating.cheating_type)

    message = "관리자%s님, 부정행위가 발생했습니다.\n과목명: %s, 응시자: %s\n부정행위 유형: %s" % (cheating.admin_id, cheating.test_name, cheating.examinee_name, cheating.cheating_type)
    #message = "응시자: %s\n부정행위 유형: %s" % (cheating.examinee_id, cheating.cheating_type)
    return message

def capture_save(filename, frame):
    extension = os.path.splitext(filename)[1]
    result, n = cv2.imencode(extension, frame, None)
    if result:
        with open(filename, mode='w+b') as f:
            n.tofile(f)


def exam_digital(request):
    user = request.session['user']
    user_id = User.objects.get(username = user)
    enter_info = Examinee.objects.filter(examinee_id=user_id).latest('entry_time')
    test_info = Test.objects.get(test_id=enter_info.test_id)

    #-- 비디오 활성화
    cap = cv2.VideoCapture(0) #-- 웹캠 사용시 vedio_path를 0 으로 변경
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    record = False
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        # cheating table에 ['웹캠 없음'] 추가
        cam_not_found = Cheating(examinee_id=user_id, examinee_name=user_id.last_name, test_id=enter_info.test_id, test_name=test_info.test_name,admin_id=enter_info.admin_id, cheating_type='[웹캠 없음]')
        cam_not_found.save()
        exit(0)
    #count = 0
    myDetectAndDisplay = detectAndDisplay()
    myAnglesOfHead = anglesOfHead()
    myEyeTracking = eyeTracking()
    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        hour = now.strftime('%H%M%S')

        # 웹캠 화면 캡쳐 - 파일 구조 변경할것! 
        filename = './cameraApp/image/Webcam_{}_{}.png'.format(date, hour)

        
        ##############
        key =cv2.waitKey(33)
        
        logg = []
        logg2 = []
        ###############
        # run module
        frame = myEyeTracking.run(frame)
        frame = myDetectAndDisplay.run(frame, logg, logg2)
        frame = myAnglesOfHead.run(frame, logg, logg2)
        
        cv2.imshow("press 'q' button to exit", frame)
        print(logg)
        print(logg2)
        #logg2가 비어있지 않다면: 부정행위가 포착된다면
        if len(logg2)!=0:
            cheating = Cheating(examinee_id=user_id, examinee_name=user_id.last_name, test_id=enter_info.test_id, test_name=test_info.test_name,admin_id=enter_info.admin_id, cheating_type=logg2)

            cheating.save()
            capture_save(filename, frame)
            
            admin = User.objects.get(username=enter_info.admin_id)

            message = db_to_list(cheating.admin_id)
            forKakao = Kakao(message, admin)
            forKakao.send_message()


        #-- q 입력시 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return render(request, "digital_exam.html")


def exam_paper(request):
    user = request.session['user']
    user_id = User.objects.get(username = user)
    enter_info = Examinee.objects.filter(examinee_id=user_id).latest('entry_time')
    test_info = Test.objects.get(test_id=enter_info.test_id)

    #-- 비디오 활성화
    cap = cv2.VideoCapture(0) #-- 웹캠 사용시 vedio_path를 0 으로 변경
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    record = False
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        cam_not_found = Cheating(examinee_id=user_id, examinee_name=user_id.last_name, test_id=enter_info.test_id, test_name=test_info.test_name,admin_id=enter_info.admin_id, cheating_type='[웹캠 없음]')
        cam_not_found.save()
        exit(0)
    #count = 0
    myDetectAndDisplay = detectAndDisplay2()
    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        hour = now.strftime('%H%M%S')

        # 웹캠 화면 캡쳐 - 파일 구조 변경할것! 
        filename = './cameraApp/image/Webcam_{}_{}.png'.format(date, hour)
        
        key =cv2.waitKey(33)
        
        logg = []
        logg2 = []
        frame = myDetectAndDisplay.run(frame, logg, logg2)
        
        cv2.imshow("test", frame)
        print(logg)
        print(logg2)
        #logg가 비어있지 않다면: 부정행위가 포착된다면
        if len(logg2)!=0:
            cheating = Cheating(examinee_id=user_id, examinee_name=user_id.last_name, test_id=enter_info.test_id, test_name=test_info.test_name,admin_id=enter_info.admin_id, cheating_type=logg2)

            cheating.save()
            capture_save(filename, frame)
            admin = User.objects.get(username=enter_info.admin_id)

            message = db_to_list(cheating.admin_id)
            forKakao = Kakao(message, admin)
            forKakao.send_message()

        ###############
        
        if key == 27:
            break
        elif key == 26:
            now = datetime.datetime.now().strftime("%y_%m_%d_%H-%M-%S")
            print(str(now)+"캡쳐")

        #-- q 입력시 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return render(request, "paper_exam.html")


class CheatingListView(ListView):
    model = Cheating
    paginate_by = 5
    template_name = 'cheating_list.html'
    context_object_name = 'cheating_list'

    def get_queryset(self):
        search_keyword = self.request.GET.get('q','')
        search_type = self.request.GET.get('type','')
        cheating_list = Cheating.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword)>1:
                if search_type=='test_id':
                    search_examinee_list = cheating_list.filter(test_id__exact=search_keyword)
                elif search_type=='test_name':
                    search_examinee_list = cheating_list.filter(test_name__exact=search_keyword)
                return search_examinee_list
            else:
                messages.error(self.request,'검색어는 2글자 이상 입력해주세요')

        return cheating_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q','')
        search_type = self.request.GET.get('type','')
        if len(search_keyword)>1:
            context['q'] = search_keyword
        context['type'] = search_type
        
        return context

class CheatingListViewByUserId(ListView):
    model = Cheating
    paginate_by = 5
    template_name = 'exam_result.html'
    context_object_name = 'exam_result'


    def get_queryset(self):       
        today_min = datetime.datetime.combine(timezone.localtime().date(), datetime.datetime.today().time().min)
        today_max = datetime.datetime.combine(timezone.localtime().date(), datetime.datetime.today().time().max) 
        user = self.request.session['user']
        user_id = User.objects.get(username = user)
        exam_result = Cheating.objects.filter(examinee_id=user_id).order_by('-id')
        exam_result = Cheating.objects.filter(cheating_time__range=(today_min, today_max)).order_by('-id')
        return exam_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        
        return context


