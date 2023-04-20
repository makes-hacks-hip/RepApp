"""
Views of RepApp.
"""
import datetime
import os
import random
from hashlib import sha256
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Cafe, Device, Guest, Organisator
from .forms import RegisterDevice, RegisterGuest


class IndexView(generic.ListView):
    """
    The IndexView lists all future Repair-Cafés.
    """
    template_name = "repapp/index.html"

    def get_queryset(self):
        messages.add_message(self.request, messages.INFO,
                             'Dies ist eine Test. Leider können sie sich hier noch nicht anmelden.')
        return Cafe.objects.filter(event_date__gte=datetime.date.today())


class RegisterDeviceFormView(generic.edit.FormView):
    template_name = "repapp/register_device.html"
    form_class = RegisterDevice

    def form_valid(self, form):
        cafe = self.kwargs['cafe']
        cafe = get_object_or_404(Cafe, pk=cafe)

        mail = form.cleaned_data['mail']
        device = form.cleaned_data['device']
        identifier = sha256(
            f'{device}{mail}{datetime.datetime.now()}'.encode('utf-8')
        ).hexdigest()
        secret = sha256(
            f'{device}{mail}{datetime.datetime.now()}{random.randint(0, 999999)}'.encode(
                'utf-8')
        ).hexdigest()
        device = Device(
            identifier=identifier,
            secret=secret,
            device=device,
            error=form.cleaned_data['error'],
            follow_up=form.cleaned_data['follow_up'],
            cafe=cafe,
        )
        device.save()

        guest = Guest.objects.filter(mail=mail).first()

        if guest:
            device.guest = guest
            device.save()
            return HttpResponseRedirect(
                reverse_lazy('register_device_final', kwargs={
                    'cafe': cafe.pk,
                    'deviceentifier': device.identifier,
                    'guestentifier': guest.identifier})
            )
        else:
            return HttpResponseRedirect(
                reverse_lazy('register_guest', kwargs={
                    'cafe': cafe.pk,
                    'deviceentifier': device.identifier,
                    'mail': mail})
            )

    def get_context_data(self, **kwargs):
        cafe = self.kwargs['cafe']
        cafe = get_object_or_404(Cafe, pk=cafe)

        context = super(RegisterDeviceFormView, self).get_context_data(
            **kwargs
        )
        context["cafe"] = cafe
        return context


class RegisterGuestFormView(generic.edit.FormView):
    template_name = "repapp/register_guest.html"
    form_class = RegisterGuest

    def form_valid(self, form):
        cafe = self.kwargs['cafe']
        cafe = get_object_or_404(Cafe, pk=cafe)

        deviceentifier = self.kwargs['deviceentifier']
        device = get_object_or_404(Device, identifier=deviceentifier)

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

        device.guest = guest
        device.save()

        return HttpResponseRedirect(
            reverse_lazy('register_device_final', kwargs={
                'cafe': cafe.pk,
                'deviceentifier': device.identifier,
                'guestentifier': guest.identifier})
        )

    def get_context_data(self, **kwargs):
        cafe = self.kwargs['cafe']
        cafe = get_object_or_404(Cafe, pk=cafe)

        deviceentifier = self.kwargs['deviceentifier']
        device = get_object_or_404(Device, identifier=deviceentifier)

        context = super(RegisterGuestFormView, self).get_context_data(
            **kwargs
        )
        context["cafe"] = cafe
        context["device"] = device
        context["mail"] = self.kwargs['mail']

        return context


def register_device_final(request, cafe, deviceentifier, guestentifier):
    cafe = get_object_or_404(Cafe, pk=cafe)
    device = get_object_or_404(Device, identifier=deviceentifier)
    guest = get_object_or_404(Guest, identifier=guestentifier)

    subject = render_to_string('repapp/mail/mail_register_device_subject.html', {
        'guest': guest,
        'device': device,
        'cafe': cafe,
    }).replace('\n', '')
    text = render_to_string('repapp/mail/mail_register_device_text.html', {
        'guest': guest,
        'device': device,
        'cafe': cafe,
    })
    html = render_to_string('repapp/mail/mail_register_device_html.html', {
        'guest': guest,
        'device': device,
        'cafe': cafe,
    })

    ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[f"{guest.mail}"],
        fail_silently=True,
        html_message=html
    )

    if ok > 0:
        messages.add_message(request, messages.INFO,
                             'Die Bestätigungs-eMail wurde erfolgreich gesendet.')
    else:
        messages.add_message(request, messages.ERROR,
                             'Fehler beim senden der Bestätigungs-eMail!')

    return render(
        request,
        "repapp/register_device_final.html",
        {},
    )


def register_device_confirm(request, deviceentifier, device_secret):
    device = get_object_or_404(Device, identifier=deviceentifier)
    if not device.guest:
        raise Http404('Unknown guest!')

    device.confirmed = True
    device.save()

    if not device.guest.confirmed:
        device.guest.confirmed = True
        device.guest.save()

    text = render_to_string('repapp/mail/notice_new_device.html', {
        'guest': device.guest,
        'device': device,
        'cafe': device.cafe,
    })

    organizers = []
    for organizer in Organisator.objects.all():
        organizers.append(organizer.mail)

    send_mail(
        subject=f"Neues Gerät { device.device }",
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=organizers,
        fail_silently=True
    )

    return render(
        request,
        "repapp/register_device_confirm.html",
        {"device": device, "guest": device.guest, "cafe": device.cafe},
    )


def device_view(request, deviceentifier):
    device = get_object_or_404(Device, identifier=deviceentifier)

    return render(
        request,
        "repapp/device_view.html",
        {"device": device},
    )
