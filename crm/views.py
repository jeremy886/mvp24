from django.shortcuts import render
from .models import Record

def home(request):
    records = {"developer": "Jeremy Chen"}
    return render(request, 'crm/home.html', {'records': records})


def record_list(request):
    records = Record.objects.all()
    return render(request, 'crm/record_list.html', {"records": records})