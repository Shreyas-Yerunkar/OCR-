from ctypes.wintypes import HGDIOBJ
from distutils.command.upload import upload
from email.mime import image
from pickle import TRUE
from tkinter import CASCADE
from uuid import UUID, uuid4
from django.db import models



class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class ImageTable(BaseClass):
    image=models.ImageField(upload_to='imgupload/files/covers',blank=True,null=True)


class FeedTable(BaseClass):
    image_table=models.ForeignKey(ImageTable, on_delete=models.CASCADE,null=True)
    text=models.CharField(max_length=500,blank=True,null=True)



