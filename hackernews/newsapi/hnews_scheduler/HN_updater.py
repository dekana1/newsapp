from apscheduler.schedulers.background import BackgroundScheduler
from newsapi.views import newsViewset

def run_update():
    scheduler = BackgroundScheduler()
    hnews = newsViewset()
    scheduler.add_job(hnews.save_hnews, "interval", minutes=5, id="HNEWS001", replace_existing=True)
    
    scheduler.start()