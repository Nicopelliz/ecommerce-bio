from django.shortcuts import render, redirect
from . forms import CreateUserForm


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def contatti(request):
    return render(request, 'contatti.html')


def home(request):
    return render(request, 'home.html')
