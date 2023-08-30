import logging
from bs4 import BeautifulSoup
from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Message


logger = logging.getLogger(__name__)


class MessageForm(forms.ModelForm):
    """
    A form for creating new messages.
    """
    mail_text = forms.CharField(
        label=_("Text content"), required=False, widget=forms.Textarea)
    use_mail_text = forms.BooleanField(
        label=_('Use text content?'), required=False)

    class Meta:
        model = Message
        fields = ['receiver', 'summary', 'html_content']
        widgets = {'html_content': CKEditorUploadingWidget()}

    def clean(self):
        if self.cleaned_data['use_mail_text'] and self.cleaned_data['mail_text'] == '':
            raise forms.ValidationError(
                _("Mail text cannot be empty if it is used!"))

        return super().clean()

    def save(self, commit: bool = True):
        message = super().save(commit=False)

        if not self.cleaned_data['use_mail_text']:
            message.text_content = self.cleaned_data['mail_text']
        else:
            # convert HTML content to text content
            soup = BeautifulSoup(
                self.cleaned_data['html_content'], features='html.parser')
            message.text_content = soup.get_text('\n')

        if commit:
            message.save()

        return message
