from django.shortcuts import render
from django.http import HttpResponse


def stats(request):
    return render(request, "stats.html")


def stats_medios(request, tipo):
    return render(request, "stats.html")


def total_movimientos(request):
    return 3


def total_usuarios(request):
    return HttpResponse('3')


def testingView(request):
    return render('testing...')
