from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from home.models import catgories,feedback,filesys
from django.contrib import messages
import json
import requests
import transformers
from transformers import pipeline
from autoscraper import AutoScraper
import requests
from bs4 import BeautifulSoup
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import PyPDF2
import spacy
import pandas as pd
import string
import unicodedata
import numpy as np
from numpy import random
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
summarizer=pipeline("summarization")
final=[]
def home(request):
    return render(request,'home/home.html')

def feedbackk(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['message']
        
        feed=feedback(name=name,email=email,phone=phone,content=content)
        feed.save()
        return redirect('home')
        
    return render(request,'home/feedback.html')

def clean_text(text):
    printable = set(string.printable)
    cleaned_text = ''.join(filter(lambda x: x in printable, text))
    cleaned_text = unicodedata.normalize('NFKD', cleaned_text).encode('ascii', 'ignore').decode('ascii')
    return cleaned_text

def uploadd(request):
    if request.method== 'POST':
        if  'document' in request.POST:
            print("ye hai")
        else: 
            print("nhi aaya bc")    
        
        document = request.FILES.get('document')
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(request.user.email)
        savefile= FileSystemStorage() 
        name = savefile.save(uploaded_file.name, uploaded_file)# this is the name of file
         #know where to save the file
        d = os.getcwd() #current directory of the project
        file_directory = d+'\files\\'+name
        #return render(request,'home/feedback.html')
        files(request.user.email,uploaded_file.name)
        return redirect('home')
    
    return render(request,'home/upload.html')     
    

def files(email,file):
    #  if request.method == "POST":
    # print("hello")
    if True:
        print("if ke andar hello")
        # file = request.FILES.get('file') 
        # fill=filesys(user=user,file=file)
        # fill.save()
        nlp = spacy.load("en_ner_bc5cdr_md")
        # nlp = spacy.load("en_core_sci_lg")
     
        with open(f'files\{file}','rb') as file:
       
            reader = PyPDF2.PdfReader(file)

            num_pages = len(reader.pages)

            text = ''
            for i in range(num_pages):
                page = reader.pages[i]
                text += page.extract_text()
        
        doc = nlp(text)

        # entities = [(entity.text, entity.label_) for entity in doc.ents]
        # Define the set of allowed characters
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.,')

# Initialize the entities list
        entities = []

# Loop through all the entities in the doc
        for entity in doc.ents:
    # Check if the entity text contains only allowed characters
            if set(entity.text).issubset(allowed_chars):
            # Add the entity text and label to the entities list
                entities.append((entity.text, entity.label_))

        
        df = pd.DataFrame(entities, columns=['Keyword', 'Entity Type'])
        temp=random.randint(1000)
        df.to_excel(f'{temp}.xlsx',index=False)
        
        
        fromaddr = "predict.io.2k22@gmail.com"
        
        toaddr = f"{email}"

        msg = MIMEMultipart()
        msg['From'] = fromaddr

        # storing the receivers email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = "Here are your personalized news summaries :)"

        # string to store the body of the mail
        # body = ''
        # for f in final:
        #     body =body+'\n'+ f
        
        body = "Thank you for using our website, here are the results."
   

        msg.attach(MIMEText(body,'plain'))
        
        filename = f"{temp}.xlsx"
        attachment = open(f'{temp}.xlsx', "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        
        # encode into base64
        encoders.encode_base64(p)
            
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        
            # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, "merwuzzcsxlpzjve")

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()
                     
    
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
      daily=request.POST.get('daily','off')
      weekley=request.POST.get('weekely','off')
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
        
      if daily=="on":
        obj.daily=True
        obj.save()
        
      if weekley=="on":
        obj.weekely=True
        obj.save()  
        
      obj.save()
    print("function call ke phele")    
    mlinfo(request)
    send_email(user.email)
    # return render(request,'home/Categories.html',caty)
    return redirect('home')    #to show cat selcted by user need to send dict and "return render(request,home/cat.html,dict)"
    
def mlinfo(request):
    myuser=request.user
    userr=catgories.objects.filter(user=myuser).order_by('-created').first() #not showing the latest setted category shows the category first selected by user
    if userr:
        if userr.sports==True:
            sportscon=requests.get('https://gnews.io/api/v4/search?q=football&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
            bootstrap(sportscon) 
            
        if userr.healthandmedicine==True:
            healthcon=requests.get('https://gnews.io/api/v4/search?q=disease&lang=en&country=us&max=10&apikey=abbb76e19b5168c131d403f8560f1d0b').json()
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
    
    
    
    print("1jijisjd")
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
    if len(cont)>10:
        y=" "
        for con in cont:
            y=y+con.text
        dictt[f"{i}"]=y
        i=i+1
    print(dictt)
    moti =0
    for j in range(0,1):
        print(len(dictt[f"{j}"]))
        # if moti>2:
        #     break
        if len(dictt[f"{j}"]) <1500:
            continue
        moti=moti+1
        chunksz = [dictt[f'{j}'][i:i+1500] for i in range(0, len(dictt[f'{j}']), 1500)]
        summarized=summarizer(chunksz[0],min_length=200,max_length=250)
        # summarized=summarized.replace(".","")
        print(summarized[0]) 
        print(summarized[0]['summary_text']) 
        final.append(summarized[0]['summary_text'])

def send_email(email):
    # subject='Your Account need to be verifred',
    # message=f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    # email_from=settings.EMAIL_HOST_USER
    # recipient_list=[email]
    # send_mail(subject,message,email_from,recipient_list)
    # instance of MIMEBase and named as p
 
    fromaddr = "predict.io.2k22@gmail.com"
    toaddr = f"{email}"

    msg = MIMEMultipart()
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Here are your personalized news summaries :)"

    # string to store the body of the mail
    body = ''
    for f in final:
        body =body+'\n'+ f
    
    body=body.replace(".","")
        
    msg.attach(MIMEText(body, 'plain'))
    
        # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "merwuzzcsxlpzjve")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()
    
