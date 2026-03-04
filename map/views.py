from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from map.models import location
from cart.models import Item
from django.db.models import Sum

@login_required(login_url='/accounts/login/')
def index(request):
    # 1. Filter to only get locations that are linked to at least one Order
    locations_with_orders = location.objects.filter(order__isnull=False).distinct()
    
    trending_data = []

    for loc in locations_with_orders:
        # 2. Filter items by the new Order.location relationship
        items_in_loc = Item.objects.filter(order__location=loc)
        
        if items_in_loc.exists():
            # 3. Aggregate quantities to find the top movie
            top_movie = items_in_loc.values('movie__name').annotate(
                total_purchased=Sum('quantity')
            ).order_by('-total_purchased').first()

            if top_movie:
                trending_data.append({
                    'city': loc.city,
                    'state': loc.state,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'top_movie': top_movie['movie__name'],
                    'purchase_count': top_movie['total_purchased']
                })

    context = {'cities': trending_data}
    return render(request, 'map/index.html', context)