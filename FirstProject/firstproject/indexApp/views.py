from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def index2(request):
    return render(request, 'index2.html')

def waiting_room(request):
    return render(request, 'waiting_room.html')