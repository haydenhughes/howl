import os
import pyotp


class Config:
    # Set the log level.
    # Possible values are DEBUG, INFO, WARNING, ERROR or CRITICAL
    #
    # Default: INFO
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Username for authentication.
    # Set using the USERNAME environment variable.
    #
    # Must be set for the application to work.
    USERNAME = os.environ['USERNAME']

    # A base32 encoded string used to generate the totp password.
    #
    # Default: Something random.
    TOTP_SECRET = os.getenv('TOTP_SECRET', pyotp.random_base32())

    # The amount of time in seconds to wait between checking
    # if any alerts should be sounded.
    #
    # Default: 21600
    CHECK_INTERVAL = int(os.getenv('LOG_LEVEL', '21600'))

    # The url to a SMTP server to use for sending emails.
    #
    # Default: None
    SMTP_HOST = os.getenv('SMTP_HOST')

    # The port of the SMTP server used to send emails.
    #
    # Default: None
    SMTP_PORT = os.getenv('SMTP_PORT')

    # The username of the SMTP server.
    #
    # Default: None
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')

    # The password of the SMTP server.
    #
    # Defualt: None
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
