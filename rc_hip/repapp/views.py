"""
Views of RepApp.
"""
import datetime
import random
import string
import time
import os
import logging
from hashlib import sha256
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from .forms import RegisterDevice, RegisterGuest, Mail, UpdateDeviceForm, MemberSettings
from .models import (Cafe, Device, Guest, OneTimeLogin, Question,
                     CustomUser, Organisator, Reparateur)
from . import mail_interface


logger = logging.getLogger(__name__)


def send_one_time_login_mail(secret, mail, request):
    """
    Send a mail with a one time login link.
    """
    url = request.build_absolute_uri(
        f'/onetimelogin/{secret}/')
    subject = render_to_string(
        'repapp/mail/mail_one_time_login_subject.html').replace('\n', '')
    html = render_to_string('repapp/mail/mail_one_time_login_html.html', {
        'link': url,
    })
    soup = BeautifulSoup(html)
    text = soup.get_text('\n')

    send_ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[mail],
        fail_silently=True,
        html_message=html
    )

    if send_ok > 0:
        messages.add_message(request, messages.INFO,
                             'Sie haben einen neuen Login per eMail erhalten.')


def send_confirmation_mails(device, guest, cafe, request):
    """
    Send confirmation mails for device registration.
    """
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

    path = reverse('view_device', kwargs={
                   'device_identifier': device.identifier})
    url = request.build_absolute_uri(path)
    secret = create_one_time_login(guest.user, url)
    login_url = request.build_absolute_uri(f'/onetimelogin/{secret}/')

    subject = render_to_string('repapp/mail/mail_register_device_subject.html', {
        'cafe': cafe,
    }).replace('\n', '')
    html = render_to_string('repapp/mail/mail_register_device_html.html', {
        'guest': guest,
        'device': device,
        'cafe': cafe,
        'login_url': login_url,
    })
    soup = BeautifulSoup(html)
    text = soup.get_text('\n')

    mail_count = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[f"{guest.mail}"],
        fail_silently=True,
        html_message=html
    )

    if mail_count > 0:
        device.confirmed = True
        device.save()
    else:
        messages.add_message(request, messages.ERROR,
                             'Fehler beim senden der Bestätigungs-eMail!')


def send_guest_account_mail(guest, password, request):
    """
    Send guest user account created mail.
    """
    url = request.build_absolute_uri('/guest/profile/')
    subject = render_to_string(
        'repapp/mail/mail_new_guest_subject.html').replace('\n', '')
    html = render_to_string('repapp/mail/mail_new_guest_html.html', {
        'link': url,
        'username': guest.user.email,
        'password': password,
    })
    soup = BeautifulSoup(html)
    text = soup.get_text('\n')

    send_ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[f"{guest.user.email}"],
        fail_silently=True,
        html_message=html
    )

    if send_ok > 0:
        messages.add_message(request, messages.INFO,
                             'Sie haben ihre Benutzerdaten per eMail erhalten.')


def send_device_reject_mail(device, reply, request):
    """
    Send a mail to reject the given device.
    """
    subject = render_to_string(
        'repapp/mail/mail_reject_device_subject.html', {
            'device': device
        }).replace('\n', '')

    soup = BeautifulSoup(reply)
    text = soup.get_text('\n')

    send_ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[device.guest.mail],
        fail_silently=True,
        html_message=reply
    )

    if send_ok > 0:
        messages.add_message(request, messages.INFO,
                             f'Das Gerät {device.device} wurde abgelehnt.')


def send_device_question_mail(question, request):
    """
    Send a mail to ask more details about an device.
    """
    subject = render_to_string(
        'repapp/mail/mail_question_device_subject.html', {
            'device': question.device,
            'question': question,
        }).replace('\n', '')

    soup = BeautifulSoup(question.question)
    text = soup.get_text('\n')

    send_ok = send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=[question.device.guest.mail],
        fail_silently=True,
        html_message=question.question
    )

    if send_ok > 0:
        question.sent = True
        question.save()

        messages.add_message(request, messages.INFO,
                             f'Die Rückfrage zum Gerät {question.device.device} wurde gesendet.')


def is_member(user):
    """
    Test is a user is a Repair-Café member.
    """
    organisator = Organisator.objects.filter(mail=user.email).first()
    reparateur = Reparateur.objects.filter(mail=user.email).first()
    return organisator or reparateur


