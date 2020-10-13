from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DecimalField, TextField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


class Category(models.Model):
    '''
    Model for shop category.
    '''
    name = models.CharField(_("name"), max_length=254, db_index=True, unique=True)
    slug = models.SlugField(max_length=254, db_index=True, unique=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



def image_upload_path(instance, filename):
    '''
    Function that create path for saving item img depends on item slug field.
    '''
    return f"images/{instance.slug}.png"

class Product(models.Model):
    '''
    Model for shop items.
    '''
    name = models.CharField(_("name"), max_length=254, db_index=True, unique=True)
    slug = models.SlugField(max_length=254, db_index=True, unique=True)
    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2)
    description = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to=image_upload_path)
    category = models.ForeignKey("Category",on_delete=models.SET_NULL, null=True, related_name="products")
    available = models.BooleanField(_("available"), default=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def image_preview(self):
        image = self.image
        if image:
            return mark_safe('<img src="{0}" width="50" height="50" />'.format(image.url))
        else:
            return '(No image)'



class Order(models.Model):
    '''
    Model to store shop orders.
    '''

    class Status(models.IntegerChoices):
        WAITING = 0, _("waiting")
        PROCESSING = 1, _("processing")
        DONE = 2, _("done")
        CANCELED = 3, _("canceled")

    items = models.ManyToManyField('Product', through='OrderItems')
    first_name = models.CharField(_("first name"), max_length=254)
    last_name = models.CharField(_("last name"), max_length=254)
    email = models.EmailField(_("email"), max_length=254, db_index=True)
    phone = models.CharField(_("phone"), max_length=12, ) #TODO: add phone validator
    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2, null=True) 
    status = models.IntegerField(_("status"), choices=Status.choices, default=Status.WAITING)
    comment = models.TextField(_("comment"),blank=True,null=True)

    def calc_price(self):
        # e = models.ExpressionWrapper(models.F('item_count') * models.F('item__price'), output_field=models.DecimalField(max_digits=10,decimal_places=2))
        # return self.orderitems_set.annotate(price=e).aggregate(models.Sum('price'))['price__sum']
        return sum( (i.item.price * i.item_quantity for i in self.items.through.objects.all()) )



class OrderItems(models.Model):
    item = models.ForeignKey('Product', on_delete=CASCADE)
    order = models.ForeignKey('Order', on_delete=CASCADE)
    item_quantity = models.PositiveIntegerField(_('quantity'))

    def image_preview(self):
        return self.item.image_preview()