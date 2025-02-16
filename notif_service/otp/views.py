from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from random import randint
from notif_service.settings import OTP_TIMEOUT_SECONDS

from .tasks import send_otp_task


class SendOTPView(APIView):
    # TODO: change to IsJWTAuthenticated
    permission_classes = [permissions.IsAuthenticated]

    # @swagger_auto_schema(responses={200: "OTP is being sent"})
    def post(self, request):
        otp = randint(10000, 99999)
        
        # TODO: what if the user has multiple phone numbers?
        # TODO: what if the phone number does not exist?
        # TODO: how to fetch the user id when using a custom IsJWTAuthenticated permission?

        user_id = request.user.user_id
        print(f"request.user: {request.user}")
        # print(user_id)
        phone_number = cache.get(f"phone_number:{user_id}")
        otp_key = f"otp:{phone_number}"

        send_otp_task.delay(phone_number, otp)
        cache.set(otp_key, otp, timeout=OTP_TIMEOUT_SECONDS)

        return Response({"message": "OTP is being sent"}, status=status.HTTP_200_OK)
