"""
Views of RepApp.
"""
import datetime
import random
import string
import time
from hashlib import sha256
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.timezone import now
from repapp.models import CustomUser
from .models import Cafe, Device, Guest, OneTimeLogin
from .forms import RegisterDevice, RegisterGuest
from .utils import (send_confirmation_mails, create_one_time_login,
                    send_one_time_login_mail, send_guest_account_mail, is_member)


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
    """
    RegisterDeviceFormView shows the form for registering new devices.
    """
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

        if guest:
            device.guest = guest
            device.save()

            send_confirmation_mails(device, guest, cafe, self.request)

            resp = HttpResponseRedirect(
                reverse_lazy('register_device_final', kwargs={
                    'cafe': cafe.pk,
                    'device_identifier': device.identifier})
            )
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
    """
    View for registering a new guest.
    """
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
            )
            user.set_password(password)
            user.save()

            guest.user = user
            guest.save()

            send_guest_account_mail(guest, password, self.request)

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

        mail = self.kwargs['mail']
        guest = Guest.objects.filter(mail=mail).first()
        if guest:
            return HttpResponseRedirect(
                reverse_lazy('register_device_final', kwargs={
                    'cafe': cafe.pk,
                    'device_identifier': device.identifier})
            )

        context = super(RegisterGuestFormView, self).get_context_data(
            **kwargs
        )
        context["cafe"] = cafe
        context["device"] = device
        context["mail"] = mail

        return context


def register_device_final(request, cafe, device_identifier):
    """
    View to confirm device registration.
    """
    cafe = get_object_or_404(Cafe, pk=cafe)
    device = get_object_or_404(Device, identifier=device_identifier)

    return render(
        request,
        "repapp/register_device_final.html",
        {"device": device, 'cafe': cafe},
    )


@login_required
def device_view(request, device_identifier):
    """
    View for showing device details.
    """
    user = request.user
    if not user:
        raise PermissionDenied()

    device = get_object_or_404(Device, identifier=device_identifier)
    if not device.guest:
        raise PermissionDenied()

    if not (is_member(user) or device.guest.mail == user.email):
        raise PermissionDenied()

    return render(
        request,
        "repapp/device_view.html",
        {"device": device},
    )


@login_required
def profile(request):
    """
    View for showing guest details.
    """
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
    """
    Login page for repair cafe members, using OIDC.
    """
    return render(
        request,
        "repapp/member_login.html"
    )


def cron(request):
    """
    View to trigger automated regular tasks.
    """
    pass


def process_mails(request):
    """
    View to trigger processing of email in inbox.
    """
    pass


def one_time_login(request, secret):
    """
    View for one time login.
    """
    # waste a little time as brute force protection
    time.sleep(1)

    otl = get_object_or_404(OneTimeLogin, secret=secret)

    if otl.login_used:
        messages.add_message(request, messages.ERROR,
                             'Der Einmal-Login wurde schon verwendet und ist nichtmehr gültig.')
        new_otl = create_one_time_login(otl.user, otl.url)
        send_one_time_login_mail(new_otl, request)
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        otl.login_used = True
        otl.login_date = now()
        otl.save()

    user = authenticate(request, username=secret, password=None)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.INFO, 'Login erfolgreich!')
        return HttpResponseRedirect(otl.url)
    else:
        messages.add_message(request, messages.ERROR, 'Login fehlgeschlagen.')
        return HttpResponseRedirect(reverse_lazy('index'))
