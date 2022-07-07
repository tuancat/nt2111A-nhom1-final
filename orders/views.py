from django.shortcuts import render
from django.http import HttpResponse
from carts.models import CartItem

# Create your views here.

def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_item = CartItem.object.filter(user=account_user)
    cart_count = cart_item.count()
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
            data.first_name = form.cleanned_data('first_name')
            data.last_name = form.cleanned_data('last_name')
            data.phone = form.cleanned_data('phone')
            data.mail = form.cleanned_data('mail')
            data.address_line_1 = form.cleanned_data('address_line_1')
            data.address_line_2 = form.cleanned_data('address_line_2')
            data.country = form.cleanned_data('country')
            data.state = form.cleanned_data('state')
            data.city = form.cleanned_data('city')
            data.order_note = form.cleanned_data('order_note')
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
            return redirect ('checkout')
    else:
        return redirect('checkout')