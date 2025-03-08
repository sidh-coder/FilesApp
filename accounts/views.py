from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup.
            login(request, user)
            return redirect('file_list')# Change 'home' to your desired redirect URL.
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

