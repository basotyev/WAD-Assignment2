from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task, User
from django.views.decorators.csrf import csrf_exempt

def task_list(request):
    tasks = Task.objects.all()
    response = "<h1>Task List</h1><ul>"
    for task in tasks:
        response += f"<li>{task.title} - {task.description} (Completed: {task.completed})</li>"
    response += "</ul>"
    return HttpResponse(response)

def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        response = f"<h1>{task.title}</h1>"
        response += f"<p>Description: {task.description}</p>"
        response += f"<p>Completed: {task.completed}</p>"
        response += f"<p>Assignee: {task.assignee.username}</p>"
        response += f"<p>Tags: {', '.join(tag.name for tag in task.tags.all())}</p>"
    except Task.DoesNotExist:
        response = "Task not found."
    return HttpResponse(response)

@csrf_exempt
def task_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'on'
        assignee_id = request.POST.get('assignee')
        assignee = User.objects.get(id=assignee_id)

        task = Task.objects.create(title=title, description=description, completed=completed, assignee=assignee)
        return redirect('/tasks/')  # Redirect to task list after creation

    form = '''
        <h1>Create Task</h1>
        <form method="POST">
            Title: <input type="text" name="title"><br>
            Description: <input type="text" name="description"><br>
            Completed: <input type="checkbox" name="completed"><br>
            Assignee (User ID): <input type="number" name="assignee"><br>
            <button type="submit">Create Task</button>
        </form>
    '''
    return HttpResponse(form)