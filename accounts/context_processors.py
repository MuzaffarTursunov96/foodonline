from vendor.models import Vendor
from django.conf import settings


def vendor_get(request):
  try:
    vendor = Vendor.objects.get(user=request.user)
  except:
    vendor=None
  context = {
      'vendor': vendor
  }
  return context


def get_google_api(request):
  return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}