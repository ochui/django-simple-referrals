from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import FlatReferral, Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'token']
    readonly_fields = ['token']


admin.site.register(FlatReferral)
