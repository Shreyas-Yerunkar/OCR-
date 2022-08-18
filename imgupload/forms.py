from dataclasses import fields
from socket import fromshare
from django.forms import ModelForm
from django import forms
from .models import ImageTable

class UploadForm(ModelForm):

    image=forms.ImageField()

    class Meta:
        model=ImageTable
        fields=['image']



