from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def index(request):
    context = {
        'PROJECTS_ON_PAGE': getattr(settings, 'PROJECTS_ON_PAGE', 10)
    }
    return direct_to_template(request, 'main/index.html', context)