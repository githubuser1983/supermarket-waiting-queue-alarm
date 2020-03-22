from django.contrib import admin

from .models import Supermarket, Cities, Warn

admin.site.register(Supermarket)
admin.site.register(Cities)
admin.site.register(Warn)
