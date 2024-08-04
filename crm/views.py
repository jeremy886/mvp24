from django.shortcuts import render, get_object_or_404
from .models import Record


def home(request):
    records = {"developer": "Jeremy Chen"}
    return render(request, 'crm/home.html', {'records': records})


def record_list(request):
    records = Record.objects.all()
    return render(request, 'crm/record_list.html', {"records": records})


def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'crm/record_detail.html', {'record': record})

