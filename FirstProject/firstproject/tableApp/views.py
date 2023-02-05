from asyncio.windows_events import NULL
from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from .models import Test, Examinee
from .forms import ExamineeForm, TestForm
from UserApp.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def view_board(request):
    return render(request, "view_table.html")

@login_required
def add_testInfo(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        user = request.session['user']
        user_id = User.objects.get(username = user)
        print(form)
        if form.is_valid():            
            test = form.save()
            test.writer = user_id
            print(test.test_type)
            test.save()
            return redirect('/table')
    else:
        print("GET")
        form = TestForm()
    return render(request, 'add_test.html', {'form': form})

class TestListView(ListView):
    model = Test
    paginate_by = 5
    template_name = 'view_table.html'
    context_object_name = 'view_table'

    def get_queryset(self):
        view_table = Test.objects.order_by('-test_id')
        return view_table

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

def view_list(request):
    boards = Test.objects.all().order_by('-test_id')
    return render(request, 'test_list.html',{"boards":boards})

#waiting_room 
def wait(request):
    return render(request, "waiting_room.html")

#입장목록 DB에 넣기
def add_examineeInfo(request):
    print("add_examinee?")
    if request.method == 'POST':
        form = ExamineeForm(request.POST)
        user = request.session['user']
        user_id = User.objects.get(username = user)
        print("POST")
        print(form)
        if form.is_valid():            
            examinee = form.save()
            examinee.examinee_id = user_id
            test = Test.objects.get(test_id=examinee.test_id)
            if test.writer==None:
                messages.error(request,"잘못된 시험코드입니다.")
                return render(request, 'waiting_room.html', {'form':form})
            examinee.admin_id = test.writer
            examinee.test_type = test.test_type
            print(examinee.examinee_id)
            examinee.save()
            print(test.test_type)
            if (test.test_type=='paper'):
                return redirect('exam_paper')
            elif (test.test_type=='digital'):
                return redirect('exam_digital')
            return redirect('/table/enter')
    else:
        print("GET")
        form = ExamineeForm()
    return render(request, 'waiting_room.html', {'form': form})

#입장목록 보기
class ExamineeListView(ListView):
    model = Examinee
    paginate_by = 5
    template_name = 'examinee_list.html'
    context_object_name = 'examinees'

        # 검색 기능 추가
    def get_queryset(self):
        search_keyword = self.request.GET.get('q','')
        search_type = self.request.GET.get('type','')
        examinees = Examinee.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword)>1:
                if search_type=='test_id':
                    search_examinee_list = examinees.filter(test_id__exact=search_keyword)
                elif search_type=='examinee_id':
                    search_examinee_list = examinees.filter(examinee_id__exact=search_keyword)
                elif search_type=='writer':
                    search_examinee_list = examinees.filter(writer__exact=search_keyword)
                return search_examinee_list
            else:
                messages.error(self.request,'검색어는 2글자 이상 입력해주세요')
        return examinees

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



        

def exam_paper(request):
    return render(request, "paper_exam.html")

def exam_digital(request):
    return render(request, "digital_exam.html")


