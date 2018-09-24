# -*- coding:utf-8 -*-
from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from utils.check_code import create_validate_code
from django import forms
from django.forms import fields
from django.forms import widgets
from user import models
import time
import datetime
import re
import json

# Create your views here.
class User(forms.Form):
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )
class Newuser(forms.Form):
    username=fields.CharField(max_length=12,min_length=3,error_messages={'required':'用户名不能为空','max_length':'用户名长度不能12','min_length':'用户名长度不能小于3'},
                              widget=widgets.Input(attrs={'type':"text",'class':"form-control",'name':"username",'id':"username",'placeholder':"请输入用户名"}))
    email=fields.EmailField(error_messages={'required':'邮箱不能为空','invalid':'邮箱格式不正确.'}, widget=widgets.Input(attrs={'type':"email",'class':"form-control",'name':"email",'id':"email",'placeholder':"请输入邮箱名"}))
    password=fields.CharField(max_length=12, min_length=6,
                               error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                               'min_length': '密码长度不能小于6'},
                              widget=widgets.Input(
                                  attrs={'type': "password", 'class': "form-control", 'name': "password", 'id': "password",
                                         'placeholder': "请输入密码"})
                              )
    confirm_password=fields.CharField(max_length=12, min_length=6,
                               error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                               'min_length': '两次密码不一致'},
                                      widget=widgets.Input(
                                          attrs={'type': "password", 'class': "form-control", 'name': "confirm_password",
                                                 'id': "confirm_password",
                                                 'placeholder': "请重新输入密码"})
                                      )
def login(request):
        """
        登陆
        :param request:
        :return:
        """
        # if request.method == "POST":
        #     if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
        #         pass
        #     else:
        #         print('验证码错误')
        er = ''
        s = ''
        if request.method == 'GET':
            obj = User()
            return render(request, 'login.html', {'obj': obj})
        if request.method == 'POST':
            obj = User(request.POST)
            code = request.POST.get('check_code')
            auto = request.POST.get('auto')
            a=request.POST.get('s')
            if auto:
                request.session.set_expiry(2419200)
            else:
                pass
            if code.upper() == request.session['CheckCode'].upper():
                u = request.POST.get('username')
                t1 = models.User.objects.filter(username=u)
                if t1:
                    pwd = request.POST.get('password')
                    if pwd == t1[0].pwd:
                        if a=='学生' and t1[0].user_role==1:
                            request.session['user'] = u
                            request.session['is_login'] = True
                            request.session['pwd'] = pwd
                            request.session['role']=1
                            return redirect('/sign/0')
                        elif a == '老师' and t1[0].user_role==0:
                            request.session['user'] = u
                            request.session['is_login'] = True
                            request.session['pwd'] = pwd
                            request.session['role'] = 0
                            return redirect('/teacher/')
                        else :
                            s = '''
                                                 <script>alert('请选择正确的角色!!!');</script>
                                                 '''


                    else:
                        s = '''
                      <script>alert('密码错误!!!请重新输入!!!');</script>
                      '''
                else:
                    s = '''
               <script>alert('该用户名不存在!!!请检查是否正确!!!');</script>
                                    '''

            else:
                er = '验证码错误'
            return render(request, 'login.html', {'obj': obj, 'er': er, 's': s})
def logout(request):
    request.session.clear()
    obj=User()
    return render(request,'login.html',{'obj':obj})
