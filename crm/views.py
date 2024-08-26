from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Record, Event
from .forms import RecordForm


def home(request):
    records = {"developer": "Jeremy Chen"}
    return render(request, 'crm/home.html', {'records': records})


@login_required
def record_list(request):
    records = Record.objects.all()
    return render(request, 'crm/record_list.html', {"records": records})


@login_required
def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'crm/record_detail.html', {'record': record})


@login_required
def record_create(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')  # Redirect to the list view after successful creation
    else:
        form = RecordForm()
    return render(request, 'crm/record_form.html', {'form': form})


@login_required
def record_update(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == "POST":
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = RecordForm(instance=record)
    return render(request, 'crm/record_form.html', {'form': form})


@login_required
def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == "POST":
        record.delete()
        return redirect('record_list')
    return render(request, 'crm/record_confirm_delete.html', {'record': record})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'crm/event_list.html', {"events": events})
