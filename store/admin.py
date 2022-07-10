from django.contrib import admin
<<<<<<< .mine
from .models import Product, Variation
=======
from .models import Product,Variation
>>>>>>> .theirs

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available' )
    prepopulated_fields = {'slug':('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display    =('product','variation_category','variation_value','is_active')
    list_editable   =('is_active',)
    list_filter     = ('product','variation_category','variation_value')
admin.site.register(Product,ProductAdmin)
<<<<<<< .mine
admin.site.register(Variation)
=======
admin.site.register(Variation,VariationAdmin)
>>>>>>> .theirs

