# coding=utf-8
# -*- coding:utf-8 -*-
##
# Date: 2015/11/06 (CST)
# Author: Michael Liu (HIT)
# Copyright (c) 2015 liu. All rights reserved.
#

from django.conf.urls import include, url
from django.shortcuts import render, render_to_response
from django.views.generic import *
from django.views.generic.edit import *
from django.shortcuts import redirect
from bookmanagement.models import *


class RedirectTo(object):
    """ redirect View used by instants """
    def __init__(self,url):
        self.url = url

    def as_view(self):
        t_url = self.url
        class Redirect(RedirectView):
            url = t_url

        return Redirect.as_view()


class RestView(object):
    ''' Restful API for Model CRUD operation '''


    def __init__(self,model=None,field=None,success_url=None):
        self.model = model
        self.field = field
        self.success_url = success_url or '../..'



    def urlGroup(self):
        return [url(r'^$',self.asList().as_view()),
                url(r'^create/$',self.asCreate().as_view()),
                url(r'^update/(?P<pk>\d+)/$',self.asUpdate().as_view()),
                url(r'^delete/(?P<pk>\d+)/$',self.asDelete().as_view()),
                url(r'^deleteAll$',self.asDeleteAll().as_view()),
                url(r'^detail/(?P<pk>[-\w]+)/$', self.asDetail().as_view()),
                ]
    def asDeleteAll(self):
        t_model = self.model
        class DeleteAll(View):
            model = t_model
            def post(self, request, *args, **kwargs):
                deleteList = [ int(key) for key in request.POST if request.POST[key] == u'on']
                self.model.objects.filter(pk__in=deleteList).delete()
                return redirect('./')

        return DeleteAll

    def asDetail(self):
        t_model = self.model
        class Detail(DetailView):
            model = t_model

        return Detail

    def asList(self):
        t_model = self.model
        class List(ListView):
            model = t_model

        return List


    def asCreate(self):
        t_model = self.model
        t_field = self.field
        t_success_url = self.success_url

        class Create(CreateView):
            model = t_model
            fields = t_field
            success_url = '../'

        return Create

    def asUpdate(self):
        t_model = self.model
        t_field = self.field
        t_success_url = self.success_url

        class Update(UpdateView):
            model = t_model
            fields = t_field
            success_url = t_success_url
            template_name_suffix = '_update_form'

        return Update

    def asDelete(self):
        t_model = self.model
        t_success_url = self.success_url

        class Delete(DeleteView):
            model = t_model
            success_url = t_success_url

        return Delete



class BookView(RestView):

    def __init__(self):
        super(BookView,self).__init__(
            model=Book,
            field=['ISBN', "Title", "Publisher", "PublishDate", "Author", "Price"]
        )
        self.searchField= 'Author'


    def urlGroup(self):
        url_array = super(BookView, self).urlGroup()
        url_array.append(url(r'^search', self.asSearch().as_view()))
        return url_array

    def asSearch(self):
        t_model = self.model
        class Search(View):
            model = t_model
            template_name_suffix = '_search'
            def get(self, request, *args, **kwargs):
                queryset = self.model.objects.filter(Author__Name__contains = request.GET[u'search']).all()
                content = {'object_list': queryset,'search_str':request.GET[u'search']}
                return render_to_response('bookmanagement/'+
                                          str.lower(self.model.__name__)+
                                          self.template_name_suffix+'.html'
                                          ,content)
        return Search

