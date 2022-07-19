from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct

from store.models import Product
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

# Lưu chi tiết dao dịch
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()

#Chuyển tất cả số lượng hàng trong giỏ hàng vào table Order Product
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_items = CartItem.objects.get(id=item.id)
        product_variation = cart_items.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.get(product_variation)
        orderproduct.save()
        

# Giảm số lượng sản phẩm đã bán
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

# Xóa giỏ hàng
    CartItem.objects.filter(user=request.user).delete()


# Gửi đơn hàng vào mail của khách
    mail_subject = 'Cảm ơn bạn đã đặt hàng của chúng tôi'
    message = render_to_string('account/order_received_email.html', {
        'user': request.user,
        'order': order,
    })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

# Gửi số đơn hàng và giao dịch id
    data = {
        'orders_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

   # return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (0.1 * total)
    grand_total = total + tax


    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleanned_data['first_name']
            data.last_name = form.cleanned_data['last_name']
            data.phone = form.cleanned_data['phone']
            data.email = form.cleanned_data['email']
            data.address_line_1 = form.cleanned_data['address_line_1']
            data.address_line_2 = form.cleanned_data['address_line_2']
            data.country = form.cleanned_data['country']
            data.state = form.cleanned_data['state']
            data.city = form.cleanned_data['city']
            data.order_note = form.cleanned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Tạo mã đơn hàng
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d') #20220706
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    trsnsID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {

            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'payment':payment,
            'subtotal': subtotal,
        }

        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')