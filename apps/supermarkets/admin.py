from django.contrib import admin

from .models import Supermarket, City, Warn

admin.site.register(Supermarket)
admin.site.register(City)
admin.site.register(Warn)
