from .funcs import generate, getCartQuantity, ptn_address,ptn_name, ptn_phone, subscribe
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
import re
from django.http import Http404
from django.shortcuts import get_object_or_404


def removeItemCart(request, item):
    cart = request.session.get('cart', {})
    try:
        cart.pop(str(item))
    except Exception as e:
        pass
    
    request.session['cart'] = cart

    return HttpResponse('Everything is okay', status=200)


def checkout(request):
    settings = None
    cartQuantity = getCartQuantity(request)
    cart = request.session.get('cart', {})
    order_error = None
    items = []
    total = 0
    info = request.session.get('info', None)
    ship_price = '-'
    ships = Shipping.objects.filter(state=True)
    all_total = '-'
    constants = None

    if cartQuantity == 0:
        return redirect('index')

    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')

    try:
        constants = Constants.objects.all()[0]
    except:
        return redirect('admin:login')
    
    if request.method == 'POST':
        if 'save_order' in  request.POST and 'name' in request.POST and 'phone' in request.POST and 'city' in request.POST and 'address' in request.POST:
            name = request.POST['name']
            phone = request.POST['phone']
            city = request.POST['city']
            address = request.POST['address']

            if not(name and address and city and phone):
                order_error = 'المرجو ملء الحقل الفارغ'
            elif not re.match(ptn_name, name):
                order_error = 'يجب أن يحتوي حقل الاسم على أحرف فقط ولا يجب أن يحتوي على أي رموز خاصة'
            elif len(name.replace(' ', '')) < 3 or len(name) > 40:
                order_error = 'يجب على حقل الاسم ان يكون أكثر من حرفين وألا يتجاوز 40 حرفا'
            elif not re.match(ptn_phone, phone):
                order_error = 'يجب أن يحتوي حقل الهاتف على أرقام فقط ولا يجب أن يحتوي على أي أحرف أو رموز آخرى.'
            elif len(phone) < 10 or len(phone) > 12:
                order_error = 'يجب على حقل الهاتف ان يكون أكثر من 10 أرقام وألا يتجاوز 12 رقما'
            elif not Shipping.objects.filter(city=city, state=True).exists():
                order_error = 'المرجو اختيار المدينة من الخيارات الموجودة'
            elif not re.match(ptn_address, address):
                order_error = 'لا يجب أن  يحتوي حقل العنوان على أي رموز خاصة'
            elif len(address.replace(' ', '')) < 5 or len(address) > 255 :
                order_error = 'يجب على حقل الاسم ان يكون أكثر من 5 أحرف وألا يتجاوز 255 حرفا'
            elif len(cart) > 0:
                ship = Shipping.objects.get(city=city, state=True)
                order = Order(number=generate(), customer=name, phone_number=phone, address=address, city=ship, )
                order.save()
                total = int(ship.price)
                for key in cart:
                    
                    try:
                        product = Product.objects.get(id=int(key),  state=True)
                        item = CartProduct(product=product, order=order, quantity=cart[key])
                        item.save()
                        items.append(item)
                        total += item.getTotal
                    except:
                        pass
                info = {
                    'name': name,
                    'phone': phone,
                    'city': city,
                    'address': address,
                }
                request.session['info'] = info
                request.session['cart'] = {}
                if settings.end_order == True:
                    return redirect(f"/order/{order.number}")
                else:
                    details = constants.command_details.split('\n')
                    for d in details:
                        if len(d.replace(' ', '')) == 0:
                            details.remove(d)
                    return render(request, 'order_success.html', {
                        'settings': settings,
                        'details': details,
                        'constants': constants,
                        'cartQuantity': cartQuantity,
                        'order': order,
                        'total': total,
                        'ship': ship.price,
                        'products': items,
                        'title': constants.command_title,
                    })
            else:
                redirect('index')
        elif 'save_order' in request.POST:
            order_error = 'المرجو ملء الحقل الفارغ'

    for key in cart:
        try:
            item = Product.objects.get(id=int(key), state=True)
            item.quantity = cart[key]
            total += int(item.quantity) * int(item.price)
            items.append(item)
        except:
            pass

    if info != None and 'city' in info:
        try:
            ship_price = Shipping.objects.get(city=info['city'], state=True).price
            all_total = int(ship_price) + total
        except Exception as e:
            pass

    return render(request, 'checkout.html', {
        'cartQuantity': cartQuantity,
        'products': items,
        'settings': settings,
        'constants': constants,
        'ships': ships,
        'ship': ship_price,
        'all_total': all_total,
        'order_error': order_error,
        'total': total,
        'info': info,
        'title': constants.checkout_title,
    })

def cartPage(request):
    settings = None
    cart = request.session.get('cart', {})
    items = []
    total = 0
    error = None
    success  = None
    all_total = '-'
    ship = '-'
    cartQuantity = getCartQuantity(request)
    info = request.session.get('info', None)
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
        error, success = subscribe(request)

        if 'save_changes' in request.POST:
            for key in request.POST:
                if key.startswith('quantity-'):
                    try:
                        product = Product.objects.get(id=int(key[9:]), state=True)
                        quantity = int(request.POST[key])
                        if quantity >= 1 and quantity <= product.max_quantity:
                            cart[str(product.id)] = quantity
                            
                    except:
                        break
            request.session['cart'] = cart
            cartQuantity = getCartQuantity(request)
            

    for key in cart:
        try:
            item = Product.objects.get(id=int(key), state=True)
            item.quantity = cart[key]
            total += int(item.quantity) * int(item.price)
            items.append(item)
        except:
            pass

    if info != None and 'city' in info:
        try:
            ship = Shipping.objects.get(city=info['city']).price
            all_total = int(ship) + total
        except Exception as e:
            pass

    return render(request, 'cart_page.html', {
        'cartQuantity': cartQuantity,
        'products': items, 
        'total': total,
        'settings': settings,
        'constants': constants,
        'sub_error': error,
        'sub_success': success,
        'all_total': all_total,
        'ship': ship,
        'title': 'عربة التسوق',
    })
    
 
def end_order(request, order_num):
    constants =  None
    settings = None
    try:
        settings = SettingSite.objects.all()[0]
    except:
        return redirect('admin:login')

    try:
        constants = Constants.objects.all()[0]
    except:
        return redirect('admin:login')
    
    if settings.end_order == False:
        raise Http404()
    
    order = get_object_or_404(Order, number=order_num)
    cartQuantity = getCartQuantity(request)
    products= order.products.all()
    details = constants.command_details.split('\n')
    for d in details:
        if len(d.replace(' ', '')) == 0:
            details.remove(d)
    
    return render(request, 'order_success.html', {
        'settings': settings,
        'constants': constants,
        'cartQuantity': cartQuantity,
        'details': details,
        'order': order,
        'total': order.getTotal,
        'ship': order.city.price,
        'products': products,
        'title': constants.command_title,
    })