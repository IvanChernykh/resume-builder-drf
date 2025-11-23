from django.core.mail import send_mail

from config.celery import app


@app.task(bind=True, max_retries=5, default_retry_delay=30, queue="emails")
def send_verification_email(self, user_username: str, user_email: str, verify_url: str):
    message = f"""
    Hello, {user_username}!
    Please confirm your email address by clicking the link below:
    {verify_url}
    """

    try:
        send_mail(
            subject="Email confirmation",
            message=message,
            recipient_list=[user_email],
            from_email="noreply@resumebuilder.com",
        )
    except Exception as exc:
        print(f"Failed to send verification email: {exc}")
        raise self.retry(exc=exc)


@app.task(bind=True, max_retries=5, default_retry_delay=30, queue="emails")
def send_password_reset_email(self, user_email: str, reset_url: str):
    try:
        send_mail(
            subject="Password reset",
            message=f"Reset your password:\n{reset_url}",
            recipient_list=[user_email],
            from_email="noreply@resumebuilder.com",
        )
    except Exception as exc:
        print(f"Failed to send password reset email: {exc}")
        raise self.retry(exc=exc)
