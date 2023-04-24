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
     
     created = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
         return self.user.username
         
     
     
     