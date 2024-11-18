from django.shortcuts import redirect, render
from .models import *

def pageNotFound(request, exception):
    path = request.get_full_path()
    if not path.endswith('/'):
        return redirect(f'{path}/')

    return redirect('index')

def forbidden(request, *args, **argv):
    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')
    
    return render(request, '403.html', {
        'settings': settings,
    })

def serverError(request, *args, **argv):
    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')
    
    return render(request, '500.html', {
        'settings': settings,
    })