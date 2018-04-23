from django.contrib import admin

from .models import Provider


def regenerate_token(modeladmin, request, queryset):
    for provider in queryset:
        provider.generate_token()


regenerate_token.short_description = 'Regenerate token'


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'phone_number',)
    search_fields = ('name', 'email', 'phone_number',)
    actions = [
        regenerate_token,
    ]
