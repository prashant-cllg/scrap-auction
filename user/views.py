from django.shortcuts import render,redirect
from django.http import HttpResponse
import time
from . import models
from myadmin import models as myadmin_models
from djangoprj import models as djangoprj_models
from django.conf import settings
media_url=settings.MEDIA_URL

def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/funds/':
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)
		return response
	return middleware

def userhome(request):
	return render(request,"userhome.html",{"sunm":request.session['sunm']})

def funds(request):
	paypalURL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
	paypalID = 'sb-zeovy15254966@business.example.com'
	price=100
	#sb-i2kj015324548@personal.example.com
	return render(request,"funds.html",{"sunm":request.session['sunm'],"paypalURL":paypalURL,"paypalID":paypalID,"price":price})

def cancel(request):
	return render(request,"cancel.html",{"sunm":request.session['sunm']})

def payment(request):
	uid=request.GET.get("uid")
	price=request.GET.get("price")
	ob=models.Payment(uid=uid,price=int(price),info=time.asctime())
	ob.save()
	return redirect('/user/success/')
def success(request):
	return render(request,"success.html",{"sunm":request.session['sunm']})


def cpuser(request):
 if request.method=="GET":
  return render(request,"cpuser.html",{"sunm":request.session['sunm'],"output":""})
 else:
  opass=request.POST.get("opass")
  npass=request.POST.get("npass")
  cnpass=request.POST.get("cnpass")
  sunm=request.session['sunm']

  userDetails=djangoprj_models.Register.objects.filter(username=sunm,password=opass)
  if len(userDetails)>0:
    if npass==cnpass:
      djangoprj_models.Register.objects.filter(username=sunm).update(password=cnpass)
      return render(request,"cpuser.html",{"sunm":request.session['sunm'],"output":"Password changed , please login again...."})
    else:
      return render(request,"cpuser.html",{"sunm":request.session['sunm'],"output":"New & confirm new password not matched"})
  else:
    return render(request,"cpuser.html",{"sunm":request.session['sunm'],"output":"Invalid old password , please try again"})


def epuser(request):
	if request.method=="GET":
 		sunm=request.session['sunm']
 		userDetails=djangoprj_models.Register.objects.filter(username=sunm)
 		m,f="",""
 		if userDetails[0].gender=="male":
  			m="checked"
 		else:
  			f="checked"
 		return render(request,"epuser.html",{"sunm":request.session['sunm'],"output":"","userDetails":userDetails[0],"m":m,"f":f})
	else:
		name=request.POST.get("name")
		username=request.POST.get("username")
		mobile=request.POST.get("mobile")
		address=request.POST.get("address")
		city=request.POST.get("city")
		gender=request.POST.get("gender")

	djangoprj_models.Register.objects.filter(username=username).update(name=name,mobile=mobile,address=address,city=city,gender=gender)

	return redirect("/user/epuser/")

def viewbidproduct(request):
	plist=myadmin_models.Addproduct.objects.filter()
	return render(request,"viewbidproduct.html",{"plist":plist,"sunm":request.session['sunm']})

def bid(request):
	if request.method=="GET":
		pid=int(request.GET.get("pid"))
		pDetails=myadmin_models.Addproduct.objects.filter(pid=pid)
		if (time.time()-float(pDetails[0].info))>172800:
			status=1
		else:
			status=0

		bidDetails=models.Bid.objects.filter(pid=pid)
		if len(bidDetails)==0:
			cprice=pDetails[0].baseprice
		else:
			cprice=bidDetails[len(bidDetails)-1].bidprice

		return render(request,"bid.html",{"sunm":request.session['sunm'],"status":status,"pDetails":pDetails[0],"cprice":cprice})
	else:
		pid=request.POST.get("pid")
		bprice=request.POST.get("bprice")
		cprice=request.POST.get("cprice")
		bidprice=request.POST.get("bidprice")

		p=models.Bid(pid=int(pid),bprice=bprice,cprice=cprice,bidprice=bidprice,info=time.asctime())
		p.save()
		return redirect("/user/bid/?pid="+pid)

def transactions(request):
	ob=models.Payment.objects.filter(uid=request.session['sunm'])
	return render(request,"transactions.html",{"ob":ob,"sunm":request.session['sunm']})
