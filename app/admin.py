from django.contrib import admin
from .models import License, LicenseLog, User

admin.site.register(License)
admin.site.register(LicenseLog)
admin.site.register(User)
