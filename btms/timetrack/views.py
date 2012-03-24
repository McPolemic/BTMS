from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date, timedelta
from models import Status,Task,MyTask
import settings
from timetrack import utils

def index(request):
    """Redirect to the weekly view with today's date"""
    today = date.today()
    (y,m,d) = [str(i) for i in (today.year, today.month, today.day)]
    return HttpResponseRedirect(reverse('timetrack.views.weekly', args=(y,m,d)))

def weekly(request, year, month, day):
    """Weekly time entry view"""
    (y, m, d) = (int(year), int(month), int(day))
    date_target = date(y,m,d)

    sunday = utils.find_start_date_from_date(date_target)

    day_of_week = [sunday,]

    #Fill out the rest of the days of the week
    for i in range(1,7):
        day_offset = timedelta(days=i)
        day_of_week.append(sunday + day_offset)

    task_list = Task.objects.select_related().filter(date__range=(sunday, day_of_week[-1]))
    #.filter(user = request.user.username)

    #Pull the statuses that are in task_list (unique)
    status_list = set([i.status for i in task_list])
    #filter(user = request.user.username)

    week = []    

    #FIXME
    for status in status_list:
        #Construct week-long object if status happened this week
        week_status = {}
        week_status['status'] = status
        
        #Initialize fractional hour display to all 0s
        week_status['values'] = [0.0 for i in range(7)]

        tasks_for_status = [t for t in task_list if t.status == status]

        if tasks_for_status == None:
            continue
        
        for t in tasks_for_status:
            #the array index is the weekday (0 for Sunday, 1 for Monday, etc.)
            index = (t.date.weekday() + 1) % 7
            week_status['values'][index] += t.frac_hours()

        week_status['total'] = sum(week_status['values'])        
        week.append(week_status)
    
    #Fill out the totals for the week
    totals = [0.0 for i in range(7)]

    for i in range(7):
        for week_status in week:
            totals[i] += week_status['values'][i]
    
    week.append({'status': Status(description='Total'),
                 'values': totals})
    
    tasks = Task.objects.filter(date = date_target)
    #Add to tasks end when we implement users
    #.filter(user = request.user.username)

    #Temp object to return total time.  Do not save.
    total = Task(total_minutes = sum([t.total_minutes for t in tasks]))
    remaining = 8 - total.frac_hours()

    #Create previous and next week links
    one_week = timedelta(7)

    prev_date = date_target - one_week
    next_date = date_target + one_week

    (py, pm, pd) = (str(prev_date.year), str(prev_date.month), str(prev_date.day))
    week_prev_link = reverse('timetrack.views.weekly', args=(py,pm,pd))
    (ny, nm, nd) = (str(next_date.year), str(next_date.month), str(next_date.day))
    week_next_link = reverse('timetrack.views.weekly', args=(ny,nm,nd))
    
    my_tasks = MyTask.objects.all()
    return render_to_response('timetrack/timesheet.html',
                              {'day_of_week': day_of_week,
                               'week':     week,
                               'week_prev': week_prev_link,
                               'week_next': week_next_link,
                               'my_tasks': my_tasks,
                               'day_curr': date_target,
                               'total':    total,
                               'debug':    settings.DEBUG},
                              context_instance=RequestContext(request))
