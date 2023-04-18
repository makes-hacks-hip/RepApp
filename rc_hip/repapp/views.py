from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Cafe


def index(request):
    return HttpResponse("Hello from RepApp.")


class IndexView(generic.ListView):
    template_name = "repapp/index.html"

    def get_queryset(self):
        return Cafe.objects.all()
