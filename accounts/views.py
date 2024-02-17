import django.contrib.auth.decorators
from django.shortcuts import render, redirect
import django.contrib.auth.forms
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


# Create your views here.
def signupaccount(request):
  form = UserCreateForm()
  if request.method == 'GET':
    return render(request, 'accounts/signupaccount.html', {'form':form})

  else:
    if request.POST['password1']==request.POST['password2']:
      try:
        user = User.objects.create_user(
          request.POST['username'],
          password = request.POST['password1']
        )
        user.save()
        login(request, user)
        return redirect('home')
      except IntegrityError:
        return render(request, 'accounts/signupaccount.html', {
          'form':form,
          'error':'Ce nom d\'utilisateur existe deja, veuillez choisir un autre nom'
        })

    else:
      return render(request, 'accounts/signupaccount.html', {'form':form,
      'error':'Les mots de passe ne correspondent pas'})


@login_required
def logoutaccount(request):
  logout(request)
  return redirect('loginaccount')

def loginaccount(request):
  form = AuthenticationForm()

  if request.method == 'GET':
    return render(request, 'accounts/loginaccount.html', {'form':form})
  else:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
      return render(request, 'accounts/loginaccount.html' ,{'form':form, 'error':'Nom d\'utilisateur ou le mot de passe est invalide !'})
    else:
      login(request, user)
      return redirect('home')

   