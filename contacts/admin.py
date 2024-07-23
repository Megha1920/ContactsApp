from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address', 'company')
    search_fields = ('first_name', 'last_name', 'address', 'company')
    list_filter = ('company',)  # Add filters based on company
    ordering = ('last_name', 'first_name')  # Default ordering

    # Optional: Customize the form for better management of phone numbers
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Customize form fields or widgets if needed
        return form
