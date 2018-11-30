import smtplib
import yaml
from config import Config  # A bit of a hack but removes circular imports.
from email.message import EmailMessage


class Email(yaml.YAMLObject):
    """A interface to create and send emails.

    Attributes:
        recipient: A string of the email address to send the email to.
                    Use commas to seperate multiple email addresses.
        sender: A string of the email address to send the email from.
        subject: A string of the subject of the email.
        body: A string of the body of the email.
        timeout: A integer of the amount of hours to wait after the last
                 check in before the alert is triggered.
    """
    yaml_tag = u'!Email'

    def __init__(self, recipient, sender, subject, body, timeout):
        self.recipient = recipient
        self.sender = sender
        self.subject = subject
        self.body = body
        self.timeout = timeout

    def send(self,
             host=Config.SMTP_HOST,
             username=Config.SMTP_USERNAME,
             password=Config.SMTP_PASSWORD,
             port=Config.SMTP_PORT):
        """Send the email!

        You'll note that all the args have a default to their repective
        config. This is so that send() can be called without needing any args
        to be directly passed to it so that howl can be as modular as possible
        to allow adding various services.

        Args:
            host: A string of the url to a SMTP server.
            username: A string of the username to login to the SMTP server.
            password: A string of the password to login to the SMTP server.
            port: An integer of the port of the SMTP server.
        """
        msg = EmailMessage()

        msg['To'] = self.recipient
        msg['From'] = self.sender
        msg['Subject'] = self.subject
        msg.set_content(self.message)
        msg.set_content(self.body)

        with smtplib.SMTP(host=host,
                          port=port) as s:
            s.login(username, password)
            s.send_message(msg)
