from django.contrib import admin
from .models import customer_user
# Register your models here.


class ViewuserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.id)

admin.site.register(customer_user,ViewuserAdmin)
