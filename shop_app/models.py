from django.db import models
from django.db.models.fields import CharField, DecimalField, TextField
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

    first_name = models.CharField(_("first name"), max_length=254)
    last_name = models.CharField(_("last name"), max_length=254)
    email = models.EmailField(_("email"), max_length=254, db_index=True)
    phone = models.CharField(_("phone"), max_length=12, ) #TODO: add phone validator
    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2) 
    status = models.IntegerField(_("status"), choices=Status.choices, default=Status.WAITING)
    comment = models.TextField(_("comment"),blank=True,null=True)
