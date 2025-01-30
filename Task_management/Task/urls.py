from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('app-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('app-admin/tasks/create/', views.AdminTaskCreateView.as_view(), name='admin_task_create'),
    path('app-admin/tasks/<int:pk>/edit/', views.AdminTaskUpdateView.as_view(), name='admin_task_edit'),
    path('app-admin/tasks/<int:pk>/delete/', views.AdminTaskDeleteView.as_view(), name='admin_task_delete'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/tasks/create/', views.UserTaskCreateView.as_view(), name='user_task_create'),
    path('user/tasks/<int:pk>/delete/', views.UserTaskDeleteView.as_view(), name='user_task_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]