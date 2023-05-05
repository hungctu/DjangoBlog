from django.contrib import admin
from .models import book,category,chapter,topic,comment,rating,category_book,topic_book

# Register your models here.

class ViewBookAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user)



class ViewChapAdmin(admin.ModelAdmin):
    def get_queryset(self, request):

        if request.user.is_superuser:
            print(chapter.objects.all())
            return chapter.objects.all()
        return chapter.objects.all().select_related('book').filter(book__user_id=request.user)

admin.site.register(category)
admin.site.register(topic)
admin.site.register(book,ViewBookAdmin)
admin.site.register(chapter,ViewChapAdmin)
admin.site.register(comment)
admin.site.register(rating)
admin.site.register(category_book)
admin.site.register(topic_book)