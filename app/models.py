# coding=utf8

import uuid
from django.db import models
import django.utils.timezone as timezone


# 用户
class UserInfo(models.Model):
	user_id = models.BigAutoField(primary_key=True)
	username = models.CharField("用户名", max_length=128, blank=False)
	password = models.CharField("密码", max_length=128, blank=False)
	email = models.CharField("邮箱", max_length=128, blank=True)
	login_time = models.IntegerField(blank=True, null=True)
	is_superuser = models.BooleanField("是否超级用户", blank=True)
	description = models.CharField("描述", max_length=128, blank=True)

	def __str__(self):
		return self.username

# 上传文件的信息
class UploadFileInfo(models.Model):
	file_name = models.CharField("文件名", max_length=128, blank=False)
	file_path = models.CharField("文件完整路径", max_length=128, blank=False)
	file_size = models.CharField("文件大小", max_length=128, blank=False)
	upload_time = models.DateTimeField("文件上传的日期和时间", max_length=128, default=timezone.now)
	upload_user = models.CharField("上传文件的用户", max_length=128, blank=True)
	def __str__(self):
		return self.file_name