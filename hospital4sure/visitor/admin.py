from .models import *
from django.contrib import admin

# Register your models here.

admin.site.register(VisitorProfile)
admin.site.register(Appointment)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(TemporaryBloodbankVisitor)