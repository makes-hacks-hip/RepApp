import os
import logging
from pathlib import Path
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from .forms import MessageForm
from .utils import create_message, send_message, process_mails
from .models import Message, Attachment


logger = logging.getLogger(__name__)


def process(request):  # pragma: no cover
    # no logic contained, no test needed
    count = process_mails()
    return HttpResponse(f'{count} new messages were processed.')


@login_required
def mail_thread(request, id):
    message = get_object_or_404(Message, pk=id)

    form = MessageForm()

    form['receiver'].field.widget.attrs['disabled'] = 'disabled'
    form.initial['receiver'] = message.sender

    form['summary'].field.widget.attrs['disabled'] = 'disabled'
    summary = f'Re: {message.summary}'
    form.initial['summary'] = summary

    if request.method == 'POST':
        # Form was submitted
        form = MessageForm(request.POST.copy())
        form.data['receiver'] = message.sender.pk
        form.data['summary'] = summary

        logger.debug('mail_thread: sending mail %r', form)

        if form.is_valid():
            logger.debug('mail_thread: mail is valid. %r', form)
            m = form.save(commit=False)
            m.sender = request.user
            m.reply_to = message
            m.save()

            message.answered = True
            message.save()

            success = send_message(m, request)

            if success:
                messages.info(request, _('Mail was sent.'))
                return HttpResponseRedirect(reverse_lazy('email_interface:mail_thread', kwargs={'id': m.pk}))
            else:  # pragma: no cover
                # should never happen
                messages.error(request, _('Sending of mail failed!'))
        else:  # pragma: no cover
            # only debug log
            logger.debug('mail_thread: mail is not valid! %r', form.errors)

    return render(
        request,
        "email_interface/testing/mail_thread.html",
        {
            'form': form,
            'mails': message.thread(),
            'mail': message,
            'answers': message.answers(),
            'siblings': message.siblings(),
        }
    )


@login_required
def send_test_mail(request):  # pragma: no cover
    """
    Debug view to send a test mail.
    """
    # debug view
    # get first user
    user = get_user_model().objects.get(pk=1)
    current_folder = Path(__file__).resolve().parent
    file = os.path.join(current_folder, 'test_data', 'Nut.jpg')
    res = create_message(
        request,
        request.user,
        user,
        'A test mail',
        '<html><body><h1>Test!</h1></body></html>',
        'Test!',
        attachments=[file]
    )

    if res:
        return HttpResponse('Mail was sent successful!')
    else:
        return HttpResponse('Sending of mail failed!')


class SendMailView(LoginRequiredMixin, generic.FormView):  # pragma: no cover
    # debug view
    form_class = MessageForm
    template_name = "email_interface/testing/write_mail.html"
    success_url = reverse_lazy("email_interface:send_mail")

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user
        message.save()

        success = send_message(message, self.request)

        if success:
            messages.info(self.request, _('Mail was sent.'))
        else:
            messages.error(self.request, _('Sending of mail failed!'))

        return super().form_valid(form)


@login_required
def my_sent_mails(request):
    return render(
        request,
        "email_interface/testing/my_mails.html",
        {
            'mails': Message.from_user(request.user),
        }
    )


@login_required
def my_received_mails(request):
    return render(
        request,
        "email_interface/testing/my_mails.html",
        {
            'mails': Message.to_user(request.user),
        }
    )


@login_required
def my_attachments(request):
    return render(
        request,
        "email_interface/testing/my_attachments.html",
        {
            'attachments': Attachment.of_user(request.user),
        }
    )
