# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myapp.models import users, blogs, categories
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import markdown


@csrf_exempt
def userList(request):
    # if request.method == 'GET':
    response = {}
    response['code'] = 0
    response['data'] = serializers.serialize('json', users.objects.all())
    return JsonResponse(response)

# 登录
def login_in(request):
    if request.method == "POST":
        response = {}
        userId = request.POST.get('user_id')
        userPwd = request.POST.get('user_pwd')
        print(request.COOKIES)
        try:
            userLen = users.objects.filter(user_id=userId)
            if len(userLen) != 0: userMsg = users.objects.get(user_id=userId)
            if len(userLen) == 0:
                response['msg'] = '用户不存在'
                response['code'] = 2
            elif check_password(userPwd, userMsg.user_pwd) == False:
                response['msg'] = '密码错误'
                response['code'] = 2
            else:
                request.session['user_id'] = userMsg.id
                response['msg'] = '登录成功'
                response['code'] = 0
                response['user_id'] = userMsg.user_id
                response['user_name'] = userMsg.user_name
        except:
            response = {}
            response['msg'] = '登录失败'
            response['code'] = 1
        return JsonResponse(response)
    else:
        return JsonResponse('错误')


# 退出
def logout(request):
    request.session.flush()
    response = {}
    response['msg'] = '登出成功'
    return JsonResponse(response)

# 新增用户
def add_user(request):
    """
    新增用户
    """
    if request.method == "POST":
        response = {'code': 1, 'msg': None}
        try:
            userId = request.POST['user_id']
            userPwd = request.POST['user_pwd']
            userName = request.POST['user_name']
            userLength = users.objects.filter(user_id=userId)
            if len(userLength) == 0:
                users.objects.create(
                  user_id=userId,
                  user_pwd=make_password(userPwd),
                  user_name=userName,
                )
                response['msg'] = '新增成功'
                response['code'] = 0
            else:
                response['msg'] = '已经存在该用户名，请更改用户名'
                response['code'] = 2
        except:
            response['msg'] = '新增失败'
            response['code'] = 1
        return JsonResponse(response)
    else:
        return JsonResponse('错误')


# 修改密码
def modify_pwd(request):
    """
    修改密码
    """
    if request.method == "POST":
        response = {'code': 1, 'data': None, 'msg': None}
        print(request)
        try:
            userLength = users.objects.filter(user_id=request.POST['user_id'])
            if len(userLength) == 0:
                response['msg'] = '用户不存在'
                response['code'] = 2
            elif len(request.POST.get('user_id')) != 0 and len(request.POST.get('user_pwd')) != 0:
                users.objects.filter(user_id=request.POST['user_id']) \
                    .update(user_pwd=request.POST['user_pwd'])
                response['msg'] = '修改成功'
                response['code'] = 0
            elif len(request.POST.get('user_pwd')) == 0:
                response['msg'] = '密码不能为空'
                response['code'] = 2
        except:
            response['msg'] = '修改失败'
            response['code'] = 1
        return JsonResponse(response)
    else:
        return JsonResponse('错误')

# ========================== #


# 新增博文
def blog_add(request):
    if request.method == "POST":
        response = {}
        try:
            user_id = request.session['user_id']
            title = request.POST['title']
            content = request.POST['content']
            userList = users.objects.filter(id=user_id)
            if len(userList) == 0:
                response['data'] = '未登录'
            user = users.objects.get(id=user_id)
            category_id = request.POST['category_id']
            category = categories.objects.get(id=category_id)
            blogs.objects.create(
                title=title,
                content=content,
                category=category,
                user=user
            )
            response['msg'] = '新增成功'
            response['code'] = 0
        except:
            response['msg'] = '新增失败'
            response['code'] = 1

        return JsonResponse(response)
    else:
        return JsonResponse('错误')

