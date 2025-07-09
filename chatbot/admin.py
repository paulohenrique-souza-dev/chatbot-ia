from django.contrib import admin

from .models import Chat
@admin.register(Chat)
class BrandAdmin(admin.ModelAdmin):
    list_display=('user','message')
    search_fields=('user',)
    list_filter=('created_at',)

