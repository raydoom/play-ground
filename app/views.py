from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views import View
import json, os, time
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from app.models import UserInfo, UploadFileInfo


# 返回json示例
class JsonResponseView(View):
	def get(self, request):
		request.session['islogin'] = True
		request.session['user'] = 'ma'
		dict = {'status': 'succ', 'msg': 'ok'}
		dict1 = {'status': 'failed', 'msg': 'no ok'}
		l = UserInfo.objects.filter(username='maxd4').first().description
		print (l[1])


		data = []
		#queryset = UserInfo.objects.filter(user_id='06d5e2c5-02e8-4bc2-b5cb-e9db0a32594f')
		queryset = UserInfo.objects.all()
		serializer_json = serializers.serialize('json', queryset)
		serializer_data = json.loads(serializer_json)
		for query_res in serializer_data:
			data.append(query_res['fields'])

		return JsonResponse(data, safe=False)


# 文件上传接口
class UploadFileView(View):
	def get(self, request):
		return JsonResponse({'status': 'succ'})
		
	def post(self, request):
		request.session['user'] = 'ma'
		file =request.FILES.get("file", None) # 获取上传的文件，如果没有文件，则默认为None 
		if not file: 
			return JsonResponse({'status': 'failed', 'msg': 'no files for upload!'})
		file_dir_root = "C:/Users/ma/Downloads/upload/"
		file_save_path = time.strftime("%Y/%m/%d")
		file_full_path = file_dir_root + file_save_path
		if not os.path.exists(file_full_path):
			os.makedirs(file_full_path)
		with open(os.path.join(file_full_path,file.name),'wb+') as destination: # 打开特定的文件进行二进制的写操作 
			for chunk in file.chunks():      # 分块写入文件 
				destination.write(chunk)
		#destination.close()
		upload_user = request.session.get('user')
		UploadFileInfo.objects.create(
			file_name=file.name,
			file_path=file_save_path+'/'+file.name,
			file_size=file.size,
			upload_user=upload_user
			)
		return JsonResponse({'status': 'succ', 'msg': 'ok'})

# 文件下载
class DownloadFileView(View):
	def get(self, request):
		file_path = request.GET.get('file_path')
		file_name = request.GET.get('file_name')
		if not file_path:
			res_code = 'mi0002'
			res_msg = '文件路径不能为空'
			res_state = 'fail'
		else:		
			file_directory_root = "C:/Users/ma/Downloads/upload/"
			file_full_path = file_directory_root + file_path
			file = open(file_full_path, 'rb')
			response = FileResponse(file)
			response['Content-Type'] = 'application/octet-stream'
			response['Content-Disposition'] = 'attachment;filename=' + file_name
			return (response)

# 解析post传递的json数据
'''
解析使用下面方式发送的post数据
curl -H "Content-Type:application/json" -X POST --data '{"Head":{"channel":"01","version":"1.0","service":"userLogin","sid":"","cReqTime":"2019-03-06 14:04:59.155"},"Body":{"userLogin":{"loginId":"18615120801","pwd":"mm121001","imageCode":"8888","isRemembere":true}}}' 192.168.0.139:8001/api/v1.0/resolve_json/
'''
class ResolveJsonView(View):
	def post(self, request):
		data = json.loads(request.body.decode())
		print (data.get('Head').get('version'))
		return JsonResponse(data, safe=False)

# 分页数据以json格式返回
class PaginatorJsonView(View):
	def get(self, request):
		queryset = UserInfo.objects.all()
		print (len(queryset))
		row_per_page = 3  # 每页3条数据
		paginator = Paginator(queryset, row_per_page)
		page = request.GET.get('page', 1)
		try:
			current_page = paginator.page(page)
		except PageNotAnInteger:  # If page is not an integer, deliver first page.
			current_page = paginator.page(3)
		except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
			current_page = paginator.page(paginator.num_pages)
		print ('-----------------')
		print (current_page.number) # 当前返回的页面的页码
		print (paginator.num_pages) # 总共分页数目

		page_data = {}
		data = []
		serializer_json = serializers.serialize("json", current_page)
		serializer_data = json.loads(serializer_json)
		for query_res in serializer_data:
			data.append(query_res['fields'])
		page_data['data'] = data
		page_data['page_number'] = current_page.number
		page_data['num_pages'] = paginator.num_pages
		return JsonResponse(page_data, safe=False)

object_list = {'UserInfo': UserInfo, 'UploadFileInfo': UploadFileInfo}
# json api入口处理函数
class JsonApiMainView(View):
	def get(self, request):
		data = json.loads(request.body.decode())
		query = data.get('body').get('query')
		query_result = {}
		for q in query:
			object_name_o = q.get('object')
			object_name = object_list.get(object_name_o)
			object_filter = q.get('filter')
			object_field = tuple(q.get('field'))
			result = object_name.objects.filter(**object_filter).values(*object_field)
			result = list(result)
			query_result[object_name_o] = result
		return JsonResponse(query_result, safe=False)