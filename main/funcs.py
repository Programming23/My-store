from .models import *
import re
import random

def generate():
    return str(random.randint(100000000000, 999999999999))

def getCartQuantity(request):
    if 'cart' not in  request.session:
        return 0
    
    quantity = 0
    for key in request.session['cart']:
        try:
            product = Product.objects.get(id=int(key))
            if product.state == False:
                request.session['cart'].pop(key)
            else:
                if product.max_quantity < request.session['cart'][key]:
                    request.session['cart'][key] = product.max_quantity
                quantity += request.session['cart'][key]
        except:
            pass

    return quantity


ptn_name = '^[A-Za-zأ-ي؀-ۿ\\s]+$'
ptn_phone = '^[0-9]+$'
ptn_address = '^[A-Z0-9a-zأ-ي؀-ۿ\\s]+$'

def subscribe(request):
    name= None
    phone  = None
    error = None
    success = None


    if  'subscribe' in request.POST and 'name' in request.POST and 'phone' in request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        
        if not(phone and name):
            error = 'المرجو ملء الحقل الفارغ' 
        elif len(name.replace(' ', '')) < 3 or len(name) > 40:
            error = 'يجب على الاسم ان يكون أكثر من حرفين وأقل من 40 حرفا'
        elif not re.match(ptn_name, name):
            error = 'يجب أن يحتوي حقل الاسم على أحرف فقط ولا يجب أن يحتوي على أي رموز خاصة'
        elif not re.match(ptn_phone, phone):
            error = 'يجب أن يحتوي حقل الهاتف على أرقام فقط ولا يجب أن يحتوي على أي أحرف أو رموز آخرى.'
        elif len(phone) < 10 or len(phone) > 12:
            error = 'يجب على حقل الهاتف ان يكون مابين 10 أرقام و 12 رقما'
        else:
            try:
                if not Subscription.objects.filter(phone=phone).exists():
                    sub = Subscription(name=name, phone=phone)
                    sub.save()
                    success = 'تم الاشتراك بنجاح '
                else:
                    error = 'لقد تم الاشتراك مسبقا بهذا الرقم'
            except:
                error = 'حدث خطأ'
        

    return error, success