from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','quantity','product_price', 'order')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','city','order_total','tax','status','is_ordered','created_at']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','phone','email']
    inlines = OrderProductInline

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)