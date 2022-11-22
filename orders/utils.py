import datetime
import simplejson as json
import ast

def generte_order_number(pk):
  current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M")
  order_number = current_datetime + str(pk)
  return order_number


def order_total_by_vendor(order,vendor_id):
  total_data = json.loads(order.total_data)
  data = total_data.get(str(vendor_id))
  subtotal = 0
  tax = 0
  tax_dict = {}
  for key, val in data.items():
    # print(key,val,type(val))
    subtotal +=float(key)
    val = ast.literal_eval(val)
    tax_dict.update(val)

    for i in val:
        for j in val[i]: 
            tax += float(val[i][j])
        
  grand_total =subtotal + tax

  context ={
  'subtotal':subtotal,
  'tax_dict':tax_dict,
  'grand_total':grand_total
  }


  return context
  pass
