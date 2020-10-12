from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    '''
    Item model representation on admin site.
    '''
    list_display = ('name','category','price')
    list_editable = ('price')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    '''
    Item model representation on admin site.
    '''
    list_display = ('id','email','first_name','last_name','phone','price')
    search_fields = ('email','first_name','last_name')
    actions = ('close_order', 'process_order', 'cancel_order')

    def close_order(self, request, queryset):
        '''
        Action to set order status to DONE
        '''
        queryset.update(status=models.Order.Status.DONE)

    def process_order(self, request, queryset):
        '''
        Action to set order status to PROCESSING 
        '''
        queryset.update(status=models.Order.Status.PROCESSING)

    def cancel_order(self, request, queryset):
        '''
        Action to set order status to CANCELED 
        '''
        queryset.update(status=models.Order.Status.CANCELED)

