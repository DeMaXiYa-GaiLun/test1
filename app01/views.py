import os

from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse,Http404
from .models import Owner,Goods
import redis

# Create your views here.
red = redis.Redis(host='127.0.0.1',port=6379,db=1)

# def check_login(func):
#   def inner(request,*args,**kwargs):
#     condition = red.get('name')
#     if condition:
#       return func(request, *args, **kwargs)
#     else:
#       return redirect('/login/')
#   return inner




def register(request):
  if request.method=='GET':
    return render(request,'register.html')
  if request.method == 'POST':
    name = request.POST.get('name')
    password = request.POST.get('password')
    if not Owner.objects.filter(name=name,password=password).first():
      red.set('name',name)
      h1 = Owner.objects.create(name=name,password=password)
      h1.save()
      return redirect('/index/')
    else:
      return HttpResponse('注册失败')

def login(request):
  if request.method =='GET':
    return render(request,'login.html')
  if request.method =='POST':
    name = request.POST.get('name')
    password = request.POST.get('password')
    if Owner.objects.filter(name=name, password=password).first():

      red.set('name',name)
      print('zheli',red.get('name'))
      return redirect('/index/')
    else:
      return HttpResponse('登录失败')

def index(request):
  user = red.get('name')
  if not user:
    user = None
    owner = Owner.objects.all()
    List = []
    for i in owner:
      dict={}
      goods = Goods.objects.filter(owner=i.id).all()
      for j in goods:
        print(j.name)
        dict['name'] = i.name
        dict['goods_name'] = j.name
        dict['price'] = j.price
        dict['picture'] = '/static/'+j.picture+'.jpg'
        List.append(dict)
    return render(request,'index.html',{'data':List,'name':user})
  else:
    user = user.decode('UTF-8')
    i = Owner.objects.filter(name=user).first()
    goods = Goods.objects.filter(owner=i).all()
    List=[]
    for j in goods:
      dict = {}
      dict['name'] = user
      dict['goods_name'] = j.name
      dict['price'] = j.price
      dict['picture'] = '/static/'+j.picture+'.jpg'
      print('app01/static/'+j.picture+'.jpg')
      List.append(dict)
    return render(request, 'index.html', {'data': List,'name':user})

# @check_login
def add(request):
  user = red.get('name')
  if request.method=='GET':
    return render(request,'add.html')
  if request.method == 'POST':
    name = request.POST.get('name')
    price = request.POST.get('price')
    picture = request.FILES.get('pic')
    os_path = os.path.dirname(os.path.dirname(__file__))+'/static/' + str(picture) +'.jpg'
    os_path = os_path.replace('\\', '/')
    file = open(os_path, 'wb')
    for i in picture.chunks():
      file.write(i)
      file.close()

    i = Owner.objects.filter(name=user.decode('UTF-8')).first()
    h1 = Goods.objects.create(name=name,price=price,picture=picture,owner=i)
    h1.save()
    return HttpResponse('添加成功')


def test(request):
  # request.session.flush()
  name = red.set('name','11')
  print(red.get('name'))
  return HttpResponseRedirect('/index/')


# @check_login
def Edit(request):
  name = red.get('name')
  i = Owner.objects.filter(name=name.decode('UTF-8')).first()
  data = Goods.objects.filter(owner=i.id).all()

  return render(request,'edit.html',{'data':data,'name':name.decode('UTF-8')})

def delete(request,pl):
  name = red.get('name')
  h1 = Goods.objects.filter(id=pl).delete()

  return redirect('/edit/')


