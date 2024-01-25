from django.contrib import admin

from .models import User

admin.site.site_header = 'Financial Accounting Admin'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display = ('username', 'email')
    def get_list_display(self, request):
        return [field.name for field in User._meta.fields]

