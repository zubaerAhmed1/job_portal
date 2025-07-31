# core/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    #path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    #path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Job-related
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),

    # Application-related
    path('jobs/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:app_id>/status/', views.change_application_status, name='change_application_status'),
]
