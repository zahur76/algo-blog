from django.contrib import admin
from .models import SiteHits

# Register your models here.
# Register your models here.
class siteHitsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "count",
        "visitors"
    )

admin.site.register(SiteHits, siteHitsAdmin)