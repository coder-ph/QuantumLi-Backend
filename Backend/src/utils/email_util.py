import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.config import Config
from src.utils.logger import logger
from src.error.apiErrors import InternalServerError
from time import sleep
import os

MAX_RETRIES = 3
RETRY_DELAY = 5 

def send_password_reset_email(to_email: str, reset_token: str) -> None:
    subject = "Password Reset Request"
    reset_link = f"http://localhost:5000/reset-password?token={reset_token}"
    body = f"""
    <h1>Password Reset Request</h1>
    <p>We received a request to reset your password.</p>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    <p>If you did not request a password reset, please ignore this email.</p>
    """
    send_email(subject, body, to_email, is_html=True)

def send_email(subject: str, body: str, to_email: str, is_html: bool = False) -> None:
    retries = 0
    while retries < MAX_RETRIES:
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_SENDER
            msg['To'] = to_email
            msg['Subject'] = subject

            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=10) as server:
                server.starttls() 
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(Config.EMAIL_SENDER, to_email, text)

            logger.info(f"Verification email sent to {to_email}")
            return  

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error while sending email to {to_email}: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                logger.info(f"Retrying... Attempt {retries}/{MAX_RETRIES}")
                sleep(RETRY_DELAY)  
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise InternalServerError("Error sending verification email.")

   
    logger.error(f"Failed to send email to {to_email} after {MAX_RETRIES} attempts.")
    raise InternalServerError("Failed to send verification email after multiple attempts.")

def send_email(subject, body, to_email, is_html=False):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_SENDER
            msg['To'] = to_email
            msg['Subject'] = subject

           
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=10) as server:
                server.starttls() 
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(Config.EMAIL_SENDER, to_email, text)

            logger.info(f"Verification email sent to {to_email}")
            return  

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error while sending email to {to_email}: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                logger.info(f"Retrying... Attempt {retries}/{MAX_RETRIES}")
                sleep(RETRY_DELAY)  # Wait before retrying
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise InternalServerError("Error sending verification email.")

  
    logger.error(f"Failed to send email to {to_email} after {MAX_RETRIES} attempts.")
    raise InternalServerError("Failed to send verification email after multiple attempts.")