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
    list_display = ('name','category','price','image_preview')
    list_editable = ('price',)
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.StackedInline):
    '''
    Items in order inline representation.
    '''
    model = models.OrderItems
    fields = ('item','item_quantity','image_preview')
    readonly_fields = ('image_preview',)
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    '''
    Item model representation on admin site.
    '''
    list_display = ('id','email','first_name','last_name','phone','price','created_date')
    search_fields = ('email','first_name','last_name')
    actions = ('close_order', 'process_order', 'cancel_order')
    inlines = (OrderItemInline,)
    date_hierarchy = 'created_date'

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

