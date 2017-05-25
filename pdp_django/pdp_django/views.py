from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

ERROR_TEMPLATE_NAME = 'error/detail.html'

def custom_400(request):
    return render_to_response(ERROR_TEMPLATE_NAME, {
        'status_code': '400',
        'status_msg': 'bad request',
    }, status=400)

def custom_403(request):
    return render_to_response(ERROR_TEMPLATE_NAME, {
        'status_code': '403',
        'status_msg': 'permission denied',
    }, status=403)

def custom_404(request):
    return render_to_response(ERROR_TEMPLATE_NAME, {
        'status_code': '404',
        'status_msg': 'page not found',
    }, status=404)

def custom_500(request):
    return render_to_response(ERROR_TEMPLATE_NAME, {
        'status_code': '500',
        'status_msg': 'server error',
    }, status=500)

class HomeView(TemplateView):
    template_name = 'home.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)