# -*- coding: utf-8 -*-
from utils.extjs import RpcRouter
from main.models import Project
from django.conf import settings

PROJECTS_ON_PAGE = getattr(settings, 'PROJECTS_ON_PAGE', 10)

class MainApiClass(object):
    
    def hello(self, name, user):
        return {
            'msg': 'Hello %s!' % name
        }
    
    hello._args_len = 1

class ProjectApiClass(object):
    
    def read(self, rdata, user):
        start = int(rdata.get('start', 0))
        end = start + int(rdata.get('limit', PROJECTS_ON_PAGE))      
           
        qs = Project.objects.all()
        data = [item.store_record() for item in qs[start:end]]
        #Возвращаем данные для Ext.ux.stores.ProjectStore
        #Данные в Ext.ux.stores.ProjectStore.root
        #Общее количество в Ext.ux.stores.ProjectStore.totalProperty для
        #отображения постранички
        return {'data': data, 'count': Project.objects.count()}
    
    read._args_len = 1
    
class Router(RpcRouter):
    
    def __init__(self):
        self.url = 'main:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'ProjectApi': ProjectApiClass()
        }
        self.enable_buffer = 50
