from django.db import models


# Country
# class Country(models.Model):
#     name = models.CharField(max_length=100)

# class County(models.Model):
#     name = models.CharField(max_length=100)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)

# class Subcounty(models.Model):
#     name = models.CharField(max_length=100)
#     county = models.ForeignKey(County, on_delete=models.CASCADE)

# class Locationplace(models.Model):
#     name = models.CharField(max_length=100)
#     subcounty = models.ForeignKey(Subcounty, on_delete=models.CASCADE)

# class Sublocation(models.Model):
#     name = models.CharField(max_length=100)
#     locationplace = models.ForeignKey(Locationplace, on_delete=models.CASCADE)

# from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

class County(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='counties', on_delete=models.CASCADE)

class Subcounty(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, related_name='subcounties', on_delete=models.CASCADE)

class Locationplace(models.Model):
    name = models.CharField(max_length=100)
    subcounty = models.ForeignKey(Subcounty, related_name='locationplaces', on_delete=models.CASCADE)

class Sublocation(models.Model):
    name = models.CharField(max_length=100)
    locationplace = models.ForeignKey(Locationplace, related_name='sublocations', on_delete=models.CASCADE)
