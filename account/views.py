from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import courses
# Create your views here.


def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method== "POST":
        username=request.POST["username"]
        email=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username ,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Error : Username or Password wrong!! Please try again.")
            return render(request,"account/login.html")
    all_courses = courses.objects.all()
    return render(request,"account/login.html", {'courses': all_courses})

def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        username=request.POST["username"]
        email=request.POST["email"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        password=request.POST["password"]
        repassword=request.POST["repassword"]

        if password==repassword:
            if User.objects.filter(username=username).exists():
                return render(request,"account/register.html",{"error":"The username is already used.Please change username", 
                                                               "username":username,"firstname":firstname,"lastname":lastname,"email":email})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request,"account/register.html",{"error":"The Email is already used.Please change Email",
                                                                   "username":username,"firstname":firstname,"lastname":lastname,"email":email})
                else:
                    user=User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    messages.success(request,"Register successful!")
                    return redirect("login")
        else:
            return render(request,"account/register.html",{"error":"Password and Re-Password doesnot match!!",
                                                           "username":username,"firstname":firstname,"lastname":lastname,"email":email})


    return render(request,"account/register.html")

def logout_request(request):
    # Kullanıcıyı oturumdan çıkar
    logout(request)
    # Oturumu temizle
    request.session.flush()
    return redirect("home")