def is_organisator(user):
    """
    Test is a user is a Repair-Café organisator.
    """
    organisator = Organisator.objects.filter(mail=user.email).first()
    return organisator is not None


def is_reparateur(user):
    """
    Test is a user is a Repair-Café reparateur.
    """
    reparateur = Reparateur.objects.filter(mail=user.email).first()
    return reparateur is not None


def create_one_time_login(user, url) -> str:
    """
    create_one_time_login creates a one time login object for guest user logins.
    """
    secret = sha256(
        f'{user.email}{url}{datetime.datetime.now()}{random.randint(0,9999999)}'.encode(
            'utf-8')
    ).hexdigest()
    secret_hash = sha256(secret.encode('utf-8')).hexdigest()
    otl = OneTimeLogin(
        secret=secret_hash,
        user=user,
        url=url,
    )
    otl.save()
    return secret


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
        user = CustomUser.objects.filter(email=mail).first()

        if guest and user:
            device.guest = guest
            device.save()

            guest.user = user
            guest.save()

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

            username = name
            i = 1
            while CustomUser.objects.filter(username=username).first():
                username = f'{name}{i}'
                i = i + 1

            user = CustomUser.objects.create_user(
                username=username,
                email=mail,
            )
            user.set_password(password)
            user.save()

            guest.user = user
            guest.save()

            # Simplify flow for guests, hide account and use only one-time-login
            # send_guest_account_mail(guest, password, self.request)

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


def member(request):
    """
    Login page for repair cafe members, using OIDC.
    """
    # TODO: test
    logger.debug('Member-View: User: %s', str(request.user))
    if request.user.is_anonymous or not is_member(request.user):
        return HttpResponseRedirect(reverse_lazy('oidc_authentication_init'))

    if is_organisator(request.user) and is_reparateur(request.user):
        return HttpResponseRedirect(reverse_lazy('select_role'))

    if is_organisator(request.user):
        return HttpResponseRedirect(reverse_lazy('orga'))

    if is_reparateur(request.user):
        return HttpResponseRedirect(reverse_lazy('repa'))

    logger.warning('User %s is no member!', str(request.user))
    raise PermissionDenied('No member!')


@login_required(login_url=reverse_lazy('member'))
def orga(request):
    """
    Landing page for organisators.
    """
    # TODO: test
    if not is_organisator(request.user):
        logger.warning('The user %s is no organisator!', str(request.user))
        raise PermissionDenied('Not organisator!')

    devices = Device.objects.filter(status=0).order_by('-date')
    questions_not_sent = Question.objects.filter(sent=False).order_by('-date')
    questions_open_and_answered = Question.objects.filter(
        open=True, answered=True).order_by('-date')

    next_cafe = Cafe.objects.filter(
        event_date__gte=datetime.datetime.today()).order_by('event_date').first()

    return render(
        request,
        "repapp/orga/main.html",
        {
            'devices': devices,
            'questions_not_sent': questions_not_sent,
            'questions_open_and_answered': questions_open_and_answered,
            'next_cafe': next_cafe,
        }
    )


@login_required(login_url=reverse_lazy('member'))
def review_device(request, device):
    """
    Review new device registration.
    """
    # TODO: test
    if not is_organisator(request.user):
        logger.warning('The user %s is no organisator!', str(request.user))
        raise PermissionDenied('Not organisator!')

    device = get_object_or_404(Device, pk=device)

    return render(
        request,
        "repapp/orga/review_device.html",
        {
            'device': device
        }
    )


@login_required(login_url=reverse_lazy('member'))
def review_device_accept(request, device):
    """
    Review new device registration.
    """
    # TODO: test
    if not is_organisator(request.user):
        logger.warning('The user %s is no organisator!', str(request.user))
        raise PermissionDenied('Not organisator!')

    device = get_object_or_404(Device, pk=device)
    device.status = 3
    device.save()

    return HttpResponseRedirect(reverse_lazy('orga'))


