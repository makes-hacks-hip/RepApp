"""
Views of RepApp.
"""
import datetime
from hashlib import sha256
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Cafe, Device, Guest
from .forms import RegisterDevice, RegisterGuest


class IndexView(generic.ListView):
    """
    The IndexView lists all future Repair-Cafés.
    """
    template_name = "repapp/index.html"

    def get_queryset(self):
        return Cafe.objects.filter(event_date__gte=datetime.date.today())


class RegisterDeviceFormView(generic.edit.FormView):
    template_name = "repapp/register_device.html"
    form_class = RegisterDevice

    def form_valid(self, form):
        cafe_id = self.kwargs['cafe_id']
        cafe = get_object_or_404(Cafe, pk=cafe_id)

        mail = form.cleaned_data['mail']
        device = form.cleaned_data['device']
        identifier = sha256(
            f'{device}{mail}{datetime.datetime.now()}'.encode('utf-8')
        ).hexdigest()
        device = Device(
            identifier=identifier,
            device=device,
            error=form.cleaned_data['error'],
            follow_up=form.cleaned_data['follow_up'],
        )
        device.save()

        guest = Guest.objects.filter(mail=mail).first()

        if guest:
            device.guest_id = guest
            device.save()
            return HttpResponseRedirect(
                reverse_lazy('register_device_final', kwargs={
                    'cafe_id': cafe.pk,
                    'device_identifier': device.identifier,
                    'guest_identifier': guest.identifier})
            )
        else:
            return HttpResponseRedirect(
                reverse_lazy('register_guest', kwargs={
                    'cafe_id': cafe.pk,
                    'device_identifier': device.identifier,
                    'mail': mail})
            )

    def get_context_data(self, **kwargs):
        cafe_id = self.kwargs['cafe_id']
        cafe = get_object_or_404(Cafe, pk=cafe_id)

        context = super(RegisterDeviceFormView, self).get_context_data(
            **kwargs
        )
        context["cafe"] = cafe
        return context


class RegisterGuestFormView(generic.edit.FormView):
    template_name = "repapp/register_guest.html"
    form_class = RegisterGuest

    def form_valid(self, form):
        cafe_id = self.kwargs['cafe_id']
        cafe = get_object_or_404(Cafe, pk=cafe_id)

        device_identifier = self.kwargs['device_identifier']
        device = get_object_or_404(Device, identifier=device_identifier)

        name = form.cleaned_data['name']
        residence = form.cleaned_data['residence']
        identifier = sha256(
            f'{name}{residence}{datetime.datetime.now()}'.encode('utf-8')
        ).hexdigest()
        guest = Guest(
            identifier=identifier,
            name=name,
            phone=form.cleaned_data['phone'],
            residence=residence,
            mail=self.kwargs['mail'],
        )
        guest.save()

        device.guest_id = guest
        device.save()

        return HttpResponseRedirect(
            reverse_lazy('register_device_final', kwargs={
                'cafe_id': cafe.pk,
                'device_identifier': device.identifier,
                'guest_identifier': guest.identifier})
        )

    def get_context_data(self, **kwargs):
        cafe_id = self.kwargs['cafe_id']
        cafe = get_object_or_404(Cafe, pk=cafe_id)

        device_identifier = self.kwargs['device_identifier']
        device = get_object_or_404(Device, identifier=device_identifier)

        context = super(RegisterGuestFormView, self).get_context_data(
            **kwargs
        )
        context["cafe"] = cafe
        context["device"] = device
        context["mail"] = self.kwargs['mail']

        return context


def register_device_final(request, cafe_id, device_identifier, guest_identifier):
    cafe = get_object_or_404(Cafe, pk=cafe_id)
    device = get_object_or_404(Device, identifier=device_identifier)
    guest = get_object_or_404(Guest, identifier=guest_identifier)
    print(cafe)
    print(device)
    print(guest)
    return render(
        request,
        "repapp/register_device_final.html",
        {},
    )
