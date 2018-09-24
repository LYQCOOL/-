from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    realname=models.CharField(max_length=32)
    email=models.EmailField()
    phone=models.CharField(max_length=12)
    user_role=models.IntegerField()#0 老师 1学生
class Class(models.Model):
    teacher_id=models.IntegerField()
    classname=models.CharField(max_length=32)
class S_class(models.Model):
    Student_id=models.ForeignKey(to='User',on_delete=True)
    Class_id=models.ForeignKey('Class',on_delete=True)

class Status(models.Model):
        stasus= models.CharField(max_length=32)
class kaoqing(models.Model):
    Student_id=models.ForeignKey(User,on_delete=True)
    signtime=models.DateTimeField()
    class_id=models.ForeignKey(Class,on_delete=True)
    s=models.ForeignKey(Status,on_delete=True,default=2)
class Yanzheng(models.Model):
    number=models.ImageField()
    time=models.DateField(auto_now=True)
    class_a=models.ForeignKey(Class,on_delete=True)


