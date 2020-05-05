from django.contrib import admin
from .models import Product, Category, Info, InfoCategory, Contact, CustomUser, Comment
from adminsortable.admin import SortableAdmin
from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(SortableAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    

class InfoAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ('title', 'is_public')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email')
    
class InfoCategoryAdmin(SortableAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(InfoCategory, InfoCategoryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(CustomUser)
admin.site.register(Comment)