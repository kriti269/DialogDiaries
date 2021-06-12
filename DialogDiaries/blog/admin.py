from django.contrib import admin
from .models import Post, Tag, ContactUs, Category

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(ContactUs)