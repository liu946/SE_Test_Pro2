# -*- coding:utf-8 -*-
"""booksys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from bookmanagement.views import RestView,BookView,RedirectTo
from bookmanagement.models import Author
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',RedirectTo('./books').as_view()),
    url(r'^books/',include(BookView().urlGroup())),
    url(r'^author/',include(RestView(model=Author,field=["Name", "Age", "Country"]).urlGroup())),

    ## success_url = "success/" 会到本层的success 而 success_url="/success/" 会从网站根开始找
    ## reverse 可以传入，自己起的路由名字，view，或带参数的路由 https://docs.djangoproject.com/en/1.8/ref/urlresolvers/
    ## 此处起名是可以传入url函数的 在文档中为view-name

    # url(r'^author/',include([
    #     url(r'^$',AuthorList.as_view(),name='author_list'),
    #     url(r'^create$',AuthorCreate.as_view()),
    #     url(r'^update/(?P<pk>\d+)/$',AuthorUpdate.as_view(),name="authorupdate"),
    # ]))

]
