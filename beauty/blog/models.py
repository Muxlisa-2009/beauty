from email.mime import text
from multiprocessing import context

from django.core.management.commands import makemigrations, migrate
from django.db import models


from django.db import models



class Kiyim(models.Model):
    nomi=models.CharField(max_length=100)
    turi=models.CharField(max_length=50)
    rangi=models.CharField(max_length=50)
    olchami=models.CharField(max_length=20)
    narxi=models.IntegerField()
    rasmi=models.ImageField(upload_to='kiyimlar/',blank=True, null=True)


    def __str__(self):
        return self .nomi

from django.shortcuts import render
from.models import Kiyim

def kiyimlar(request):
    kiyimlar=Kiyim.objects.all()
    context ={
        'kiyimlar':kiyimlar
    }
    return render(request ,'kiyimlar.html',context)
















