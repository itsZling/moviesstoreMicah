from django.contrib import admin
from .models import Order, Item

# Register your models here.
admin.site.register(Order)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'quantity', 'order', 'amountPurchased')
    list_filter = ['quantity', 'amountPurchased']
    ordering = ['-amountPurchased']