from operator import imod
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from django.contrib import messages


from .forms import UserForm

# Create your views here.

def registerUser(request):
  if request.method =='POST':
    form =UserForm(request.POST)
    if form.is_valid():
      password =form.cleaned_data['password']
      user = form.save(commit=False)
      user.set_password(password)
      user.role = User.CUSTOMER
      user.save()
      messages.success(request,'Your account registered successfully!')
      return redirect('registerUser')
    else:
      print(form.errors)
  else:
    form =UserForm()
  return render(request,'accounts/registerUser.html',{'form':form})
