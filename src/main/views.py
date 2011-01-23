from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return direct_to_template(request, 'main/index.html')