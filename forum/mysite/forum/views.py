from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User
from .models import Post
from .models import Answer
from .models import PostM
from .models import AnswerM
from .models import Zadanie_zamkniete
from .models import Zadanie_otwarte
from .models import zadanie_matematyczne
import random
from django.core.files.storage import FileSystemStorage
from django.db.models import Max
import re





#####################################################
#                                                   #
#   Funkcja sprawdzająca czy user jest zalogowany   #
#                                                   #
#####################################################
def is_user_authenticated(request):
    try:
        if request.session['logged_user'] == 0 or request.session['logged_user'] == "0":
            return False
        else:
            return True
    except KeyError:
        return False


#####################################################
#                                                   #
#      Funkcja zwracająca id zalogowanego usera     #
#                                                   #
#####################################################
def auth_user_id(request):
    if is_user_authenticated(request):
        return request.session['logged_user']
    else:
        return "User not authenticated"


#####################################################
#                                                   #
#   Funkcja zwracająca range zalogowanego usera     #
#                                                   #
#####################################################
def auth_user_rank(request):
    if is_user_authenticated(request):
        user = User.objects.filter(id=auth_user_id(request))[0]
        return user.ranga
    else:
        return 0



#####################################################
#                                                   #
#      Funkcja dodająca nowy post do zadania        #
#                                                   #
#####################################################
def addNewPost(NumberTask,nrWersji):
    taskAdded = zadanie_matematyczne.objects.get(nr_zadania=NumberTask,nr_wersji=nrWersji)
    newPost=PostM(zadanie=taskAdded,tresc=taskAdded.tresc)
    newPost.save()
#####################################################
#                                                   #
#      Funkcja zamieniajaca format dla mathjax      #
#                                                   #
#####################################################
def replace(text):
    newtext=text.replace('\ ',' ')
    newtext=newtext+" "
    newtext=newtext.replace(' \\',' $\\')
    newtext=newtext.replace('} ','}$ ')
    list=re.findall(r'\s[1-z]+[-^]', newtext)
    for i in list:
       newtext = newtext.replace(i,' $'+i[1:len(i)])
    count=newtext.count('$')
    if(count==1):
        newtext=newtext+"$"
    list2=re.findall(r'.*?\$(.*)$.*', newtext)
    print(list2)
    for j in list2:
       tmp=j
       newSubString=tmp.replace(' ','\ ')
       newtext = newtext.replace(j,newSubString)
    return newtext

def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'forum/index.html', context)


def login(request):
    if is_user_authenticated(request):
        return redirect('usersHOME', user_id=auth_user_id(request))
    else:
        context = {'error': ''}

    return render(request, 'forum/login.html', context)


def login_user(request):
    if request.POST:
        try:
            user = User.objects.filter(name=request.POST['login'], password=request.POST['password'])[0]
        except IndexError:
            context = {'cont': "Hfdhshfd", 'error': "Błędne dane logowania"}
            return render(request, 'forum/login.html', context)
        request.session['logged_user'] = user.id
        return redirect('usersHOME', user_id=auth_user_id(request))
    else:
        return redirect('login')


def logout(request):
    request.session['logged_user'] = "0"
    return redirect('login')


def register1(request):
    if is_user_authenticated(request):
        return redirect('usersHOME', user_id=auth_user_id(request))
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'forum/register1.html', context)

def addQuestionView(request,user_id):
    if auth_user_rank(request) != 'admin' or auth_user_rank(request) != 'moderator':
        return render(request, 'forum/error.html', context={'error': 'Brak uprawnień'})
    users = User.objects.filter(id=user_id)

    context = {'users': users}
    
    return render(request, 'forum/addQuestionOpen.html', context)
def addQuestionViewClosedQuestion(request,user_id):
    if auth_user_rank(request) != 'admin' or auth_user_rank(request) != 'moderator':
        return render(request, 'forum/error.html', context={'error': 'Brak uprawnień'})
    users = User.objects.filter(id=user_id)
    context = {'users': users}
    return render(request, 'forum/addQuestionClose.html', context)

def addQuestionOpenToDatabase(request):
    NumberTask = request.POST['numberTask']
    section = request.POST['section']
    set = request.POST['set']
    NumberPoints = request.POST['NumberPoints']
    inputQuestion = request.POST['inputQuestion']
    inputAnswer = request.POST['inputAnswer']
    solution = request.POST['solution']
    inputQuestion=replace(inputQuestion)
    if request.GET.get('image'):
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
    else:
        uploaded_file_url = ""
    version = zadanie_matematyczne.objects.filter(nr_zadania=NumberTask)
    ver=version.aggregate(Max('nr_wersji'))
    newVersion=ver['nr_wersji__max']+1

    newQuestion=zadanie_matematyczne(nr_zadania=NumberTask,nr_wersji=newVersion,rodzaj="otwarte",zestaw=set,tresc=inputQuestion,odp_a="",odp_b="",odp_c="",odp_d="",rozwiazanie=solution,odpowiedz=inputAnswer,dzial=section,punkty=NumberPoints,url=uploaded_file_url)
    newQuestion.save()

    addNewPost(NumberTask,newVersion)

    users = User.objects.filter(id=request.POST["user_id"])
    nameNew='{% url "addQuestionOpenToDatabase" %}'
    context = {'users': users}
    return render(request, 'forum/addQuestionOpen.html', context)

