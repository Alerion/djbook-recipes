from utils.extjs import RpcRouter

class MainApiClass(object):
    
    def hello(self, name, user):
        return {
            'msg': 'Hello %s!' % name
        }
    
    hello._args_len = 1
        
class Router(RpcRouter):
    
    def __init__(self):
        self.url = 'main:router'
        self.actions = {
            'MainApi': MainApiClass()
        }
        self.enable_buffer = 50
