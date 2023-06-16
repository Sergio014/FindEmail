from rest_framework.decorators import api_view
from rest_framework.response import Response

from main import models
from .db import check_email_in_db
# Create your views here.

# only for get requests
@api_view(['GET'])
def check_email(request, email, telegram_id):
    # check is person in db(from telegram bot) is_verified=False
    response = check_email_in_db(email, False)
    if response: # if is something in response
        models.TelegramUser.objects.create(email=email, telegram_id=telegram_id)
        return Response({'success': response}, status=200)
    else:
        return Response({'error': "Email not found in the database."}, status=400)