def addQuestionCloseToDatabase(request):
    NumberTask = request.POST['numberTask']
    section = request.POST['section']
    set = request.POST['set']
    NumberPoints = request.POST['NumberPoints']
    inputQuestion = request.POST['inputQuestion']
    inputAnswer = request.POST['inputAnswer']
    inputAnswerA = request.POST['inputAnswerA']
    inputAnswerB = request.POST['inputAnswerB']
    inputAnswerC = request.POST['inputAnswerC']
    inputAnswerD = request.POST['inputAnswerD']
    inputQuestion=replace(inputQuestion)
    if request.GET.get('image'):
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
    else:
        uploaded_file_url = ""
    version = zadanie_matematyczne.objects.filter(nr_zadania=NumberTask)
    ver=version.aggregate(Max('nr_wersji'))
    newVersion=ver['nr_wersji__max']+1

    newQuestion=zadanie_matematyczne(nr_zadania=NumberTask,nr_wersji=newVersion,rodzaj="zamkniete",zestaw=set,tresc=inputQuestion,odp_a=inputAnswerA,odp_b=inputAnswerB,odp_c=inputAnswerC,odp_d=inputAnswerD,rozwiazanie="",odpowiedz=inputAnswer,dzial=section,punkty=NumberPoints,url=uploaded_file_url)
    newQuestion.save()

    addNewPost(NumberTask,newVersion)

    users = User.objects.filter(id=request.POST["user_id"])
    nameNew='{% url "addQuestionOpenToDatabase" %}'
    context = {'users': users}
    return render(request, 'forum/addQuestionOpen.html', context)

def register2(request):
    Name = request.POST['Name']
    Password = request.POST['Password']
    if (Name=="" or Password=="" ):
        msg="Empty,try again"
    else:
        if(User.objects.filter(name=Name).count()==0):
            u = User(name=Name,password=Password,ranga="user")
            u.save()
            msg="User added"
        else:
            msg="User with that name exists,try again"
    context = {'msg': msg}
    return render(request, 'forum/register2.html', context)

def usersHOME(request, user_id):
    if is_user_authenticated(request):
        users = User.objects.filter(id=auth_user_id(request))
        context = {'users': users}
        return render(request, 'forum/usersHome.html', context)
    else:
        return render(request, 'forum/error.html', {'error': auth_user_id(request)})

def user_at_forum(request, user_id):
    users = User.objects.filter(id=user_id)
    posts = Post.objects.all()
    postsM= PostM.objects.all()
    postsToChcekM=PostM.objects.filter(stan="check")
    postsCheched=PostM.objects.filter(stan="")
    context = {'posts': posts,'users': users,'postsM': postsM,'postsToChcekM': postsToChcekM,'postsCheched': postsCheched}
    return render(request, 'forum/userFORUM.html', context)

def math_page(request, user_id):
    users = User.objects.filter(id=user_id)
    context = {'users': users}
    return render(request, 'forum/MATH_PAGE.html', context)

def math_page2(request, user_id):
    users = User.objects.filter(id=user_id)

    r=request.session.get('r')
    r2=request.session.get('r2')
    r3=request.session.get('r3')
    r4=request.session.get('r4')

    r=(random.randint(1,4))
    r2=(random.randint(1,4))
    r3=(random.randint(1,3))
    r4=(random.randint(1,3))

    request.session['r'] = r
    request.session['r2'] = r2
    request.session['r3'] = r3
    request.session['r4'] = r4
   
    zos=zadanie_matematyczne.objects.filter(nr_wersji=r).filter(rodzaj="otwarte",zestaw="zestaw1")
    zzs=zadanie_matematyczne.objects.filter(id=201)|zadanie_matematyczne.objects.filter(id=181)|zadanie_matematyczne.objects.filter(id=180)
    
    context = {'users': users,'zos': zos,'zzs': zzs}
    return render(request, 'forum/MATH_PAGE2.html', context)