# 编辑博文
def blog_modify(request):
    if request.method == "POST":
        response = {}
        try:
            user_id = request.session['user_id']
            blog_id = request.POST.get('id')
            title = request.POST['title']
            content = request.POST['content']
            userList = users.objects.filter(id=user_id)
            bloglist = blogs.objects.filter(id=blog_id, user_id=user_id)
            if len(userList) == 0:
                response['data'] = '未登录'
            elif len(bloglist) == 0:
                response['data'] = '该博文不存在'
            else:
                user = users.objects.get(id=user_id)
                category_id = request.POST['category_id']
                category = categories.objects.get(id=category_id)
                bloglist.update(
                    title=title,
                    content=content,
                    category=category,
                )
                response['msg'] = '修改成功'
            response['code'] = 0
        except:
            response['msg'] = '修改失败'
            response['code'] = 1

        return JsonResponse(response)
    else:
        return JsonResponse('错误')

# 删除博文
def blog_delete(request):
    if request.method == "POST":
        response = {}
        try:
            user_id = request.session['user_id']
            blog_id = request.POST.get('id')
            list = blogs.objects.filter(id=blog_id, user_id=user_id)
            if len(list) == 0:
                response['msg'] = '已删除'
            else:
                list.delete()
                response['msg'] = '删除成功'
            response['code'] = 0
        except:
            response['msg'] = '删除失败'
            response['code'] = 1

        return JsonResponse(response)
    else:
        return JsonResponse('错误')

# 博文列表
def blog_list(request):
    if request.method == "GET":
        response = {}
        try:
            user_id = request.session['user_id']
            lists = blogs.objects.filter(user_id=user_id)
            print(len(lists), 'lists')
            if len(lists) == 0:
                response['msg'] = '当前无数据'
            else:
                newlist = []
                for list in lists:
                    newlist.append({
                        'id': list.id,
                        'title': list.title,
                        'category_name': list.category.name,
                        'content': list.content,
                        'user_name': list.user.user_name,
                        'edit_date': list.edit_date
                    })
                response['data'] = newlist
            response['code'] = 0
        except:
            response['msg'] = '查询失败'
            response['code'] = 1

        return JsonResponse(response)
    else:
        return JsonResponse('错误')

# 博文列表所有
def all_blog_list(request):
    if request.method == "GET":
        response = {}
        try:
            blog_lists = blogs.objects.all()
            print(len(blog_lists), 'blog_lists')
            if len(blog_lists) == 0:
                response['msg'] = '当前无数据'
            else:
                newlist = []
                for list in blog_lists:
                    newlist.append({
                        'id': list.id,
                        'title': list.title,
                        'category_name': list.category.name,
                        'content': list.content,
                        'user_name': list.user.user_name,
                        'edit_date': list.edit_date
                    })
                response['data'] = newlist
            response['code'] = 0
        except:
            response['msg'] = '查询失败'
            response['code'] = 1

        return JsonResponse(response)
    else:
        return JsonResponse('错误')


# 博文详情
def blog_detail(request):
    if request.method == "POST":
        response = {}
        try:
            user_id = request.session['user_id']
            blog_id = request.POST.get('id')
            list = blogs.objects.filter(id=blog_id, user_id=user_id)
            if len(list) == 0:
                response['msg'] = '无数据'
            else:
                response['data'] = {
                        'id': list[0].id,
                        'title': list[0].title,
                        'category_id': list[0].category.id,
                        'category_name': list[0].category.name,
                        'content': list[0].content,
                        'user_name': list[0].user.user_name,
                        'edit_date': list[0].edit_date
                    }
                response['msg'] = '查询成功'
            response['code'] = 0
        except:
            response['msg'] = '查询失败'
            response['code'] = 1

        return JsonResponse(response)
    else:
        return JsonResponse('错误')

# ========================== #

# 新增分类

# 编辑分类

# 删除分类

# 分类列表
def category_list(request):
    if request.method == 'GET':
        newList = []
        categories_list = categories.objects.all()
        for cate in categories_list:
            newList.append({
                'id': cate.id,
                'name': cate.name,
            })
        response = {}
        response['code'] = 0
        response['data'] = newList
        return JsonResponse(response)
# 分类详情

# ========================== #

# 新增评论

# 删除评论

# 评论列表
