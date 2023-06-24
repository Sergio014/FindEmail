import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse
from main.models import CheckedEmailUser, CheckedHWIDUser

from . import models as api_models
from .db import check_email_in_db
from django.http import HttpResponse
from api.db import check_HWID_in_db, check_email_in_db
from telegram_bot.management.commands.bot import send_full_info_to_user


@api_view(['POST'])
def check_full_data(request):
    print(request.POST)
    print(json.loads(request.POST))
    telegram_id = request.POST['telegram_id']
    data = request.POST
    if data['data'] == "email":
        response = check_email_in_db(data['email'], False)
        user = CheckedEmailUser.objects.create(email=data['email'], telegram_id=telegram_id)
        if response: # if is something in response
            user.found = True
            user.save()
            send_full_info_to_user(telegram_id, response)
            return Response({"success": True}, 200)
        else:
            return Response({"error": "Email not found in the database."}, 404)
    elif data['data'] == "hwid" :
        response = check_HWID_in_db(data['hwid'])
        PC = CheckedHWIDUser.objects.create(HWID=data['hwid'], telegram_id=telegram_id)
        if response: # if is something in response
            PC.found = True
            PC.save()
            send_full_info_to_user(telegram_id, response)
            return Response({"success": True}, 200)
        else:
            return HttpResponse({"error": "HWID not found in the database."}, 404)

@api_view(['GET'])
def check_bot_view(request):
    try:
        return Response({'is_active': api_models.Bot.objects.last().is_active}, status=200)
    except Exception as e:
        print(e)
        return Response({'is_active': False}, status=400)