from django.shortcuts import render, get_object_or_404, redirect
from .models import Record
from .forms import RecordForm


def home(request):
    records = {"developer": "Jeremy Chen"}
    return render(request, 'crm/home.html', {'records': records})


def record_list(request):
    records = Record.objects.all()
    return render(request, 'crm/record_list.html', {"records": records})


def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'crm/record_detail.html', {'record': record})


def record_create(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')  # Redirect to the list view after successful creation
    else:
        form = RecordForm()
    return render(request, 'crm/record_form.html', {'form': form})
