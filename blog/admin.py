from django.contrib import admin
from .models import Post,Category,Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','ctime','mtime','category','auther']

class CategoryAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)