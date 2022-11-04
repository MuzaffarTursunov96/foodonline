from vendor.models import Vendor


def vendor_get(request):
  try:
    vendor = Vendor.objects.get(user=request.user)
  except:
    vendor=None
  context = {
      'vendor': vendor
  }
  return context
