from django.shortcuts import render


def index(request):

    return render(request, 'company_dashboard/index.html',{})