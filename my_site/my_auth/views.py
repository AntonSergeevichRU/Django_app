from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.utils.translation import gettext_lazy as _, ngettext


from .models import *
from .forms import *

class AboutMyView(TemplateView):
    template_name = 'my_auth/about_me.html'


class UserListView(ListView):
    template_name = 'my_auth/user_list.html'
    queryset = User.objects.all()
    context_object_name = 'Users'


class DetailUserView(DetailView):
    template_name = 'my_auth/user_detail.html'
    context_object_name = 'Profile'
    queryset = Profile.objects.all()


class UpdateProfile(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or \
               self.request.user.id == self.get_object().user_id

    model = Profile
    form_class = AddAvatarForm
    #fields = 'bio', 'avatar'
    template_name = 'my_auth/user_update_form.html'
    template_name_suffix = '_update_form'


    def get_success_url(self):
        return reverse('my_auth:user_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)




class RegisterUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'my_auth/register.html'
    success_url = reverse_lazy('my_auth:about')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response




class MyLogoutView(LogoutView):
    next_page = reverse_lazy('my_auth:login')

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('ASSSSSS', 'QWERTY', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('ASSSSSS', 'default value')
    return HttpResponse(f'Куки значение: {value!r}')


@permission_required('my_auth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['footbar'] = 'Что то записали и получили'
    return HttpResponse('Установка сессии!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('footbar', 'default')
    return HttpResponse(f'Значение сессии: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})



class HelloView(View):
    welcome = _('Welcome hello world!')
    def get(self, request: HttpRequest):
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_lines = ngettext(
            'one products',
            '{count} products',
            items,
        )
        products_line = products_lines.format(count=items)

        return HttpResponse(f'\n<h2>{self.welcome}</h2>\n\n<h3>{products_line}</h3>')