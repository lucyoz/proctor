from csv import unregister_dialect
from importlib.resources import contents
from msilib.schema import ListView
from multiprocessing import context
from django.shortcuts import redirect, render, get_object_or_404
from .forms import BoardWriteForm, BoardForm, NoticeWriteForm
from .models import Board, Notice
from django.views.generic import ListView
#from .models import Notice


# Create your views here.
def board_list(request):
    boards = Board.objects.all().order_by('-id')
    return render(request,'board_list.html', {"boards":boards})

def board_write(request):

    if request.method == 'GET':
        write_form = BoardWriteForm()
        context['forms'] = write_form
        return render(request, 'board_write.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board = Board(
                title=write_form.title,
                contents=write_form.contents
            )
            board.save()
            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board_write.html', context)

# 두번째 방법
def board_list2(request):
    boards = Board.objects.all().order_by('-id')
    return render(request,'board_list2.html', {"boards":boards})

# 2번 방법, 템플릿 적용
def board_list3(request):
    boards = Board.objects.all().order_by('-id')
    return render(request,'board_list3.html', {"boards":boards})

def board_write2(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']

            board.save()
    else:
        form = BoardForm()
    return render(request, 'board_write.html',{'form':form})

def board_detail2(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'board_detail2.html', {'board':board})


###
def view_list(request):
    boards = Board.objects.all().order_by('-id')
    return render(request, 'noticeBoard.html',{"boards":boards})

def view_list2(request):
    boards = Board.objects.all().order_by('-id')
    return render(request, 'noticeBoard2.html',{"boards":boards})

def view_detail(request,pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'detailBoard.html', {'board':board})




### url, github 참고 https://parkhyeonchae.github.io/2020/04/08/django-project-21/
class NoticeListView(ListView):
    model = Notice
    paginate_by = 5
    template_name = 'notice_list.html'
    context_object_name = 'notice_list'

    def get_queryset(self):
        notice_list = Notice.objects.order_by('-id')
        return notice_list

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

def notice_detail_view(request,pk):
    notice = get_object_or_404(Notice, pk=pk)
    context = {
        'notice' : notice,
    }
    return render(request, 'notice_detail.html', context)

def notice_write_view(request):
    if request.method == "POST":
        form = NoticeWriteForm(request.POST)
        #user = request.session['user_id']
        #user_id = User.objects.get(uesr_id = user)
        
        if form.is_valid():
            notice = form.save(commit = False)
            #notice.writer = user_id
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeWriteForm()

    return render(request,"notice_write.html", {'form': form})

