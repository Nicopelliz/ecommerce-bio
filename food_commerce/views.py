from django.shortcuts import render, redirect
from . forms import CreateUserForm, UpdateUserForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required(login_url="/login")
def edit_profile(request):
    form = UpdateUserForm()
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))

    context = {'form': form}
    return render(request, 'registration/edit_profile.html', context)

# social_views

def login(request):
  return redirect(request.META.get('HTTP_REFERER'))


def contatti(request):
    return render(request, 'contatti.html')

def home(request):
    return render(request, 'home.html')
    #return redirect('mercato')
