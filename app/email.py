import os
import html2text
import logging

from flask import render_template, render_template_string
from flask_mail import Message

from app import create_app
from app import mail

logger = logging.getLogger('werkzeug')


def send_email(recipient, subject, template, **kwargs):
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        msg = Message(
            app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
            sender=app.config['EMAIL_SENDER'],
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)


def send_custom_email(recipient, subject, custom_html, **kwargs):
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    h = html2text.HTML2Text()
    with app.app_context():
        msg = Message(
            app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
            sender=app.config['EMAIL_SENDER'],
            recipients=[recipient])
        msg.body = render_template_string(h.handle(custom_html))
        msg.html = render_template_string(custom_html)
        mail.send(msg)
