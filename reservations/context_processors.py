from .models import Reservation, ReservationItem
from .views import _reservation_id

def counter(request):
    reservation_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            reservation = Reservation.objects.filter(reservation_id=_reservation_id(request))
            if request.user.is_authenticated:
                reservation_items   = ReservationItem.objects.all().filter(user=request.user)
            else:
                reservation_items = ReservationItem.objects.all().filter(reservation=reservation[:1])

            for reservation_item in reservation_items:
                reservation_count += reservation_item.quantity

        except Reservation.DoesNotExist:
            reservation_count = 0 
        
    return dict(reservation_count=reservation_count) 