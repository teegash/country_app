from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Country, County, Subcounty, Locationplace, Sublocation


# renders home
def home(request):
    return render(request, 'home.html')

# loads locations
def load_locations(request):
    location_type = request.GET.get('location_type')
    if location_type == 'country':
        locations = list(Country.objects.values())
    elif location_type == 'county':
        locations = list(County.objects.values())
    elif location_type == 'subcounty':
        locations = list(Subcounty.objects.values())
    elif location_type == 'locationplace':
        locations = list(Locationplace.objects.values())
    elif location_type == 'sublocation':
        locations = list(Sublocation.objects.values())
    else:
        locations = []
        
    return JsonResponse(locations, safe=False)

# gets location data from database
def get_location_data(request):
    location_type = request.GET.get('location_type')
    location_id = request.GET.get('location_id')

    if location_type == 'country':
        location = Country.objects.get(id=location_id)
        data = {'name': location.name, 'country': location.name}
    elif location_type == 'county':
        location = County.objects.get(id=location_id)
        data = {'name': location.name, 'country': location.country.name}
    elif location_type == 'subcounty':
        location = Subcounty.objects.get(id=location_id)
        data = {'name': location.name, 'county': location.county.name, 'country': location.county.country.name}
    elif location_type == 'locationplace':
        location = Locationplace.objects.get(id=location_id)
        data = {'name': location.name, 'subcounty': location.subcounty.name, 'county': location.subcounty.county.name, 'country': location.subcounty.county.country.name}
    elif location_type == 'sublocation':
        location = Sublocation.objects.get(id=location_id)
        data = {'name': location.name, 'locationplace': location.locationplace.name, 'subcounty': location.locationplace.subcounty.name, 'county': location.locationplace.subcounty.county.name, 'country': location.locationplace.subcounty.county.country.name}
    else:
        data = {}

    return JsonResponse(data)

# adds country, county, subcounty, locationplace, and sublocation
def add(request):
    if request.method == 'POST':
        country_name = request.POST.get('country')
        county_name = request.POST.get('county')
        subcounty_name = request.POST.get('subcounty')
        locationplace_name = request.POST.get('locationplace')
        sublocation_name = request.POST.get('sublocation')

        country, created = Country.objects.get_or_create(name=country_name)
        county, created = County.objects.get_or_create(name=county_name, country=country)
        subcounty, created = Subcounty.objects.get_or_create(name=subcounty_name, county=county)
        locationplace, created = Locationplace.objects.get_or_create(name=locationplace_name, subcounty=subcounty)
        Sublocation.objects.create(name=sublocation_name, locationplace=locationplace)

        return redirect('add')
    return render(request, 'add.html')
