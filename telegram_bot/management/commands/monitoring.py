from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
# Import your necessary models and functions
from main.models import *
from .bot import send_full_info_to_user

def monitoring_job():
    send_full_info_to_user(917369738, "Monitoring was started")
    dict_to_send_email = {user.telegram_id: RandomData.objects.filter(username=user.email, sent=False)[0] for user in CheckedEmailUser.objects.all() if RandomData.objects.filter(username=user.email, sent=False).exists()}

    for telegram_id, info in dict_to_send_email.items():
        text = f"Email: {info.username}\nPassword: {info.password}\nUrl: {info.url}\nExposed at: {info.exposed_at}"
        info.sent = True
        info.save()
        send_full_info_to_user(telegram_id, text)

    dict_to_send_hwid = {user.telegram_id: PCinfo.objects.filter(HWID=user.HWID, sent=False)[0] for user in CheckedHWIDUser.objects.all() if PCinfo.objects.filter(HWID=user.HWID, sent=False).exists()}

    for telegram_id, info in dict_to_send_hwid.items():
        text = f"HWID: {info.HWID}\nIP: {info.ip}\nPath to virus: {info.path_to_virus}\nUsername: {info.username}\nOperating system: {info.operating_system}\nDate: {info.date_log}"
        info.sent = True
        info.save()
        send_full_info_to_user(telegram_id, text)
    

# Create an instance of the scheduler
scheduler = BlockingScheduler()

# Schedule the job to run every minute
scheduler.add_job(monitoring_job, 'interval', minutes=1)

# Start the scheduler
class Command(BaseCommand):
    help = 'Checks for new user emails every 10 minutes'

    def handle(self, *args, **options):
        scheduler.start()
