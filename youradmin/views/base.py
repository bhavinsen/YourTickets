from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import (
    render
)

@staff_member_required(login_url='/youradmin/login/')
def index(request):
    return render(request, 'youradmin/base.html', {})
