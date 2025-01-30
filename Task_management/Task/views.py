from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Task
from .forms import TaskForm, RegisterForm

def home(request):
    return render(request, 'home.html')

# check admin status
def admin_check(user):
    return user.is_staff

# Admin Views
@login_required
@user_passes_test(admin_check, login_url='/login/')
def admin_dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'admin/dashboard.html', {'tasks': tasks})

class AdminTaskCreateView(UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'admin/task_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AdminTaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'admin/task_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff

class AdminTaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'admin/confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff

# User Views
@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'user/dashboard.html', {'tasks': tasks})

# Authentication Views
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

class UserTaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'user/create_task.html'
    success_url = reverse_lazy('user_dashboard')

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)
class UserTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'user/delete_task.html'
    success_url = reverse_lazy('user_dashboard')

    def test_func(self):
        task = self.get_object()
        return task.created_by == self.request.user