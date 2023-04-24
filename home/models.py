from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class catgories(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     sports=models.BooleanField(default=False)
     healthandmedicine=models.BooleanField(default=False)
     education=models.BooleanField(default=False)
     technology=models.BooleanField(default=False)
     entertainment=models.BooleanField(default=False)
     tradeandprofessional=models.BooleanField(default=False)
     daily=models.BooleanField(default=False)
     weekely=models.BooleanField(default=False)
     created = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
         return self.user.username
         
     
     
class feedback(models.Model):
    name=models.CharField(max_length=15)
    email=models.CharField(max_length=20)
    phone=models.CharField(max_length=12)
    content=models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

class filesys(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='files') 
    
    
    def __str__(self):
        return self.user.username              