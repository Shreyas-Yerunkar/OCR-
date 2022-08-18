import imp
from django.contrib import admin
from .models import FeedTable, ImageTable
 

admin.site.register(ImageTable)
admin.site.register(FeedTable)
