from django.shortcuts import render
from django.http import HttpResponseRedirect
from mysite import models
from mysite import forms
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request, pid=None, del_pass=None):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    try:
        user = models.User.objects.get(username=username)
        diaries = models.Diary.objects.filter(user=user).order_by('-ddate')
    except:
        pass
    messages.get_messages(request)
    return render(request, 'index.html', locals())


'''
def index(request, pid=None, del_pass=None):
    if 'username' in request.session:
        username = request.session['username']
        usermail = request.session['useremail']
    return render(request, 'index.html', locals())
'''


def login(request):
    if request.method == 'POST':
        login_form = forms.loginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    messages.add_message(request, messages.SUCCESS, '成功登入了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '帳號尚未啟用')
            else:
                messages.add_message(request, messages.WARNING, '登入失敗')
        else:
            messages.add_message(request, messages.INFO, '請檢查輸入的欄位內容')
    else:
        login_form = forms.loginForm()
    return render(request, 'login.html', locals())


'''
def login(request):
    if request.method == 'POST':
        login_form = forms.loginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            try:
                user = models.User.objects.get(name=login_name)
                if user.password == login_password:
                    request.session['username'] = user.name
                    request.session['useremail'] = user.email
                    messages.add_message(request, messages.SUCCESS, '登入成功')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '密碼錯誤請再檢查一次')
            except:
                messages.add_message(request, messages.WARNING, "找不到使用者")
        else:
            messages.add_message(request, messages.INFO, '請輸入必填欄位')
    else:
        login_form = forms.loginForm()
    return render(request, 'login.html', locals())

'''

'''
def logout(request):
    if 'username' in request.session:
        Session.objects.all().delete()
        return redirect("/login/")
    return redirect("/")
'''


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功登出了")
    return redirect('/')


"""
def userInfo(request):
    if 'username' in request.session:
        username = request.session['username']
    else:
        return redirect("/login/")
    try:
        userinfo = models.User.objects.get(name=username)
    except:
        message = "找不到使用者"
    return render(request, 'userInfo.html', locals())
"""


@login_required(login_url='/login/')
def userInfo(request):
    if request.user.is_authenticated:
        username = request.user.username
    try:
        user = User.objects.get(username=username)
        userinfo = models.Profile.objects.get(user=user)
    except:
        pass
    return render(request, 'userinfo.html', locals())


def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
    if request.method == 'POST':
        user = User.objects.get(username=username)
        diaries = models.Diary(user=user)
        diary_form = forms.DiaryForm(request.POST, instance=diaries)
        if diary_form.is_valid():
            messages.add_message(request, messages.INFO, "日記已儲存")
            diary_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, '要張貼日記，每一個欄位都要填...')
    else:
        diary_form = forms.DiaryForm()
    return render(request, 'posting.html', locals())


def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())
