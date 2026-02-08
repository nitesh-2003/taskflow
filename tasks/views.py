from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task
from projects.models import Project
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.models import Notification

@login_required
def kanban_board(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    todo = project.tasks.filter(status='TODO')
    in_progress = project.tasks.filter(status='IN_PROGRESS')
    done = project.tasks.filter(status='DONE')
    users = User.objects.all()
    
    context = {
        'is_manager': hasattr(request.user, 'profile') and request.user.profile.role in ['MANAGER', 'ADMIN'],
        'project': project,
        'todo': todo,
        'in_progress': in_progress,
        'done': done,
        'users': users
    }
    return render(request, 'tasks/kanban.html', context)

def is_manager(user):
    return hasattr(user, 'profile') and user.profile.role in ['MANAGER', 'ADMIN']

@login_required
@user_passes_test(is_manager, login_url='home')
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        assigned_to_id = request.POST.get('assigned_to')
        assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
        
        task = Task.objects.create(
            title=title,
            project=project,
            assigned_to=assigned_to
        )
        
        # Trigger Notification
        if assigned_to:
            msg = f"New task assigned: {title}"
            Notification.objects.create(user=assigned_to, message=msg)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{assigned_to.id}",
                {"type": "send_notification", "message": msg}
            )
            
        return redirect('kanban', project_id=project_id)

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('status')
    if new_status in dict(Task.STATUS_CHOICES):
        task.status = new_status
        task.save()
    return redirect('kanban', project_id=task.project.id)
