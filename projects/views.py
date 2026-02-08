from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project
from django.contrib.auth.models import User

def is_manager(user):
    return hasattr(user, 'profile') and user.profile.role in ['MANAGER', 'ADMIN']

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
@user_passes_test(is_manager, login_url='home')
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Project.objects.create(
            name=name,
            description=description,
            manager=request.user
        )
        return redirect('project_list')
    return render(request, 'projects/create_project.html')
