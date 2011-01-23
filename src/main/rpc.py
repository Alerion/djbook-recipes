from utils.extjs import RpcRouter
from main.models import Project

class MainApiClass(object):
    
    def hello(self, name, user):
        return {
            'msg': 'Hello %s!' % name
        }
    
    hello._args_len = 1

class ProjectApiClass(object):
    
    def read(self, user):
        qs = Project.objects.all()
        data = [item.store_record() for item in qs]
        return {'data': data}
        
class Router(RpcRouter):
    
    def __init__(self):
        self.url = 'main:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'ProjectApi': ProjectApiClass()
        }
        self.enable_buffer = 50
