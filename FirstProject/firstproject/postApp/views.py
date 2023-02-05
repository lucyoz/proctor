from django.shortcuts import render, redirect
from UserApp.models import User
from .forms import FileUploadForm
from .models import FileUpload
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.
def fileUpload(request):
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        user = request.session['user']
        user_id = User.objects.get(username = user)

        if form.is_valid():
            fileupload = form.save()
            fileupload.writer = user_id
            if request.FILES:
                if 'imgfile' in request.FILES.keys():
                    fileupload.filename = request.FILES['imgfile'].name
            fileupload.save()
            return redirect('postApp:post_list')
    else:
        form = FileUploadForm
    return render(request,'fileupload.html',{'form':form})

def post_list(request):
    posts = FileUpload.objects.all()
    return render(request, 'post_list.html', {'posts':posts})

class PostListView(ListView):
    model = FileUpload
    paginate_by = 5
    template_name = 'post_list.html'
    context_object_name = 'posts'

        # 검색 기능 추가
    def get_queryset(self):
        search_keyword = self.request.GET.get('q','')
        search_type = self.request.GET.get('type','')
        posts = FileUpload.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword)>1:
                if search_type=='test_name':
                    search_post_list = posts.filter(test_name__exact=search_keyword)
                return search_post_list
            else:
                messages.error(self.request,'검색어는 2글자 이상 입력해주세요')
        return posts

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


def post_detail_view(request, pk):
    post = get_object_or_404(FileUpload, pk=pk)
    context = {
        'post':post,
    }
    return render(request, 'post_detail.html',context)
