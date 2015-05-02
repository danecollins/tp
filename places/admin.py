from django.contrib import admin

# Register your models here.
from places.models import City, Place, UserInfo, Locale
admin.site.register(City)
admin.site.register(Place)
admin.site.register(Locale)
admin.site.register(UserInfo)
