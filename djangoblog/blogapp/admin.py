from django.contrib import admin
from .models import author, category, article,comment

# Register your models here.

admin.site.register(author)
admin.site.register(category)
admin.site.register(article)
admin.site.register(comment)
