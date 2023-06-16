from django.shortcuts import render
from .activate_email import activate_email
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import TelegramUser

from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from main.activate_email import account_activation_token
from api.db import check_email_in_db
from telegram_bot.management.commands.bot import send_full_info_to_user

# for activating account
def activate(request, uidb64, token):
    try:
        # get user from him id
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # making user active
        user.is_active = True
        user.save()
        try:
            tel_user = TelegramUser.objects.get(email=user.username)
        except TelegramUser.DoesNotExist:
            return HttpResponse('There no such user in data base!')
        response = check_email_in_db(user.username, user.is_active)
        if response:
            send_full_info_to_user(tel_user.telegram_id, f'Congitulations you succesfully confirmed your email!\nYour information:\n{response}')
            return HttpResponse('Succesfully confirmed')
        else:
            return HttpResponse('Something went wrong ;(')
    else:
        return HttpResponse('Activation link is invalid!')

# function for getting email and sending email
def activate_email_view(request):
    if request.POST: # if submit button is clicked
        if TelegramUser.objects.get(email=request.POST['email']):
            return HttpResponse("This account wasn't checked through Telegram Bot")
        user = User.objects.filter(username=request.POST['email']) # getting user from email
        if user.exists(): # cheking have user already activated account
            user = user[0]
            if not user.is_active:
                return HttpResponse('Email was sent, please check your email')
            try:
                tel_user = TelegramUser.objects.get(email=user.username)
            except TelegramUser.DoesNotExist:
                return HttpResponse('There no such user in data base!')
            response = check_email_in_db(user.username, user.is_active)
            if response:
                send_full_info_to_user(tel_user.telegram_id, f'You already been here!\nYour information:\n{response}')
                return HttpResponse('You already been here! I sent info to telegram bot')
            else:
                return HttpResponse('Something went wrong ;(')
        email = request.POST['email']
        user = User.objects.create(username=email) # save user email in db
        user.is_active = False # unactivate user (for default is_active = True)
        user.save()
        activate_email(request, user, email) # send email using above function
        return HttpResponse('Email was sent, please check your email')
    return render(request, 'home.html')
