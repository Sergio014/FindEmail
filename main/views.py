from django.shortcuts import render, redirect
from .activate_email import activate_email
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from main.activate_email import account_activation_token
from api.db import check_email_in_db

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

        return HttpResponse('Succesfully confirmed')
    else:
        return HttpResponse('Activation link is invalid!')

# function for getting email and sending email
def activate_email_view(request):
    if request.POST: # if submit button is clicked
        user = User.objects.filter(username=request.POST['email']) # getting user from email
        if user.exists() and user[0].is_active: # cheking have user already activated account
            return redirect(f'wait/{request.POST["email"]}')
        email = request.POST['email']
        user = User.objects.create(username=email) # save user email in db
        user.is_active = False # unactivate user (for default is_active = True)
        user.save()
        activate_email(request, user, email) # send email using above function
        return redirect(f'wait/{email}')
    return render(request, 'home.html')

# waiting view
def waiting(request, email):
    # get user from db
    user = User.objects.get(username=email)

    if not user.is_active: # if user have bot activate account already
        return HttpResponse('Email was sent, please check your email')

    response = check_email_in_db(email, user.is_active) # get full info from db is_verified = True

    if response:
        return HttpResponse(f'Congitulations you succesfully confirmed your email!\nYour information:\n{response}')

    return HttpResponse('Sorry something went wrong ;(')