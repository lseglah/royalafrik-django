from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from hotel.models import Product, Variation
from .models import Reservation, ReservationItem
from django.contrib.auth.decorators import login_required




# Create your views here.


def _reservation_id(request):
    reservation = request.session.session_key
    if not reservation:
        reservation = request.session.create()
    return reservation

def add_reservation(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

            is_reservation_item_exists = ReservationItem.objects.filter(product=product, user=current_user).exists()
            if is_reservation_item_exists:
                reservation_item = ReservationItem.objects.filter(product=product, user=current_user)
                ex_var_list = []
                id = []
                for item in reservation_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

                if product_variation in ex_var_list:
                    # increase the reservation item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = ReservationItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()

                else:
                    item = ReservationItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
            else:
                reservation_item = ReservationItem.objects.create(
                    product = product,
                    quantity = 1, 
                    user = current_user,
                )
                if len(product_variation) > 0:
                    reservation_item.variations.clear()
                    reservation_item.variations.add(*product_variation)
                reservation_item.save()
            return redirect('reservation')

    # Not Authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

            try:
                reservation = Reservation.objects.get(reservation_id=_reservation_id(request)) # get the reservation using the reservation_id present in the session
            except Reservation.DoesNotExist:
                reservation = Reservation.objects.create(
                    reservation_id = _reservation_id(request)
                )
            reservation.save()



            is_reservation_item_exists = ReservationItem.objects.filter(product=product, reservation=reservation).exists()
            if is_reservation_item_exists:
                reservation_item = ReservationItem.objects.filter(product=product, reservation=reservation)
                ex_var_list = []
                id = []
                for item in reservation_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                    
                if product_variation in ex_var_list:
                    # increase the reservation item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = ReservationItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()

                else:
                    item = ReservationItem.objects.create(product=product, quantity=1, reservation=reservation)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
            else:
                reservation_item = ReservationItem.objects.create(
                    product = product,
                    quantity = 1,
                    reservation = reservation,
                )
                if len(product_variation) > 0:
                    reservation_item.variations.clear()
                    reservation_item.variations.add(*product_variation)
                reservation_item.save()
            return redirect('reservation') 


def remove_reservation(request, product_id, reservation_item_id):   
    product     = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            reservation_item    = ReservationItem.objects.get(product=product, user=request.user, id=reservation_item_id)
        else:
            reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
            reservation_item    = ReservationItem.objects.get(product=product, reservation=reservation, id=reservation_item_id)
        if reservation_item.quantity > 1:
            reservation_item.quantity -= 1
            reservation_item.save()
        else:
            reservation_item.delete()
    except:
        pass
    return redirect('reservation')


def remove_reservation_item(request, product_id, reservation_item_id):
    product         = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        reservation_item     = ReservationItem.objects.get(product=product, user=request.user, id=reservation_item_id)
    else:
        reservation     = Reservation.objects.get(reservation_id=_reservation_id(request))
        reservation_item     = ReservationItem.objects.get(product=product, reservation=reservation, id=reservation_item_id)
    reservation_item.delete()
    return redirect('reservation')
        

 

def reservation(request, total=0, quantity=0, reserved_days=0, reservation_items=None):
    try:
        tax     = 0
        grand_total = 0
        if request.user.is_authenticated:
            reservation_items = ReservationItem.objects.filter(user=request.user, is_active=True)
        else:            
            reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
            reservation_items = ReservationItem.objects.filter(reservation=reservation, is_active=True)
        for reservation_item in reservation_items:
            total   += (reservation_item.product.price* reservation_item.quantity)
            quantity     += reservation_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax 
    except ObjectDoesNotExist:
        pass #just ignore
    
    context = {
       'reservation_items': reservation_items,
        'total': total,
        'quantity': quantity,
        'reserved_days': reserved_days,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'hotel/reservation.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, reservation_items=None):
    try:
        tax     = 0
        grand_total = 0
        if request.user.is_authenticated:
            reservation_items = ReservationItem.objects.filter(user=request.user, is_active=True)
        else:            
            reservation = Reservation.objects.get(reservation_id=_reservation_id(request))
            reservation_items = ReservationItem.objects.filter(reservation=reservation, is_active=True)
        for reservation_item in reservation_items:
            total   += (reservation_item.product.price* reservation_item.quantity)
            quantity     += reservation_item.quantity
        tax = (10 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    
    context = {
       'reservation_items': reservation_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'hotel/checkout.html', context)