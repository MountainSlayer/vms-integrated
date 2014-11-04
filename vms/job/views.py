from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job
from job.forms import JobForm
from job.services import *
from event.services import *

@login_required
def create(request):
    event_list = get_events_ordered_by_name()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('job:list'))
        else:
            return render(request, 'job/create.html', {'form' : form, 'event_list' : event_list})
    else:
        form = JobForm()
        return render(request, 'job/create.html', {'form' : form, 'event_list' : event_list})

@login_required
def list(request):
    job_list = get_jobs_ordered_by_title()
    return render(request, 'job/list.html', {'job_list' : job_list})
