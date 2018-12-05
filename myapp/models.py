# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class users(models.Model):
    """
    用户表
    """
    user_id = models.TextField(verbose_name="用户名", max_length=20)
    user_pwd = models.TextField(verbose_name="密码", max_length=400)
    user_name = models.TextField(verbose_name="昵称", max_length=20)
    head_img = models.CharField(verbose_name="头像", max_length=100)

    def __str__ (self):
        return self.name


class categories(models.Model):
    """
    分类
    """
    name = models.CharField(verbose_name="分类名称", max_length=20)
    name_des = models.CharField(verbose_name="分类描述", max_length=20)

    def __str__(self):
        return self.name

class blogs(models.Model):
    """
    博文表
    """
    title = models.TextField(u"标题", max_length=100)
    content = models.TextField(u"内容", max_length=300)
    user = models.ForeignKey(users, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    edit_date = models.DateField(u"编辑时间", auto_now_add=True)
    # blogs_comment_num = models.IntegerField(verbose_name="评论量")

class comments(models.Model):
    """
    评论表
    """
    # id = models.AutoField(verbose_name="id", max_length=20)
    content = models.CharField(verbose_name="内容", max_length=3000)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    edit_date = models.DateField(verbose_name="评论时间")
    def __str__ (self):
        return self.name

# CASCADE:这就是默认的选项，级联删除，你无需显性指定它。
# PROTECT: 保护模式，如果采用该选项，删除的时候，会抛出ProtectedError错误。
# SET_NULL: 置空模式，删除的时候，外键字段被设置为空，前提就是blank=True, null=True,定义该字段的时候，允许为空。
# SET_DEFAULT: 置默认值，删除的时候，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值。
# SET(): 自定义一个值，该值当然只能是对应的实体了