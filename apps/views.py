from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from.models import Users
from .forms import UserCreateForm, UserLoginForm
from .mixins import NotLoginRequiredMixin
from django.contrib.auth import authenticate
from django.views import View
from django.views.generic import (
    ListView, TemplateView, DetailView,
    CreateView, FormView,
)

class IndexView(TemplateView):
    template_name = 'index.html'    

class UserCreateView(NotLoginRequiredMixin, CreateView):
    model = Users
    form_class = UserCreateForm
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']

        password = form.cleaned_data['password']

        if Users.objects.filter(username=username).exists():
            form.add_error('username', 'Bu username ishlatilgan.')
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        return super().form_valid(form)


class UserSigninView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)  

        if user:
            login(self.request, user)
            return redirect(self.success_url)

        form.add_error(None, 'Username yoki parol noto‘g‘ri.') 

        return self.form_invalid(form)
    
class UserLogoutView(View):

    def get(self, request):
        logout(request)
        next_page = ''
        return redirect('/')


def register_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreateForm()
    return render(request, 'your_template.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            pass
    else:
        login_form = UserLoginForm()
    return render(request, 'your_template.html', {'login_form': login_form})
