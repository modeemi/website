from django.http import Http404
from django.shortcuts import render_to_response

def etusivu(request):
    return render_to_response('etusivu.html')

def yhdistys(request):
    return render_to_response('yhdistys.html')

def palvelut(request):
    return render_to_response('palvelut.html')

def jaseneksi(request):
    return render_to_response('jaseneksi.html')

def laitteisto(request):
    return render_to_response('laitteisto.html')
