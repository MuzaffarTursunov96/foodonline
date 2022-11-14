from vendor.models import Vendor
from django.conf import settings
from .models import UserProfile


def vendor_get(request):
  try:
    vendor = Vendor.objects.get(user=request.user)
  except:
    vendor=None
  context = {
      'vendor': vendor
  }
  return context

def get_user_profile(request):
  try:
    user_profile = UserProfile.objects.get(user=request.user)
  except:
    user_profile=None
  context = {
      'user_profile': user_profile
  }
  return context


def get_google_api(request):
  return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}