from django.shortcuts import render
from .activate_email import activate_email
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import CheckedEmailUser, CheckedHWIDUser

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from main.activate_email import account_activation_token
from api.db import check_HWID_in_db, check_email_in_db
from telegram_bot.management.commands.bot import send_full_info_to_user


def check_full_data(request, telegram_id):
    if request.method == 'GET':
        return render(request, 'full_data_check.html')
    elif request.method == 'POST':
        if "check_email" in request.POST:
            return render(request, 'full_data_check.html', {'page': 'email'})
        elif "check_HWID" in request.POST:
            return render(request, 'full_data_check.html', {'page': 'HWID'})
        elif "email" in request.POST:
            response = check_email_in_db(request.POST['email'], False)
            user = CheckedEmailUser.objects.create(email=request.POST['email'], telegram_id=telegram_id)
            if response: # if is something in response
                user.found = True
                user.save()
                send_full_info_to_user(telegram_id, response)
                return HttpResponse('Email was found in the database. I sent info to your telegram')
            else:
                return HttpResponse("Email not found in the database.")
        elif "HWID" in request.POST:
            response = check_HWID_in_db(request.POST['HWID'])
            PC = CheckedHWIDUser.objects.create(HWID=request.POST['HWID'], telegram_id=telegram_id)
            if response: # if is something in response
                PC.found = True
                PC.save()
                send_full_info_to_user(telegram_id, response)
                return HttpResponse('HWID was found in the database. I sent info to your telegram')
            else:
                return HttpResponse("HWID not found in the database.")

# for activating account
def activate(request, uidb64, token):
    try:
        # get user from him id
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CheckedEmailUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CheckedEmailUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # making user active
        user.verified = True
        user.save()
        send_full_info_to_user(user.telegram_id, f'Congitulations you succesfully confirmed your email!')
        return HttpResponse('Succesfully confirmed')
    else:
        return HttpResponse('Activation link is invalid!')

# # function for getting email and sending email
# def activate_email_view(request):
#     if request.POST: # if submit button is clicked
#         if not CheckedEmailUser.objects.filter(email=request.POST['email']).exists():
#             return HttpResponse("This account wasn't checked through Telegram Bot")
#         user = User.objects.filter(username=request.POST['email']) # getting user from email
#         if user.exists(): # cheking have user already activated account
#             user = user[0]
#             if not user.is_active:
#                 return HttpResponse('Email was sent, please check your email')
#             try:
#                 tel_user = CheckedEmailUser.objects.get(email=user.username)
#             except CheckedEmailUser.DoesNotExist:
#                 return HttpResponse('There no such user in data base!')
#             response = check_email_in_db(user.username, user.is_active)
#             if response:
#                 send_full_info_to_user(tel_user.telegram_id, f'You already been here!\nYour information:\n{response}')
#                 return HttpResponse('You already been here! I sent info to telegram bot')
#             else:
#                 return HttpResponse('Something went wrong ;(')
#         email = request.POST['email']
#         user = User.objects.create(username=email) # save user email in db
#         user.is_active = False # unactivate user (for default is_active = True)
#         user.save()
#         activate_email(request, user, email) # send email using above function
#         return HttpResponse('Email was sent, please check your email')
#     return render(request, 'home.html')
