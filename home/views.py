from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from home.models import catgories
from django.contrib import messages
import json
import requests
import transformers
from transformers import pipeline
from autoscraper import AutoScraper
import requests
from bs4 import BeautifulSoup
# Create your views here.
summarizer=pipeline("summarization")
def home(request):
    return render(request,'home/home.html')

def feedback(request):
    return render(request,'home/feedback.html')
def cat(request):
    return render(request,'home/Categories.html')

def log(request):
    return render(request,'home/login.html')

def signup(request):
    return render(request,'home/sign_up.html')

def loginn(request):
     if request.method=='POST':
        username=request.POST['name']
        email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['cnfpassword']
        
        #check for user details.
        # if User.objects.filter(username=username).first():
            # messages.error(request,"Username already exists !!")
            # return redirect('home')
        
        if User.objects.filter(email=email).first():
            # messages.error(request,"Email already registered  !!")
            return redirect('home')
        
        if len(username)>20:
            # messages.error(request,"username must be less than 10 char")
            return redirect('home')
        
        # if not username.isalnum() :
        #      messages.error(request,"username sholud contain letters and numbers only")
        #     return redirect('home')
        
        if pass1 !=pass2:
            # messages.error(request,"password donot match")
            return redirect('home')
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        # mesages.success(request,"You have sucessfully login")
        #return redirect('choose') this will call choose and choose will redirect it to home as choose is returing home
        print("yaha pahuche") 
        return redirect("log")  
    
     else:
        return HttpResponse("404-NOT FOUND")
    
def mainlogin(request) :
    if request.method=='POST':
        username=request.POST['emaill']
        loginpass=request.POST['passwordd']
        user=authenticate(username=username,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"sucefully login")
            return render(request,'home/Categories.html')  
        
        else:
            messages.error(request,"invalid crenditals")
            return render(request,'home/login.html')
    else:
        return HttpResponse("404-ERROR")    

def logoutt(request):
    logout(request)
    # messages.success(request,"sucessfully logout")
    return redirect('home')

def choose(request):
    user=request.user
    if request.method=="POST":
    
      sports=request.POST.get('sports','off')
      healthandmedicine=request.POST.get('health','off')
      education=request.POST.get('education','off')
      technology=request.POST.get('technology','off')
      entertainment=request.POST.get('entertainment','off')
      tradeandprofessional=request.POST.get('trade','off')
      
    #   catty=catgories(user=user,sports=sports,healthandmedicine=healthandmedicine,education=education,technology=technology,entertainment=entertainment,tradeandprofessional=tradeandprofessional)
    #   catty.save()
      caty={'sports':sports,'healthandmedicine':healthandmedicine,'education':education,'technology':technology,' entertainment': entertainment,'tradeandprofessional':tradeandprofessional} 
      obj=catgories.objects.create(user=user)
      print(sports)
      if sports=="on":
        obj.sports=True
        obj.save()
        
      if healthandmedicine=="on":
        obj.healthandmedicine=True
        obj.save()    
        
      if education=="on":
        obj.education=True
        obj.save()
        
      if technology=="on":
        obj.technology=True
        obj.save()
        
      if entertainment=="on":
        obj.entertainment=True
        obj.save() 
          
      if tradeandprofessional=="on":
        obj.tradeandprofessional=True
        obj.save()
    
      obj.save()
    print("function call ke phele")    
    mlinfo(request)
    
    # return render(request,'home/Categories.html',caty)
    return redirect('home')    #to show cat selcted by user need to send dict and "return render(request,home/cat.html,dict)"
    
def mlinfo(request):
    myuser=request.user
    userr=catgories.objects.filter(user=myuser).order_by('-created').first() #not showing the latest setted category shows the category first selected by user
    if userr:
        if userr.sports==True:
            sportscon=requests.get('https://gnews.io/api/v4/search?q=cricket&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
            bootstrap(sportscon) 
            
        if userr.healthandmedicine==True:
            healthcon=requests.get('https://gnews.io/api/v4/search?q=hospital&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
            bootstrap(healthcon) 
        
        if userr.education==True:
            educon=requests.get('https://gnews.io/api/v4/search?q=education&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
            bootstrap(educon)     
         
        if userr.technology==True:
            techcon=requests.get('https://gnews.io/api/v4/search?q=technology&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
            bootstrap(techcon) 
        
        if userr.entertainment==True:
            entertainmentcon=requests.get('https://gnews.io/api/v4/search?q=movies&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
            bootstrap(entertainmentcon)    
            
        if userr.tradeandprofessional==True:
            tradecon=requests.get('https://gnews.io/api/v4/search?q=stocks+bitcoin&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()    
            bootstrap(tradecon)  
    
    else:
        return HttpResponse("Please select categories")        


def bootstrap(empt):
    url_set=[]
    for j in range(0,4):
        url_set.append(empt["articles"][j]["url"])
    
    print(url_set)
    dictt={}
    i=0
    temp={}
    for url in url_set:
            html_cont=requests.get(url).text
            soup=BeautifulSoup(html_cont,'html.parser')
            cont=soup.find_all('p')
            title=soup.find_all('h1')
 
            #  print(cont)
    if len(cont)>20:
        y=" "
        for con in cont:
            y=y+con.text
        dictt[f"{i}"]=y
        i=i+1
   

    print(dictt) 
    summarizer=pipeline("summarization")
    summarized=summarizer(dictt["1"],min_length=200,max_length=250)
    print(summarized) 
    