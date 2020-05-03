from django.contrib import admin
from .models import Product, Category, News, NewsCategory, Contact, CustomUser, Comment
from adminsortable.admin import SortableAdmin
from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(SortableAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    

class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ('title', 'is_public')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email')
    
class NewsCategoryAdmin(SortableAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(CustomUser)
admin.site.register(Comment)