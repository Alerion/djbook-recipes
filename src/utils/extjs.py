from django.http import HttpResponse
from django.core.urlresolvers import reverse
from inspect import getargspec
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson

class RpcRouterJSONEncoder(simplejson.JSONEncoder):
    """
    JSON Encoder for RpcRouter
    """
    
    def __init__(self, url_args, url_kwargs, *args, **kwargs):
        self.url_args = url_args
        self.url_kwargs = url_kwargs
        super(RpcRouterJSONEncoder, self).__init__(*args, **kwargs)
    
    def _encode_action(self, o):
        output = []
        for method in dir(o):
            if not method.startswith('_'):
                f = getattr(o, method)
                data = dict(name=method, len=getattr(f, '_args_len', 0))
                if getattr(f, '_form_handler', False):
                    data['formHandler'] = True
                output.append(data) 
        return output        
    
    def default(self, o):
        if isinstance(o, RpcRouter):
            output = {
                'type': 'remoting',
                'url': reverse(o.url, args=self.url_args, kwargs=self.url_kwargs),
                'enableBuffer': o.enable_buffer,
                'actions': {}
            }
            for name, action in o.actions.items():
                output['actions'][name] = self._encode_action(action)
            return output
        else:
            return super(RpcRouterJSONEncoder, self).default(o)

class RpcExceptionEvent(Exception):
    """
    This exception is sent to server as Ext.Direct.ExceptionEvent.
    So we can handle it in client and show pretty message for user.
    """
    pass

class RpcRouter(object):
    """
    Router for Ext.Direct calls.
    """
    
    def __init__(self, url, actions={}, enable_buffer=True):
        self.url = url
        self.actions = actions
        self.enable_buffer = enable_buffer    

    def api(self, request, *args, **kwargs):
        """
        This method is view that send js for provider initialization.
        Just set this in template after ExtJs including:
        <script src="{% url api_url_name %}"></script>  
        """
        obj = simplejson.dumps(self, cls=RpcRouterJSONEncoder, url_args=args, url_kwargs=kwargs)
        return HttpResponse('Ext.Direct.addProvider(%s)' % obj)

    def __call__(self, request, *args, **kwargs):
        """
        This method is view that receive requests from Ext.Direct.
        """
        user = request.user
        POST = request.POST

        if POST.get('extAction'):
            #This is request from Ext.form.Form
            requests = {
                'action': POST.get('extAction'),
                'method': POST.get('extMethod'),
                'data': [POST],
                'upload': POST.get('extUpload') == 'true',
                'tid': POST.get('extTID')
            }
    
            if requests['upload']:
                #This is form with files
                requests['data'].append(request.FILES)
                output = simplejson.dumps(self.call_action(requests, user))
                return HttpResponse('<textarea>%s</textarea>' \
                                    % output)
        else:
            try:
                requests = simplejson.loads(request.POST.keys()[0])
            except (ValueError, KeyError):
                requests = []
                            
        if not isinstance(requests, list):
                requests = [requests]
            
        output = [self.call_action(rd, request, *args, **kwargs) for rd in requests]
            
        return HttpResponse(simplejson.dumps(output, cls=DjangoJSONEncoder), mimetype="application/json")    
    
    def action_extra_kwargs(self, action, request, *args, **kwargs):
        """
        Check maybe this action get some extra arguments from request
        """
        if hasattr(action, '_extra_kwargs'):
            return action._extra_kwargs(request, *args, **kwargs)
        return {}
    
    def extra_kwargs(self, request, *args, **kwargs):
        """
        For all method in ALL actions we add request.user to arguments. 
        You can add something else, request for example.
        For adding extra arguments for one action use action_extra_kwargs.
        """
        return {
            'user': request.user
        }

    def call_action(self, rd, request, *args, **kwargs):
        """
        This method checks parameters of Ext.Direct request and call method of action.
        It checks arguments number, method existing, handle RpcExceptionEvent and send
        exception event for Ext.Direct.
        """
        method = rd['method']
        
        if not rd['action'] in self.actions:
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': 'Undefined action class'
            }
        
        action = self.actions[rd['action']]
        args = rd.get('data') or []
        func = getattr(action, method)

        extra_kwargs = self.extra_kwargs(request, *args, **kwargs)
        extra_kwargs.update(self.action_extra_kwargs(action, request, *args, **kwargs))
        
        func_args, varargs, varkw, func_defaults = getargspec(func)
        func_args.remove('self')
        for name in extra_kwargs.keys():
            if name in func_args:
                func_args.remove(name)
        
        required_args_count = len(func_args) - len(func_defaults or [])
        if (required_args_count - len(args)) > 0 or (not varargs and len(args) > len(func_args)):
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': 'Incorrect arguments number'
            }
        
        try:
            return {
                'tid': rd['tid'],
                'type': 'rpc',
                'action': rd['action'],
                'method': method,
                'result': func(*args, **extra_kwargs)
            }
        except RpcExceptionEvent, e:
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': unicode(e)
            }            
