# Author: Raines Qiu
from django.conf.urls import url
from myapp import views

urlpatterns = [
    # 用户接口
    # url(r'^userList', views.userList),
    url(r'^login_in', views.login_in),
    url(r'^add_user', views.add_user),
    url(r'^modify_pwd', views.modify_pwd),
    # 博客管理接口
    url(r'^blog_add', views.blog_add),
    url(r'^blog_delete', views.blog_delete),
    url(r'^blog_modify', views.blog_modify),
    url(r'^blog_list', views.blog_list),
    url(r'^all_blog_list', views.all_blog_list),
    url(r'^blog_detail', views.blog_detail),
    # 分类接口
    url(r'^category_list', views.category_list)
]