class RejectDeviceFormView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.FormView):
    """
    View for rejecting a device.
    """
    template_name = "repapp/orga/review_device_reject.html"
    form_class = Mail
    login_url = reverse_lazy('member')

    def test_func(self):
        return is_organisator(self.request.user)

    def form_valid(self, form):
        device = self.kwargs['device']
        device = get_object_or_404(Device, pk=device)

        message = form.cleaned_data['message']

        send_device_reject_mail(device, message, self.request)

        device.status = -1
        device.save()

        return HttpResponseRedirect(
            reverse_lazy('orga')
        )

    def get_initial(self, **kwargs):
        device = self.kwargs['device']
        device = get_object_or_404(Device, pk=device)

        text = render_to_string('repapp/mail/mail_reject_device_html.html', {
            'device': device,
        })

        initial = super(RejectDeviceFormView, self).get_initial()
        initial['message'] = text

        return initial

    def get_context_data(self, **kwargs):
        device = self.kwargs['device']
        device = get_object_or_404(Device, pk=device)

        context = super(RejectDeviceFormView, self).get_context_data(
            **kwargs
        )
        context["device"] = device

        return context


class QuestionDeviceFormView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.FormView):
    """
    View for rejecting a device.
    """
    template_name = "repapp/orga/device_question.html"
    form_class = Mail
    login_url = reverse_lazy('member')

    def test_func(self):
        return is_organisator(self.request.user)

    def form_valid(self, form):
        device = self.kwargs['device']
        device = get_object_or_404(Device, pk=device)

        question = None
        message = form.cleaned_data['message']
        mail = self.request.user.email
        organisator = Organisator.objects.filter(mail=mail).first()
        if organisator:
            question = Question(
                question=message,
                organisator=organisator,
                device=device
            )
        else:
            raise PermissionDenied('Not valid member found!')
        question.save()

        send_device_question_mail(question, self.request)

        device.status = 1
        device.save()

        return HttpResponseRedirect(
            reverse_lazy('orga')
        )

    def get_initial(self, **kwargs):
        device = self.kwargs['device']
        device = get_object_or_404(Device, pk=device)

        text = render_to_string('repapp/mail/mail_question_device_html.html', {
            'device': device,
        })

        initial = super(QuestionDeviceFormView, self).get_initial()
        initial['message'] = text

        return initial

    def get_context_data(self, **kwargs):
        device = self.kwargs['device']
        device = get_object_or_404(Device, pk=device)

        context = super(QuestionDeviceFormView, self).get_context_data(
            **kwargs
        )
        context["device"] = device

        return context


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    """
    Organisator view for edit a Repair-Café.
    """
    # TODO: create test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/edit_question.html"
    model = Question
    form_class = UpdateDeviceForm
    success_url = reverse_lazy('orga')

    def test_func(self):
        return is_organisator(self.request.user)

    def form_valid(self, form):
        response = super(QuestionUpdateView, self).form_valid(form)

        question = self.kwargs['pk']
        question = get_object_or_404(Question, pk=question)
        send_device_question_mail(question, self.request)

        return response

    def get_context_data(self, **kwargs):
        question = self.kwargs['pk']
        question = get_object_or_404(Question, pk=question)

        context = super(QuestionUpdateView, self).get_context_data(
            **kwargs
        )
        context["question"] = question
        context["show_guest"] = True

        return context


@login_required(login_url=reverse_lazy('member'))
def question(request, question):
    """
    Review new device registration.
    """
    # TODO: test
    if not is_member(request.user):
        raise PermissionDenied('Not member!')

    question = get_object_or_404(Question, pk=question)
    show_guest = False
    if is_organisator(request.user):
        show_guest = True

    return render(
        request,
        "repapp/orga/question.html",
        {
            'question': question,
            'show_guest': show_guest
        }
    )


@login_required(login_url=reverse_lazy('member'))
def questions(request):
    """
    List of all questions.
    """
    # TODO: test
    if not is_member(request.user):
        raise PermissionDenied('Not organisator!')

    questions = Question.objects.order_by('-date')

    return render(
        request,
        "repapp/orga/questions.html",
        {
            'questions': questions,
        }
    )


@login_required(login_url=reverse_lazy('member'))
def select_role(request):
    """
    Landing page for organisators.
    """
    # TODO: test
    if not is_organisator(request.user):
        logger.warning('The user %s is no organisator!', str(request.user))
        raise PermissionDenied('Not organisator!')

    if not is_reparateur(request.user):
        logger.warning('The user %s is no reparateur!', str(request.user))
        raise PermissionDenied('Not reparateur!')

    return render(
        request,
        "repapp/orga/select_role.html"
    )


