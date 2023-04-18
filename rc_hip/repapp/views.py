"""
Views of RepApp.
"""
import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Cafe, Guest, Device


class IndexView(generic.ListView):
    """
    The IndexView lists all future Repair-Cafés.
    """
    template_name = "repapp/index.html"

    def get_queryset(self):
        return Cafe.objects.filter(event_date__gte=datetime.date.today())


def register_device(request, cafe_id):
    if request.method == "POST":
        mail = request.POST.get('email_address', '')
        device = request.POST.get('device', '')
        issue = request.POST.get('issue', ''),
        follow_up = request.POST.get('follow_up', 'false') == 'on'
        return HttpResponse(f"{mail} {device} {issue} {follow_up}")
        # return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    else:
        cafe = get_object_or_404(Cafe, pk=cafe_id)
        return render(
            request,
            "repapp/register_device.html",
            {
                "cafe": cafe,
            },
        )
