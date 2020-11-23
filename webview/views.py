from rest_framework import viewsets
from webview.serializers import booksSerializer,UserSerializer, GroupSerializer
from webview.models import books
import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse   #基本的伺服器回復
from django.http import HttpResponseRedirect   #伺服器的路徑進行重定向
from django.contrib import auth              #導入Django內建認證函數
from django.contrib.auth.decorators import login_required              #導入Django login_requirement
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework import pagination
from rest_framework import permissions
from django.contrib.auth.models import User, Group


# Create your views here.
def index(request):
    return render(request,'index.html')

#登錄的行為
def login_action(request):
    if request.method == 'POST':    #針對index網頁上提交的表單行為，做處理
        username=request.POST.get('username','')    #針對index網頁提交的username的資料，取得username的資訊
        password=request.POST.get('password','')    #針對index網頁提交的password的資料，取得password的資訊
        user=auth.authenticate(username=username,password=password)   #使用authenticate()函數認證得到使用者名字和密碼(如果輸入正確，會回傳正確物件)
        #if username == 'admin' and password == 'admin123':   #針對index網頁提交的的資料，判定資料是否正確
        if user is not None:                                  
            auth.login(request,user)                          #登錄
            request.session['user']=username                   #將session資訊記錄到瀏覽器
            #return HttpResponse('login success!')            #如果成功的話，伺服器直接回傳login success
            #return HttpResponseRedirect('/event_manage/')     #如果成功的話，伺服器路徑直接進行重定向到event_manage
            response=HttpResponseRedirect('/home/')     #將伺服器路徑直接進行重定向到event_manage的事件由response使用
            #response.set_cookie('user',username,3600)         #新增瀏覽器的cookie<set_cookie('cookie的名稱',使用者登錄頁上的資訊,保持時間)在登錄成功後，會在瀏覽器新增cookie的資訊>
            #request.session['user']=username                   #將session資訊記錄到瀏覽器
            #return response
            return response
        else:                                                 #如果失敗的話，伺服器直接島到index.html,並告訴各位密碼或使用者錯誤
            return render(request,'index.html',{'error':'username or password error'})



class booksViewSet(viewsets.ModelViewSet):
    queryset=books.objects.all()
    serializer_class=booksSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create your views here.
@login_required   
def home(request):
    # return HttpResponse("Hello Django")   #直接伺服器回復
    book_list=books.objects.all()
    #bkname=request.session.get('title','')
    return render(request,"home.html",{"books":book_list})    #指向要求的網頁

@login_required 
def search_title(request):
    #username=request.session.get('user','')
    search_name=request.GET.get("title","")
    book_list=books.objects.filter(title__contains=search_name)
    return render(request,"home.html",{"books":book_list}) #抓取cookie值

@login_required 
def ytindex(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }
    
    return render(request, 'search/ytindex.html', context)

#退出登錄
@login_required
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/')
    return response