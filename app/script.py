from apscheduler.schedulers.background import BackgroundScheduler
from base_engine import session
from base import User

budzik = BackgroundScheduler()
def send(email):


# do implementacji...


def summary():
    baza =session()
    try:
        maile = baza.query(User).all()
        for i in maile:
            send(User.email)
    finally:
        baza.close()





budzik.add_job(summary, 'cron', hour=0, minute=0)

