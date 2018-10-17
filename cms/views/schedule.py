from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from cms.models import Schedule
from ..forms import ScheduleForm
from django.http import JsonResponse


# Create your views here.
# schedule views
def schedule_index(request, company_id='ac'):
    sort = request.GET.get('sort', 'start_time')
    request.session['company'] = company_id
    schedules = get_list_or_404(Schedule.objects.order_by(sort), company=company_id)

    return render(request, 'cms/schedule/index.html', {'schedules': schedules, 'company': company_id})


def schedule_new(request):
    # if this is a post method then we need to create the new schedule
    if request.method == 'POST':
        form = ScheduleForm(request.session, request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('cms:schedule_index', form.data.get('company'))

    # otherwise show a blank for for entry of a new schedule
    form = ScheduleForm(request.session)
    return render(request, 'cms/schedule/new.html', {'form': form, 'company': request.session['company']})


def schedule_edit(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)

    # if this is a post method then we need to save the updated form data
    if request.method == 'POST':
        form = ScheduleForm(request.session, request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('cms:schedule_index', form.data.get('company'))

    # otherwise return a form instance for the specified schedule
    # form = get_schedule_form(schedule)
    form = ScheduleForm(request.session, instance=schedule)
    return render(request, 'cms/schedule/edit.html',
                  {
                      'schedule': schedule,
                      'form': form,
                      'company': schedule.company_id
                  })


def schedule_delete(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        return redirect('cms:schedule_index', schedule.company_id)

    return render(request, 'cms/schedule/delete.html', {'schedule': schedule})


# schedule json
def schedule_json(request):
    schedules = Schedule.objects.all().values()
    schedules_list = list(schedules)  # important: convert the QuerySet to a list object
    return JsonResponse(schedules_list, safe=False)
