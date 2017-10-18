# -*- coding: UTF-8 -*-
from django.http import HttpResponse

from TestModel.models import Test2

def testdb(request):
	# test1 = Test2(name='runoob',address='西安大路699号')
	# test1.save()

	response =''
	txt=''
	response=Test2.objects.all()
	# filter相当于SQL中的WHERE，可设置条件过滤结果
	response2 = Test2.objects.filter(id=1)
    
    # 获取单个对象
	response3 = Test2.objects.get(id=1)
    
    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
	Test2.objects.order_by('name')[0:2]
    
    #数据排序
	Test2.objects.order_by("id")
    
    # 上面的方法可以连锁使用
	Test2.objects.filter(name="runoob").order_by("id")
    
	for r in response2:
		txt=txt+'name:'+r.name+'| address:'+r.address
	return HttpResponse("<p>"+txt+"</p>")
