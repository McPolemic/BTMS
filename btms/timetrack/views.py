from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Status,Task,MyTask

def index(request):
    tasks = Task.objects.all()
    my_tasks = MyTask.objects.all()
    return render_to_response('timetrack/timesheet.html',
                              {'tasks': tasks,
                               'my_tasks': my_tasks},
                              context_instance=RequestContext(request))
    