def math_page3(request, user_id):
    users = User.objects.filter(id=user_id)

    r=request.session.get('r')
    r2=request.session.get('r2')
    r3=request.session.get('r3')
    r4=request.session.get('r4')

    zos=zadanie_matematyczne.objects.filter(nr_wersji=r).filter(rodzaj="otwarte",zestaw="zestaw1")
    zzs=zadanie_matematyczne.objects.filter(nr_wersji=r2).filter(rodzaj="zamkniete",zestaw="zestaw1")

    odpZ = request.POST.getlist('odpZ')
    odpO = request.POST.getlist('odpO')

    linki = []

    punktyZ=0
    punktyO=0
    punktyMAX=0
    x=0
    for zz in zzs:
      posts= PostM.objects.filter(zadanie=zz.id)
      for post in posts:
        linki.append(post)
      punktyMAX=punktyMAX+1
      if zz.odpowiedz == odpZ[x]:
        punktyZ=punktyZ+1
      x=x+1

    for zo in zos:
      posts= PostM.objects.filter(zadanie=zo.id)
      for post in posts:
        linki.append(post)
      punktyMAX=punktyMAX+2
      x=int(punktyO)/2
      if zo.odpowiedz == odpO:
        punktyO=punktyO+2
    
    punkty=punktyZ+punktyO
      

    context = {'users': users,'zos': zos,'zzs': zzs,'odpO': odpO,'odpZ': odpZ,'punktyMAX': punktyMAX,'punkty': punkty,'linki': linki}
    return render(request, 'forum/MATH_PAGE3.html', context)

def post(request, user_id,post_id):
    users = User.objects.filter(id=user_id)
    posts = Post.objects.filter(id=post_id)
    answers = Answer.objects.filter(post=post_id)
    context = {'posts': posts,'answers': answers,'users': users}
    return render(request, 'forum/posts.html', context)

def postM(request, user_id,post_id):
    users = User.objects.filter(id=user_id)
    postsM = PostM.objects.filter(id=post_id)
    answersM = AnswerM.objects.filter(zadanie=post_id)
    context = {'postsM': postsM,'answersM': answersM,'users': users}
    return render(request, 'forum/postsM.html', context)

def add(request, user_id):
    users = User.objects.filter(id=user_id)
    temat = request.POST['temat']
    tresc = request.POST['tresc']
    for user in users:
        w=user
    error=""
    if (temat=="" or tresc==""):
        error="Empty,try again"
    else:
        q = Post(userP=w,subject=temat,text=tresc)
        q.save()
        error="Post added"

    context = {'users': users,'temat': temat,'tresc': tresc,'error': error}
    return render(request, 'forum/add.html', context)

def delete(request, user_id,post_id):
    users = User.objects.filter(id=user_id)
    posts = Post.objects.filter(id=post_id)
    posts.delete()
    context = {'users': users}
    return render(request, 'forum/delete.html', context)

def odp(request, user_id,post_id):
    users = User.objects.filter(id=user_id)
    posts = Post.objects.filter(id=post_id)
    answers = Answer.objects.filter(post=post_id)
    error=""
    for user in users:
        x=user
    for post in posts:
        y=post
    new_answer = request.POST['comment']
    if (new_answer==""):
        error="Empty,try again"
    else:
        a = Answer(post=y,userA=x,answer=new_answer)
        a.save()
    context = {'posts': posts,'answers': answers,'users': users,'new_answer': new_answer,'error': error}
    return render(request, 'forum/posts.html', context)

def delete_odp(request, user_id,post_id,answer_id):
    users = User.objects.filter(id=user_id)
    posts = Post.objects.filter(id=post_id)
    answers = Answer.objects.filter(id=answer_id)
    answers.delete()
    answers = Answer.objects.filter(post=post_id)
    context = {'posts': posts,'answers': answers,'users': users}
    return render(request, 'forum/posts.html', context)

def odpM(request, user_id,post_id):
    users = User.objects.filter(id=user_id)
    postsM = PostM.objects.filter(id=post_id)
    answersM = AnswerM.objects.filter(zadanie=post_id)
    error=""
    for user in users:
        x=user
    for post in postsM:
        y=post
        y.stan="check"
        y.save()
    new_answer = request.POST['comment']
    if (new_answer==""):
        error="Empty,try again"
    else:
        a = AnswerM(zadanie=y,userA=x,answer=new_answer)
        a.save()
    context = {'postsM': postsM,'answersM': answersM,'users': users,'new_answer': new_answer,'error': error}
    return render(request, 'forum/postsM.html', context)

def delete_odpM(request, user_id,post_id,answer_id):
    users = User.objects.filter(id=user_id)
    postsM = PostM.objects.filter(id=post_id)
    answersM = AnswerM.objects.filter(id=answer_id)
    answersM.delete()
    answersM = AnswerM.objects.filter(zadanie=post_id)
    context = {'postsM': postsM,'answersM': answersM,'users': users}
    return render(request, 'forum/postsM.html', context)

def check(request, user_id,post_id):
    users = User.objects.filter(id=user_id)
    postsM = PostM.objects.filter(id=post_id)
    answersM = AnswerM.objects.filter(zadanie=post_id)
    for post in postsM:
        y=post
        y.stan=""
        y.save()
    context = {'postsM': postsM,'answersM': answersM,'users': users}
    return render(request, 'forum/postsM.html', context)