import datetime

def generte_order_number(pk):
  current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M")
  order_number = current_datetime + str(pk)
  return order_number