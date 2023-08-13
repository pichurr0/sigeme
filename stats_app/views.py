from django.shortcuts import render
from django.http import HttpResponse


def stats(request):
    return render(request, "stats.html")


def stats_medios(request, tipo):
    return render(f'testing...{tipo}')


def total_usuarios(request):
    return HttpResponse('3')
