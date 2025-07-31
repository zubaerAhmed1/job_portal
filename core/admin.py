from django.contrib import admin
from .models import UserRole, Job, Application

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'posted_by', 'created_at']
    search_fields = ['title', 'company_name', 'location']
    list_filter = ['company_name', 'location']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'applied_at']
    search_fields = ['job__title', 'applicant__username']
    list_filter = ['applied_at']
