from django.shortcuts import render

def home(request):
    records = {"developer": "Jeremy Chen"}
    return render(request, 'crm/home.html', {'records': records})