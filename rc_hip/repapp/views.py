"""
Views of RepApp.
"""
import datetime
import os
import random
import string
from hashlib import sha256
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from repapp_users.models import CustomUser
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


def send_confirmation_mails(device, guest, cafe, request):
    organizers = []
    for organizer in Organisator.objects.all():
        organizers.append(organizer.mail)

    text = render_to_string('repapp/mail/notice_new_device.html', {
        'guest': device.guest,
        'device': device,
        'cafe': device.cafe,
    })

    send_mail(
        subject=f"Neues Gerät { device.device }",
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=organizers,
        fail_silently=True
    )

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
        device.confirmed = True
        device.save()
    else:
        messages.add_message(request, messages.ERROR,
                             'Fehler beim senden der Bestätigungs-eMail!')


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
        device = Device(
            identifier=identifier,
            device=device,
            manufacturer=form.cleaned_data['manufacturer'],
            error=form.cleaned_data['error'],
            follow_up=form.cleaned_data['follow_up'],
            device_picture=self.request.FILES.get("device_picture", None),
            type_plate_picture=self.request.FILES.get(
                "type_plate_picture", None),
            cafe=cafe,
            confirmed=False,
        )
        device.save()

        guest = Guest.objects.filter(mail=mail).first()

        print(f'Register: Dev: {device}, Guest: {guest}')

        if guest:
            print('Guest already known')
            device.guest = guest
            device.save()

            send_confirmation_mails(device, guest, cafe, self.request)

            print('Mails sent')

            resp = HttpResponseRedirect(
                reverse_lazy('register_device_final', kwargs={
                    'cafe': cafe.pk,
                    'device_identifier': device.identifier})
            )
            print(resp)
            return resp
        else:
            return HttpResponseRedirect(
                reverse_lazy('register_guest', kwargs={
                    'cafe': cafe.pk,
                    'device_identifier': device.identifier,
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

        device_identifier = self.kwargs['device_identifier']
        device = get_object_or_404(Device, identifier=device_identifier)

        name = form.cleaned_data['name']
        mail = self.kwargs['mail']
        residence = form.cleaned_data['residence']
        identifier = sha256(
            f'{name}{residence}{datetime.datetime.now()}'.encode('utf-8')
        ).hexdigest()
        guest = Guest(
            identifier=identifier,
            name=name,
            phone=form.cleaned_data['phone'],
            residence=residence,
            mail=mail,
        )
        guest.save()

        device.guest = guest
        device.save()

        if not CustomUser.objects.filter(email=mail).exists():
            password = ''.join(random.choice(string.ascii_letters)
                               for i in range(10))
            user = CustomUser.objects.create_user(
                username=name,
                email=mail,
                password=password)
            user.save()

            print(f'{mail} {password}')
            # TODO: send account creation email

        send_confirmation_mails(device, guest, cafe, self.request)

        return HttpResponseRedirect(
            reverse_lazy('register_device_final', kwargs={
                'cafe': cafe.pk,
                'device_identifier': device.identifier})
        )

    def get_context_data(self, **kwargs):
        cafe = self.kwargs['cafe']
        cafe = get_object_or_404(Cafe, pk=cafe)

        device_identifier = self.kwargs['device_identifier']
        device = get_object_or_404(Device, identifier=device_identifier)

        context = super(RegisterGuestFormView, self).get_context_data(
            **kwargs
        )
        context["cafe"] = cafe
        context["device"] = device
        context["mail"] = self.kwargs['mail']

        return context


def register_device_final(request, cafe, device_identifier):
    cafe = get_object_or_404(Cafe, pk=cafe)
    device = get_object_or_404(Device, identifier=device_identifier)

    return render(
        request,
        "repapp/register_device_final.html",
        {"device": device, 'cafe': cafe},
    )


@login_required
def device_view(request, device_identifier):
    user = request.user
    if not user:
        raise PermissionDenied()

    device = get_object_or_404(Device, identifier=device_identifier)
    if not device.guest:
        raise PermissionDenied()

    # TODO: Guests can only view their devices, Reparateur and Orga can view all devices.

    return render(
        request,
        "repapp/device_view.html",
        {"device": device},
    )


@login_required
def profile(request):
    user = request.user
    if not user:
        raise PermissionDenied()

    guest = get_object_or_404(Guest, mail=user.email)

    return render(
        request,
        "repapp/guest_profile.html",
        {
            'guest': guest
        }
    )


def member_login(request):
    return render(
        request,
        "repapp/member_login.html"
    )
