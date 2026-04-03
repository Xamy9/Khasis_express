from django.contrib import admin
from .models import ServiceRequest,BusinessImage
from .models import LandingPage

admin.site.register(ServiceRequest)
admin.site.register(BusinessImage)
admin.site.register(LandingPage)