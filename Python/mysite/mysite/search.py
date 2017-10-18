# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.http import HttpResponse
from django.shortcuts import render_to_response

# 表单页面
def search_form(request):
	return render_to_response('search_form.html')

# 接收数据请求
def search(request):
	request.encoding='utf-8'
	if 'q' in request.GET:
		message = '您搜索的内容是：' + request.GET['q'	]
	else:
		message = '您提交了空表单'
	return HttpResponse(message)