def register(request):
    """
    注册
    :param request:
    :return:
    """
    er=''
    if request.method=='GET':
        obj=Newuser()
        return render(request, 'register.html',{'obj':obj,'er':er})
    if request.method == 'POST':
       try:
        obj=Newuser(request.POST)
        r=obj.is_valid()
        if r:
            code = request.POST.get('check_code')
            if code.upper() == request.session['CheckCode'].upper():
                user=request.POST.get('username')
                email=request.POST.get('email')
                a=request.POST.get('s')

                u = models.User.objects.filter(username=user)
                if u:
                    s='''
                    <script>alert('用户名已经存在，请从新输入用户名！');
                </script>
                    '''
                else:
                    pwd1=request.POST.get('password')
                    pwd2=request.POST.get('confirm_password')
                    if pwd1!=pwd2:
                        s='''
                        <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                    else:
                        if a=='学生':
                         models.User.objects.create(username=user,pwd=pwd1,email=email,user_role=1)
                        else:
                            models.User.objects.create(username=user, pwd=pwd1, email=email, user_role=0)

                        s='''
                        <script>alert('注册成功！');
                        </script>'''
                return render(request,'register.html',{'obj':obj,'er':er,'s':s})
            else:
                er='验证码错误'
                return render(request,'register.html',{'obj':obj,'er':er})

        else:
            s='''
            <script>alert('信息格式不正确,注册失败！');
                </script>'''
            return render(request,'register.html',{'obj':obj,'er':er,'s':s})
       except:
           s='''
           <script>alert('意外出错！！！！');</script>'''
           return render(request,'register.html',{'s':s})
def check_code(request):
           """
           验证码
           :param request:
           :return:
           """
           # stream = BytesIO()
           # img, code = create_validate_code()
           # img.save(stream, 'PNG')
           # request.session['CheckCode'] = code
           # return HttpResponse(stream.getvalue())

           # data = open('static/imgs/avatar/20130809170025.png','rb').read()
           # return HttpResponse(data)

           # 1. 创建一张图片 pip3 install Pillow
           # 2. 在图片中写入随机字符串
           # obj = object()
           # 3. 将图片写入到制定文件
           # 4. 打开制定目录文件，读取内容
           # 5. HttpResponse(data)

           stream = BytesIO()
           img, code = create_validate_code()
           # f=open('cc.png','wb')
           # img.save(f,'PNG')
           img.save(stream, 'PNG')
           request.session['CheckCode'] = code
           return HttpResponse(stream.getvalue())
           # return HttpResponse(open('cc.png','rb').read())
def teacher(request):
    f=request.session.get('is_login',None)
    role=request.session.get('role',None)
    user = request.session.get("user",None)
    if f :
     if role==0:
       #通过老师id查询他的班级
       tUser = models.User.objects.filter(username=user)[0]
       class_=models.Class.objects.filter(teacher_id = tUser.pk)
       return render(request,'teacher.html',{'c':class_})
     else:
         return HttpResponse('学生无法查看')
    else:
        return  HttpResponse("请先登录")
def classroom(request,nid):
    f = request.session.get('is_login', None)
    role = request.session.get('role', None)
    user = request.session.get("user", None)
    if f and role == 0:
      # nid=int(nid)
      if request.method=='GET':
        obj=models.kaoqing.objects.filter(class_id_id=nid).order_by('-signtime')
        return render(request,'classroom.html',{'obj':obj,'nid':nid})
      elif request.method=='POST':
          time=request.POST.get("time")
          print(time)
          obj = models.User.objects.filter(user_role=1)
          return render(request, 'classroom.html', {'obj': obj,'nid':nid})
def information(request):
    f = request.session.get('is_login', None)
    role = request.session.get('role', None)
    user = request.session.get("user", None)
    if f:
      if role==0:
       if request.method=='GET':
                obj=models.User.objects.filter(username=user).first()
                return render(request,'information.html',{'obj':obj})
       elif request.method=='POST':
                 r_name=request.POST.get('realname')
                 email=request.POST.get('email')
                 phone=request.POST.get('phone')
                 models.User.objects.filter(username=user).update(realname=r_name,email=email,phone=phone)
                 obj = models.User.objects.filter(username=user).first()
                 return render(request,'information.html',{'obj':obj})
      elif role==1:
          if request.method == 'GET':
              obj = models.User.objects.filter(username=user).first()
              return render(request, 'information_s.html', {'obj': obj})
          elif request.method == 'POST':
              r_name = request.POST.get('realname')
              email = request.POST.get('email')
              phone = request.POST.get('phone')
              models.User.objects.filter(username=user).update(realname=r_name, email=email, phone=phone)
              obj = models.User.objects.filter(username=user).first()
              return render(request, 'information_s.html', {'obj': obj})
    else:
        obj=User()
        return render(request,'login.html')
def password(request):
    f=request.session.get('user',None)
    role = request.session.get('role', None)
    user = request.session.get("user", None)
    error=''
    if f:
      if role==0:
        if request.method=='GET':
            obj=models.User.objects.filter(username=user)
            return render(request,'password.html',{'obj':obj,'error':error})
        elif request.method=='POST':
            oldpwd=request.POST.get('oldpwd')
            new1=request.POST.get('newpwd1')
            new2=request.POST.get('newpwd2')
            print(oldpwd)
            obj=models.User.objects.filter(username=user).first()
            if oldpwd==obj.pwd:
                 if len(new1)>=6 and len(new1)<=12:
                     if new1==new2:
                         error='修改成功！！请从新登录！！'
                         models.User.objects.filter(username=user).update(pwd=new1)
                     else:
                         error='两次密码不一致！！'
                 else:
                     error='密码长度必须大于六位小于十二位！！！'
            else:
                error='原密码不正确！！！'

            return render(request, 'password.html', {'obj': obj,'error':error})
      elif role==1:
          if request.method == 'GET':
              obj = models.User.objects.filter(username=user)
              return render(request, 'password_s.html', {'obj': obj, 'error': error})
          elif request.method == 'POST':
              oldpwd = request.POST.get('oldpwd')
              new1 = request.POST.get('newpwd1')
              new2 = request.POST.get('newpwd2')
              print(oldpwd)
              obj = models.User.objects.filter(username=user).first()
              if oldpwd == obj.pwd:
                  if len(new1) >= 6 and len(new1) <= 12:
                      if new1 == new2:
                          error = '修改成功！！请从新登录！！'
                          models.User.objects.filter(username=user).update(pwd=new1)
                      else:
                          error = '两次密码不一致！！'
                  else:
                      error = '密码长度必须大于六位小于十二位！！！'
              else:
                  error = '原密码不正确！！！'

              return render(request, 'password_s.html', {'obj': obj, 'error': error})
    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def students(request,nid):
    f = request.session.get('is_login', None)
    role = request.session.get('role', None)
    user = request.session.get("user", None)
    if f and role == 0:
        obj=models.S_class.objects.filter(Class_id=nid)
        return render(request,'student_informations.html',{'obj':obj})
    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def kaoqing(request,nid):
    f = request.session.get('is_login', None)
    role = request.session.get('role', None)
    user = request.session.get("user", None)
    if f and role==1:
        if request.method=='GET':
             nid=int(nid)
             i=models.User.objects.filter(username=user).first()
             obj=models.S_class.objects.filter(Student_id=i.id)
             if nid==0:
               obj2 = models.kaoqing.objects.filter(Student_id=i.id).order_by('-signtime')
             else:
                 obj2=models.kaoqing.objects.filter(Student_id=i.id,class_id=nid).order_by('-signtime')
             return  render(request,'kaoqing.html',{'obj':obj,'nid':nid,'obj2':obj2})
        elif request.method=='POST':
            nid = int(nid)
            i = models.User.objects.filter(username=user).first()
            obj = models.S_class.objects.filter(Student_id=i.id)
            day=request.POST.get('time')
            date_from=day+' 00:00:00'
            date_to=day+' 24:00:00'
            if nid == 0:
                obj2 = models.kaoqing.objects.filter(Student_id=i.id,signtime__range=(date_from,date_to)).order_by('-signtime')
            else:
                obj2 = models.kaoqing.objects.filter(Student_id=i.id, class_id=nid,signtime__range=(date_from,date_to)).order_by('-signtime')
            return render(request, 'kaoqing.html', {'obj': obj, 'nid': nid,'obj2':obj2})

    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def qiandao(request):
    f = request.session.get('is_login', None)
    role = request.session.get('role', None)
    user = request.session.get("user", None)
    if f:
        obj2=models.User.objects.filter(username=user).first()
        ret={'status':True,'data':None,'error':None}
        r=request.POST.get('yanzheng')
        nid=request.POST.get('nid')
        time = datetime.date.today()
        # time2=datetime.time()
        nid=int(nid)
        print(r, nid,time)
        if nid==0:
            ret['status']=False
            ret['error']='请选择班级开始签到！！当前班级不明确！！'
        else:
            obj=models.Yanzheng.objects.filter(number=r,time=time,class_a_id=nid).last()
            if obj:
                models.kaoqing.objects.create(Student_id_id=obj2.id,class_id_id=nid,signtime=time,s_id=1)
                ret['error']='签到成功'
            else:
                ret['status']=False
                ret['error']='验证码错误！！签到失败！！'
        return HttpResponse(json.dumps(ret))
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})
def yanzheng(request):
    ret={'status':True,'data':None,'error':None}
    r=request.POST.get('r')
    nid=request.POST.get('nid')
    print(nid)
    time=datetime.date.today()
    if r and time:
        ret['error'] = '生成验证码成功'
        models.Yanzheng.objects.create(number=r,time=time,class_a_id=nid)
    else:
        ret['status']=False
        ret['error']='未成功'
    return HttpResponse(json.dumps(ret))






