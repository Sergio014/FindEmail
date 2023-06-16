from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

#generate token for actication
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active)
        )

# initialize class
account_activation_token = AccountActivationTokenGenerator()

def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    # create message for user, template is in /templates
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    # send email activation
    EmailMessage(mail_subject, message, to=[to_email]).send()