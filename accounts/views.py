from django.shortcuts import render,redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from django.contrib import messages,auth
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from .forms import UserForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from orders.models import Order

# Create your views here.

def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied

def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied


def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request,'You are alredy logged in!')
    return redirect('myAccount')
  elif request.method =='POST':
    form =UserForm(request.POST)
    if form.is_valid():
      password =form.cleaned_data['password']
      user = form.save(commit=False)
      user.set_password(password)
      user.role = User.CUSTOMER
      user.save()

      #Send the verification email
      email_template='accounts/emails/account_verification_email.html'
      mail_subject ='Please activate your account'
      send_verification_email(request,user,mail_subject,email_template)
      messages.success(request,'Your account registered successfully!')
      return redirect('registerUser')
    else:
      print(form.errors)
  else:
    form =UserForm()
  return render(request,'accounts/registerUser.html',{'form':form})


def registerVendor(request):
  if request.user.is_authenticated:
    messages.warning(request,'You are alredy logged in!')
    return redirect('vendorDashboard')
  elif request.method =='POST':
    form =UserForm(request.POST)
    v_form=VendorForm(request.POST,request.FILES)
    if form.is_valid() and v_form.is_valid():
      first_name =form.cleaned_data['first_name']
      last_name =form.cleaned_data['last_name']
      username =form.cleaned_data['username']
      email =form.cleaned_data['email']
      password =form.cleaned_data['password']
      user =User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role =User.VENDOR
      user.save()
      vendor =v_form.save(commit=False)
      vendor.user = user
      vendor_name=v_form.cleaned_data['vendor_name']
      vendor.vendor_slug=slugify(vendor_name)+'-'+str(user.id)
      user_profile =UserProfile.objects.get(user=user)
      vendor.user_profile =user_profile
      vendor.save()
      email_template='accounts/emails/account_verification_email.html'
      mail_subject ='Please activate your account'
      send_verification_email(request,user,mail_subject,email_template)

      messages.success(request,'Your account registered successfully! Please wait for the approval.')
      return redirect('registerVendor')
    else:
      print('Invalid Error')
  else:
    form =UserForm()
    v_form=VendorForm()
  context ={
    'form':form,
    'v_form':v_form
  }
  return render(request,'accounts/registerVendor.html',context)

def login(request):
  if request.user.is_authenticated:
    messages.warning(request,'You are alredy logged in!')
    return redirect('myAccount')
  elif request.method =='POST':
    email =request.POST.get('email',None)
    password =request.POST.get('password',None)
    # print(email,password)
    user = auth.authenticate(email=email,password=password)
    if user is not None:
      auth.login(request,user)
      messages.success(request,'You are now loged in.')
      return redirect('myAccount')
    else:
      messages.error(request,'Invalid login credentials.')
      return redirect('login')
  return render(request,'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request,'you are logged out.')
  return redirect('login')



@login_required(login_url='login')
def myAccount(request):
  user =request.user
  redirectUrl =detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  return render(request,'accounts/vendorDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
  orders = Order.objects.filter(user=request.user,is_ordered=True)
  recent_orders=orders[:5]
  context ={
    'orders':orders,
    'orders_count':orders.count(),
    'recent_orders':recent_orders
  }
  return render(request,'accounts/customerDashboard.html',context)

def activate(request,uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user,token):
    user.is_active = True
    user.save()
    messages.success(request,'Congratulations ! your account is activated.')
    return redirect('myAccount')
  else:
    messages.error(request,'Invalid activation link.')
    return redirect('myAccount')

def forgot_password(request):
  if request.method == 'POST':
    email = request.POST.get('email',None)
    if email:
      if User.objects.filter(email=email).exists():
        user = User.objects.get(email__exact=email)
        #send the reset password email
        mail_subject='Reset your password'
        email_template='accounts/emails/reset_password_email.html'
        send_verification_email(request, user, mail_subject, email_template)

        messages.success(request,'Passoword reset link has been sent to your email addres.')
        return redirect('login')
      else:
        messages.error(request,'Account does not exist.')
        return redirect('forgot_password')
    else:
      messages.error(request,'Email incorrect')
      return redirect('forgot_password')
  return render(request,'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user,token):
    request.session['uid']=uid
    messages.info(request,'Please reset your password')
    return redirect('reset_password')
  else:
    messages.error(request,'This link has been expired')
    return redirect('myAccount')



def reset_password(request):
  if request.method == "POST":
    password = request.POST.get('password',None)
    confirm_password = request.POST.get('confirm_password',None)

    if password == confirm_password and password is not None:
      pk = request.session.get('uid')
      user =User.objects.get(pk=pk)
      user.set_password(password)
      user.is_active =True
      user.save()
      messages.success(request,'Password reset successfully!')
      return redirect('login')
      
    else:
      messages.error(request,"Password don't match")
      return redirect('reset_password')

  return render(request,'accounts/reset_password.html')