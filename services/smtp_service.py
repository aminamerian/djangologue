import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from django.conf import settings
from django.utils.encoding import force_bytes


class SmtpService:
    """
    Service class to send emails using SMTP.
    """

    REQUIRED_CONFIG_FIELDS = ["username", "password", "host", "port"]

    def __init__(
        self,
        from_email=settings.DEFAULT_FROM_EMAIL,
        reply_email=None,
        config=settings.DEFAULT_EMAIL_CONFIG,
    ):
        self.from_email = from_email
        self.reply_email = reply_email
        self.config = config

        self._validate_config()
        self._connect_smtp()

    def _validate_config(self):
        for field in SmtpService.REQUIRED_CONFIG_FIELDS:
            if field not in self.config:
                raise ValueError(f"Missing configuration field: {field}")

    def _connect_smtp(self):
        self.smtp = smtplib.SMTP(self.config["host"], self.config["port"])
        if self.config.get("tls", True):
            self.smtp.starttls()
        self.smtp.login(self.config["username"], self.config["password"])

    def send_email(
        self,
        subject,
        receivers,
        html_message,
        attachment=None,
        quit=True,
    ):

        message = self._create_message(
            subject=subject,
            receiver="",
            html_message=html_message,
            attachment=attachment,
        )
        for receiver in receivers:
            message.replace_header("To", receiver)
            self.smtp.send_message(
                message["From"],
                message["To"],
                message.as_string(),
            )

        if quit:
            self._quit_smtp()

    def _create_message(self, subject, receiver, html_message, attachment=None):
        """
        Create MIME message with specified subject, HTML content, and optional attachment
        """
        message = MIMEMultipart()
        message["Subject"] = Header(force_bytes(subject), "utf-8")
        message["From"] = self.from_email
        message["To"] = receiver

        body = MIMEText(html_message.encode("utf-8"), "html", "utf-8")
        message.attach(body)

        if attachment:
            self._attach_file(message, attachment)

        return message

    def _attach_file(self, message, attachment):
        with open(attachment["filepath"], "rb") as f:
            attachment_ = MIMEApplication(f.read(), _subtype="csv")
        attachment_.add_header(
            "Content-Disposition",
            "attachment",
            filename=attachment.get("filename"),
        )
        message.attach(attachment_)

    def _quit_smtp(self):
        self.smtp.quit()
