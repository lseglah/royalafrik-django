from django.contrib import admin
from .models import Reservation, ReservationItem 

# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display    = ('reservation_id',  'date_added')
    

    
class ReservationItemAdmin(admin.ModelAdmin):
    list_display    = ('product', 'reservation', 'quantity', 'is_active')


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationItem, ReservationItemAdmin)