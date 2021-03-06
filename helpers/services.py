from django.conf import settings
import logging
import re
import requests
from requests.auth import AuthBase
import base64
import hashlib
import json
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)
EMAIL_BLACKLIST = ['']
EMAIL_PATTERN = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
PASSWORD_PATTERN = "\A(?=[a-z,A-Z,0-9,\s]*[^a-z,A-Z,0-9,\s])(?=\D*\d).{8,100}"

def send_Email(email, message,**kwargs):
    email_pattern = EMAIL_PATTERN
    if email:
        email = email if re.match(email_pattern,email) else None
    else:
        email = None
    subject = kwargs['subject']
    print('email worked')
    message = message
    token = 'nnnnnn'
    emailFrom = kwargs['email_from']
    try:
        if email == None:
            logger.info('bad email')
            raise Badinfo
        elif email in EMAIL_BLACKLIST:
            logger.info('sorry your email: {} has been blacklisted'.format(email))
        else: 
            print('we are here')
            messagee = Mail(
                from_email=emailFrom,
                to_emails=email,
                subject=subject,
                html_content=message)
            logger.info(settings.EMAIL_HOST_PASSWORD)
            sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
            response = sg.send(messagee)
            logger.info(response.status_code)
            logger.info(' email was successful ')
            return True
    except Exception as e:
        logger.info(' there was an error sending sms, info : {} '.format(e))