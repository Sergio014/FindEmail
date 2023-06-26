from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
# Import your necessary models and functions
from main.models import *
from .bot import send_full_info_to_user

def monitoring_job(group=None, hwid_or_email=None):
    send_full_info_to_user(917369738, "Monitoring was started")
    if not group:
        dict_to_send_email = {user: RandomData.objects.filter(username=user.email, sent=False)[0] for user in CheckedEmailUser.objects.all() if RandomData.objects.filter(username=user.email, sent=False).exists() and user.receive_email_notifications}
    elif group.email_notifications:
        dict_to_send_email = {user: RandomData.objects.filter(username=user.email, sent=False)[0] for user in group.email_users.all() if RandomData.objects.filter(username=user.email, sent=False).exists() and user.receive_email_notifications}
    if hwid_or_email == None or hwid_or_email == 'email':
        for user, info in dict_to_send_email.items():
            if user.need_to_verify and not user.verified:
                send_full_info_to_user(user.telegram_id, f"I have something found for you while monitoring. Please verify you email {info.username} to get the notifications.")
                continue
            text = f"Email: {info.username}\nPassword: {info.password}\nUrl: {info.url}\nExposed at: {info.exposed_at}"
            info.sent = True
            info.save()
            send_full_info_to_user(user.telegram_id, text)
    if not group:
        dict_to_send_hwid = {user.telegram_id: PCinfo.objects.filter(HWID=user.HWID, sent=False)[0] for user in CheckedHWIDUser.objects.all() if PCinfo.objects.filter(HWID=user.HWID, sent=False).exists() and user.receive_hwid_notifications}
    elif group.PC_notifications:
        dict_to_send_hwid = {user.telegram_id: PCinfo.objects.filter(HWID=user.HWID, sent=False)[0] for user in group.hwid_users.all() if PCinfo.objects.filter(HWID=user.HWID, sent=False).exists() and user.receive_hwid_notifications}
    if hwid_or_email == None or hwid_or_email == 'hwid':
        for telegram_id, info in dict_to_send_hwid.items():
            text = f"HWID: {info.HWID}\nIP: {info.ip}\nPath to virus: {info.path_to_virus}\nUsername: {info.username}\nOperating system: {info.operating_system}\nDate: {info.date_log}"
            info.sent = True
            info.save()
            send_full_info_to_user(telegram_id, text)
    

# Create an instance of the scheduler
scheduler = BlockingScheduler()

# Schedule the job to run every minute
scheduler.add_job(monitoring_job, 'interval', hours=5)

# Start the scheduler
class Command(BaseCommand):
    help = 'Checks for new user emails every 10 minutes'

    def handle(self, *args, **options):
        scheduler.start()