@login_required(login_url=reverse_lazy('member'))
def repa(request):
    """
    Organisator main menu.
    """
    # TODO: test
    if not is_reparateur(request.user):
        logger.warning('The user %s is no reparateur!', str(request.user))
        raise PermissionDenied('Not reparateur!')

    return render(
        request,
        "repapp/repa/main.html"
    )


class CafeView(LoginRequiredMixin, generic.ListView):
    """
    List of all Repair-Cafés.
    """
    # TODO: test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/cafe.html"

    def get_queryset(self):
        return Cafe.objects.all()


def cron(request):
    """
    View to trigger automated regular tasks.
    """
    return HttpResponse('done.')


def process_mails(request):
    """
    View to trigger processing of email in inbox.
    """
    count = mail_interface.process_mails()
    return HttpResponse(f'Done. Processed {count} messages.')


def one_time_login(request, secret: str):
    """
    View for one time login.
    """
    # waste a little time as brute force protection
    time.sleep(1)

    secret_hash = sha256(secret.encode('utf-8')).hexdigest()
    otl = get_object_or_404(OneTimeLogin, secret=secret_hash)

    if otl.login_used:
        messages.add_message(request, messages.ERROR,
                             'Der Einmal-Login wurde schon verwendet und ist nichtmehr gültig.')
        new_secret = create_one_time_login(otl.user, otl.url)
        send_one_time_login_mail(new_secret, otl.user.email, request)
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        otl.login_used = True
        otl.login_date = now()
        otl.save()

    user = authenticate(request, username=secret_hash, password=None)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.INFO, 'Login erfolgreich!')
        return HttpResponseRedirect(otl.url)
    else:
        messages.add_message(request, messages.ERROR, 'Login fehlgeschlagen.')
        return HttpResponseRedirect(reverse_lazy('index'))


def bootstrap(request):
    """
    Bootstrap design test page.
    """
    return render(
        request,
        "repapp/bootstrap.html"
    )


class CafeCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.CreateView):
    """
    Organisator view for creating a new Repair-Café.
    """
    # TODO: create test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/create_cafe.html"
    model = Cafe
    fields = ['event_date', 'location', 'address']
    success_url = reverse_lazy('cafe')

    def test_func(self):
        return is_organisator(self.request.user)


class CafeUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    """
    Organisator view for edit a Repair-Café.
    """
    # TODO: create test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/edit_cafe.html"
    model = Cafe
    fields = ['event_date', 'location', 'address']
    success_url = reverse_lazy('cafe')

    def test_func(self):
        logger.debug('User passes test: user: %s, result: %s.',
                     self.request.user, is_organisator(self.request.user))
        return is_organisator(self.request.user)


class CafeDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.DeleteView):
    """
    Organisator view for edit a Repair-Café.
    """
    # TODO: create test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/delete_cafe.html"
    model = Cafe
    success_url = reverse_lazy('cafe')

    def test_func(self):
        logger.debug('User passes test: user: %s, result: %s.',
                     self.request.user, is_organisator(self.request.user))
        return is_organisator(self.request.user)


class GuestView(LoginRequiredMixin, generic.ListView):
    """
    List of all Repair-Cafés.
    """
    # TODO: test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/guest.html"

    def get_queryset(self):
        return Guest.objects.all()


class GuestUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    """
    Organisator view for edit a guest.
    """
    # TODO: create test
    login_url = reverse_lazy('member')
    template_name = "repapp/orga/edit_guest.html"
    model = Guest
    success_url = reverse_lazy('guest')

    def test_func(self):
        return is_organisator(self.request.user)


def user_logout(request):
    """
    Log current user out.
    """
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


class MemberSettingsFormView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.FormView):
    """
    MemberSettingsFormView shows the member settings.
    """
    template_name = "repapp/member/member_settings.html"
    form_class = MemberSettings

    def form_valid(self, form):
        user = self.request.user
        if not is_member(user):
            raise PermissionDenied('Not a member!')
        user = get_object_or_404(CustomUser, email=user.email)
        user.notifications = form.cleaned_data['notifications']
        user.save()

        return HttpResponseRedirect(reverse_lazy('member_settings'))

    def get_initial(self):
        initial = super(MemberSettingsFormView, self).get_initial()
        initial['notifications'] = self.request.user.notifications
        return initial

    def get_context_data(self, **kwargs):
        context = super(MemberSettingsFormView, self).get_context_data(
            **kwargs
        )
        context["user"] = self.request.user
        return context

    def test_func(self):
        return is_member(self.request.user)
