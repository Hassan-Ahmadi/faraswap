from celery import shared_task


@shared_task
def send_otp_task(phone_number, otp):
    print(f"Sending OTP {otp} to {phone_number}")
