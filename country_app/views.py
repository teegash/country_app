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

def load_locations2(request):
    location_type = request.GET.get('location_type')
    location_id = request.GET.get('location_id')

    if location_type == 'county':
        country_ids = Country.objects.values_list('id', flat=True)
        locations = list(County.objects.filter(country_id=country_ids).values())
    elif location_type == 'subcounty':
        county_ids = County.objects.filter(country_id=location_id).values_list('id', flat=True)
        locations = list(Subcounty.objects.filter(county_id=county_ids).values())
    elif location_type == 'locationplace':
        subcounty_ids = Subcounty.objects.filter(county_id=location_id).values_list('id', flat=True)
        locations = list(Locationplace.objects.filter(subcounty_id__in=subcounty_ids).values())
    elif location_type == 'sublocation':
        locationplace_ids = Locationplace.objects.filter(subcounty__county_id=location_id).values_list('id', flat=True)
        locations = list(Sublocation.objects.filter(locationplace_id__in=locationplace_ids).values())
    else:
        locations = []

    return JsonResponse(locations, safe=False)



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
