from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from . import emailAPI
import time

def home(request):
    return render(request,"home.html")

def responseurl(request):
    return HttpResponse("<h1> This is Our AJAX Demo </h1>")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html",{"output":""})
    else:
     # recieve form data to insert
     name=request.POST.get("name")
     username=request.POST.get("username")
     password=request.POST.get("password")
     mobile=request.POST.get("mobile")
     address=request.POST.get("address")
     city=request.POST.get("city")
     gender=request.POST.get("gender")
     info=time.asctime()

     #To send email
    emailAPI.sendMail(username,password)

    p=models.Register(name=name,username=username,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role='user',info=info)
    p.save()



    return render(request,"register.html",{"output":"User register successfully...."})

def checkEmail(request):
 emailid=request.GET.get("emailid")
 result=models.Register.objects.filter(username__contains=emailid)
 if len(result)>0:
   return HttpResponse(1)
 else:
   return HttpResponse(0)

def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(username=vemail).update(status=1)
    return redirect("/login/")

def login(request):
    if request.method=="GET":
        request.session['sunm']=None
        request.session['srole']=None
        return render(request,"login.html",{"output":""})
    else:
        #recieve form data to insert
        username=request.POST.get("username")
        password=request.POST.get("password")

    userDetails=models.Register.objects.filter(username=username,password=password,status=1)
    if len(userDetails)>0:
        request.session['sunm']=userDetails[0].username
        request.session['srole']=userDetails[0].role
        if userDetails[0].role=="admin":
            return redirect("/myadmin/")
        else:
            return redirect("/user/")
    else:
        return render(request,"login.html",{"output":"invalid username and passsword"})
