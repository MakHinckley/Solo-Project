from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request,'register.html')

def registrationVal(request):
    if request.method=="POST":
        errors= User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')

        hash_pw= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name= request.POST['first_name'],
            last_name= request.POST['last_name'],
            email= request.POST['email'],
            password=hash_pw
        )
        request.session['logged_user']=new_user.id
        return redirect('/homepage')
    return redirect('/register')

def loginVal(request):
    if request.method == "POST":
        user=User.objects.filter(email= request.POST['email'])
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/homepage')
        messages.error(request, "Email or Password are incorrect.")
    return redirect("/login")

def homepage(request):
    context={
        'logged_user': User.objects.get(id=request.session['logged_user']),
    }
    return render(request, 'homepage.html', context)

def userAcct(request):
    context={
        'logged_user': User.objects.get(id=request.session['logged_user']),
    }
    return render(request, 'account.html', context)

def parkPage(request, park_id):
    one_park= Park.objects.get(id= park_id)
    all_img=Park.objects.all()
    context={
        'park':one_park,
        'park_image':all_img
    }
    return render(request, 'parkPage.html',context)

def parks(request):
    
    context={
        'all_parks': Park.objects.all(),
        
    }
    return render(request,'parks.html', context)

def edit(request):
    return render(request,'edit.html')

def update(request):
    errors= User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for user, value in errors.items():
            messages.error(request,value)
            
        return redirect('/user/edit') 
    else:
        update= User.objects.get(id= request.session['logged_user'])
        update.first_name=request.POST['first_name']
        update.last_name=request.POST['last_name']
        update.email=request.POST['email']
        update.password=request.POST['password']
        update.save()
    return redirect('/user/account')

def deletePage(request):
    user=User.objects.get(id=request.session['logged_user'])
    user.delete()
    return redirect('/login')

def favorite_park(request, park_id):
    user=User.objects.get(id=request.session['logged_user'])
    park=Park.objects.get(id=park_id)
    park.users_favorited.add(user)
    for parks in park.users_favorited:
        if park==True:
            request.POST['park.users_favorited']

    return redirect('/homepage')
    

def logout(request):
    request.session.flush()
    return redirect('/login')

