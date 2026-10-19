from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Safer way to import search queries
from .models import ProjectSubmission

# ==========================================
# 1. AUTHENTICATION GATES (LOGIN / LOGOUT)
# ==========================================
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('supervisor_dashboard')
                return redirect('student_dashboard')
            else:
                error_message = "Invalid username or password configuration."
        else:
            error_message = "Invalid submission details. Please try again."
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================================
# 2. STUDENT REPOSITORY WORKSPACE
# ==========================================
@login_required(login_url='login')
def student_dashboard(request):
    my_projects = ProjectSubmission.objects.filter(submitted_by=request.user).order_by('-submission_date')
    return render(request, 'student_dashboard.html', {'projects': my_projects})

@login_required(login_url='login')
def submit_project(request):
    if request.method == 'POST':
        form_title = request.POST.get('title')
        form_category = request.POST.get('category')
        form_abstract = request.POST.get('abstract')
        
        ProjectSubmission.objects.create(
            title=form_title,
            category=form_category,
            abstract=form_abstract,
            status='PENDING',
            submitted_by=request.user
        )
        return redirect('student_dashboard')
        
    return render(request, 'submit_project.html')


# ==========================================
# 3. SUPERVISOR ADMINISTRATIVE PORTAL
# ==========================================
@login_required(login_url='login')
def supervisor_dashboard(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    pending_projects = ProjectSubmission.objects.filter(status='PENDING').order_by('submission_date')
    return render(request, 'supervisor_dashboard.html', {'projects': pending_projects})

@login_required(login_url='login')
def review_project(request, project_id):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        project = ProjectSubmission.objects.get(id=project_id)
        project.status = request.POST.get('status')
        project.supervisor_feedback = request.POST.get('feedback')
        project.save()
        return redirect('supervisor_dashboard')


# ==========================================
# 4. PUBLIC DISCOVERY INDEX (THE BLANK PATH HOME PAGE)
# ==========================================
def public_archive(request):
    approved_projects = ProjectSubmission.objects.filter(status='APPROVED').order_by('-submission_date')
    
    search_query = request.GET.get('q')
    if search_query:
        approved_projects = approved_projects.filter(
            Q(title__icontains=search_query) | Q(abstract__icontains=search_query)
        )
        
    return render(request, 'public_archive.html', {'projects': approved_projects, 'query': search_query})
