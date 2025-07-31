from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from .forms import SignUpForm,JobForm,ApplicationForm
from .models import UserRole,Job,Application
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password']
            user.set_password(raw_password)
            user.save()
            role = form.cleaned_data['role']
            UserRole.objects.create(user=user, role=role)

            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'ইউজারনেম বা পাসওয়ার্ড ভুল হয়েছে।')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')




@login_required
def dashboard(request):
    try:
        user_role = request.user.userrole.role
    except UserRole.DoesNotExist:
        logout(request)
        messages.error(request, "Your account is incomplete. দয়া করে আবার সাইনআপ/লগিন করুন।")
        return redirect('login')

    if user_role == 'employer':
        return render(request, 'employer_dashboard.html')
    else:
        return render(request, 'applicant_dashboard.html')



# Post new job
@login_required
def post_job(request):
    if request.user.userrole.role != 'employer':
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('my_jobs')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

# Employer's own jobs
@login_required
def my_jobs(request):
    if request.user.userrole.role != 'employer':
        return redirect('dashboard')

    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'my_jobs.html', {'jobs': jobs})

# All jobs for everyone
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs})

# Job Detail
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})



# Apply to a Job
@login_required
def apply_to_job(request, job_id):
    if request.user.userrole.role != 'applicant':
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Check if already applied
    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    if already_applied:
        return render(request, 'already_applied.html', {'job': job})

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'apply_form.html', {'form': form, 'job': job})

# Applicant's own applications
@login_required
def my_applications(request):
    if request.user.userrole.role != 'applicant':
        return redirect('dashboard')
    status_filter = request.GET.get('status')
    apps = Application.objects.filter(applicant=request.user)
    if status_filter in dict(Application.STATUS_CHOICES):
        apps = apps.filter(status=status_filter)
    return render(request, 'my_applications.html', {
        'applications': apps,
        'status_filter': status_filter,
    })

# Employer: view applicants for a specific job
@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job).order_by('-applied_at')
    return render(request, 'view_applicants.html', {
        'job': job,
        'applications': applications,
    })




def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    return render(request, 'job_list.html', {'jobs': jobs, 'query': query})



def home(request):
    if request.user.is_authenticated and hasattr(request.user, 'userrole'):
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def change_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id, job__posted_by=request.user)
    new_status = request.POST.get('status')
    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()
        messages.success(request, f"Application for {application.applicant.username} marked {new_status}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect('view_applicants', job_id=application.job.id)




