from django.shortcuts import render
from django.http import HttpResponseRedirect
from mysite import models
from mysite import forms
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib import messages


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信。"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())


# Create your views here.
def get_example(request):
    try:
        urid = request.GET['user_id']
        urpass = request.GET['user_pass']
        se_byear = request.GET['byear']
        urfcolor = request.GET.getlist('fcolor')
        loveMovie = request.GET['movie']
        if urid != None and urpass == "12345":
            verified = True
        else:
            verified = False
    except:
        urid = None
    years = range(1960, 2021 + 1)
    return render(request, 'get_example.html', locals())


def index(request, pid=None, del_pass=None):
    if 'username' in request.session:
        username = request.session['username']
        usermail = request.session['useremail']
    return render(request, 'index.html', locals())


def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())


def posting(request):
    moods = models.Mood.objects.all()
    message = '如要張貼訊息，則每一個欄位都要填...'
    try:
        user_id = request.POST['user_id']
        user_pass = request.POST['user_pass']
        user_post = request.POST['user_post']
        user_mood = request.POST['mood']
    except:
        user_id = None
        message = '張貼每一則訊息,每個欄位都要填'
    if user_id is not None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = '儲存成功!記得編輯你的密碼[{}],之後才會顯示'.format(user_pass)
    return render(request, 'posting.html', locals())


def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message = "您的訊息已儲存，要等管理者啟用後才看得到喔。"
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message = '如要張貼訊息，則每一個欄位都要填...'
    else:
        post_form = forms.PostForm()
        message = '如要張貼訊息，則每一個欄位都要填... '
    return render(request, 'post2db.html', locals())


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


def logout(request):
    if 'username' in request.session:
        Session.objects.all().delete()
        return redirect("/login/")
    return redirect("/")


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
