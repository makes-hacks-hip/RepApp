import logging
from django.conf import settings
from django.apps import AppConfig


logger = logging.getLogger(__name__)


def message_answered_receiver(sender, instance, **kwargs):
    logger.debug('Message answered signal received: %s %s',
                 instance, kwargs['answer'])


def new_message_receiver(sender, instance, **kwargs):
    logger.debug('New message signal received: %s', instance)


class EmailInterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_interface'

    def ready(self):
        if settings.DEBUG:
            logger.debug('Register dummy signal receivers')
            from .signals import new_message, message_answered
            message_answered.connect(message_answered_receiver)
            new_message.connect(new_message_receiver)
