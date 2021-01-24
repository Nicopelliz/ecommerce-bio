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
    return render(request, 'registration/register.html', context)

def edit_profile(request):
    return render(request, 'registration/edit_profile.html')

# social_views

def login(request):
  return render(request, 'login.html')


def contatti(request):
    return render(request, 'contatti.html')

def home(request):
    return render(request, 'home.html')
    #return redirect('mercato')
