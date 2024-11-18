from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
import re
from .funcs import getCartQuantity, ptn_name, ptn_phone, subscribe


def index(request):
    products = Product.objects.filter(state=True)
    types = ProductType.objects.all()
    genres = []
    settings  = None
    constants = None
    cartQuantity = getCartQuantity(request)
    
    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')

    try:
        constants = Constants.objects.all()[0]
    except:
        return redirect('admin:login')

    error = None
    success = None

    if request.method == 'POST':
        error, success = subscribe(request)

    for t in types:
        if len(Product.objects.filter(product_type=t, state=True)) > 0:
            genres.append(t)

    return render(request, 'main.html', {
        'products': products,
        'types': genres,
        'sub_error': error,
        'sub_success': success,
        'settings': settings,
        'constants': constants,
        'title': settings.site_title,
        'cartQuantity': cartQuantity,
        'bigproducts': BigProduct.objects.filter(product__state=True),
        'lists': ListProducts.objects.all(),
        'features': Features.objects.all(),
    })



def productPage(request, name):
    product = get_object_or_404(Product, name=name.replace('-', ' '))
    cartQuantity = getCartQuantity(request)
    cart = request.session.get('cart', {}) 

    if str(product.id) in cart:
        product.quantity = cart[str(product.id)]
    else:
        product.quantity = 1

    settings = None
    error = None
    success = None
    er = None
    constants = None

    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')

    try:
        constants = Constants.objects.all()[0]
    except:
        return redirect('admin:login')

    if request.method == 'POST':
        error, success = subscribe(request)
        if 'add_to_cart' in request.POST and 'quantity' in request.POST :
            try:
                quantity = int(request.POST['quantity'])
                if quantity >= 1 and quantity <= product.max_quantity:
                    cart[str(product.id)] = quantity
                    request.session['cart'] = cart
                    product.quantity = quantity
                    cartQuantity = getCartQuantity(request)
                else:
                    er = f'المرجو اختيار الكمية الصحيحة التي تريدها و عدم تجاوز أقصى قيمة وهي {product.max_quantity}'

            except Exception as  e:
                er = 'حدث خطأ . المرجو المحاولة مرة أخرى'
       

    return render(request, 'product_page.html', {
        'product': product,
        'sub_error': error,
        'sub_success': success,
        'error': er,
        'settings': settings,
        'cartQuantity': cartQuantity,
        'title': product.name,
        'constants': constants,
    })


def contact_us(request):
    name = None
    phone = None
    subject = None
    message = None
    cartQuantity = getCartQuantity(request)
    error_message = None
    success_message = None
    e = None
    s = None
    settings = None
    constants =  None

    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')

    try:
        constants = Constants.objects.all()[0]
    except:
        return redirect('admin:login')

    if request.method == 'POST':
        e,s = subscribe(request)
        

        if 'save_message' in request.POST and 'name' in request.POST and 'phone' in request.POST and 'subject' in request.POST and 'message' in request.POST :
            name = request.POST['name']
            phone = request.POST['phone']
            subject = request.POST['subject']
            message = request.POST['message']
            print('here is one')
            if not(name != '' and phone != '' and subject != '' and message  != ''):
                error_message = 'المرجو ملء الحقل الفارغ'

            elif len(name.replace(' ', '')) < 3 or len(name) > 40:
                error_message = 'يجب على الاسم ان يكون أكثر من حرفين وأقل من 40 حرفا'

            elif not re.match(ptn_name, name):
                error_message = 'يجب أن يحتوي حقل الاسم على أحرف فقط ولا يجب أن يحتوي على أي رموز خاصة'
            
            elif not re.match(ptn_phone, phone):
                error_message = 'يجب أن يحتوي حقل الهاتف على أرقام فقط ولا يجب أن يحتوي على أي أحرف أو رموز آخرى.'
            
            elif len(phone) < 10 or len(phone) > 12:
                error_message = 'يجب على حقل الهاتف ان يكون مابين 10 أرقام و 12 رقما'
            
            elif len(subject) > 200:
                error_message = 'يجب على الموضوع ان يكون أقل من 200 حرف'

            elif len(message) > 2000:
                error_message = 'يجب على الرسالة ان تكون أقل من 2000 حرف'
            else:
                try:
                    print('here')
                    mes = Message(name=name, phone=phone, subject=subject, message=message)
                    mes.save()
                    success_message = 'تم استلام رسالتك بنجاح. سنعمل على معالجتها والرد عليك في أقرب وقت.'
                except:
                    error_message = 'حدث خطأ'

    return render(request, 'contact_page.html', {
        'success': success_message,
        'error': error_message,
        'sub_error': e,
        'sub_success': s,
        'cartQuantity': cartQuantity,
        'settings': settings,
        'constants': constants,
        'title': constants.contact_title,
    })