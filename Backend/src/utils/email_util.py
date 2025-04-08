import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.config import Config
from src.utils.logger import logger
from src.error.apiErrors import InternalServerError
from time import sleep
import os

# Set retry parameters
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def send_email(subject, body, to_email, is_html=False):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_SENDER
            msg['To'] = to_email
            msg['Subject'] = subject

            # Attach the body (plain or HTML)
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Send the message via our SMTP server
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT, timeout=10) as server:
                server.starttls()  # Secure the connection
                server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
                text = msg.as_string()
                server.sendmail(Config.EMAIL_SENDER, to_email, text)

            logger.info(f"Verification email sent to {to_email}")
            return  # Exit the function once email is sent successfully

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error while sending email to {to_email}: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                logger.info(f"Retrying... Attempt {retries}/{MAX_RETRIES}")
                sleep(RETRY_DELAY)  # Wait before retrying
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise InternalServerError("Error sending verification email.")

    # If the loop exits, all retries failed
    logger.error(f"Failed to send email to {to_email} after {MAX_RETRIES} attempts.")
    raise InternalServerError("Failed to send verification email after multiple attempts.")

