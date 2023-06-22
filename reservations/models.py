from django.db import models
from hotel.models import Product, Variation
from accounts.models import Account
import datetime



# Create your models here.

class Reservation(models.Model):
    reservation_id  = models.CharField(max_length=250, blank=True)
    date_added  = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.reservation_id
    
    
    
    
class ReservationItem(models.Model):
    user    = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations   = models.ManyToManyField(Variation, blank=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active   = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return  self.product.price * self.quantity 
    
    
    def __unicode__(self):
        return self.product