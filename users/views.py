from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    '''Registrates new user'''
    if request.method != 'POST':
        # Creates blank registration form
        form = UserCreationForm()
    else:
        # Processes filled form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Sign in and redirect on home page 
            login(request, new_user)
            return redirect('learning_logs:index')
    
    # Create blanck and unvalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)


