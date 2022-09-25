from apscheduler.schedulers.background import BackgroundScheduler
from newsapi.views import newsViewset
from newsapi.models import NewHNStories, HNew

def run_update():
    scheduler = BackgroundScheduler() 
    hnews = newsViewset()    
    scheduler.add_job(hnews.save_hnews, "interval", minutes=5, id="HNEWS001", replace_existing=True)
    
    # HNEWS DATA SCHEDULE
    
    hnews_list = [x['hn_id'] for x in NewHNStories.objects.all().values()]
    
    # print(hnews_list)
    
    for x in range(5):
        
        print("from scheduler.py", x)
        
        if HNew.objects.filter(pk_id=hnews_list[x]).exists():
            
            pass
        
        
        else: 
            
            scheduler.add_job(lambda: hnews.save_hnews_dets(hnews_list[x]), "interval", minutes=5, id="HNEWS002", replace_existing=True)

    scheduler.start()
    
    
# def get_hnews_data():
    
#     scheduler = BackgroundScheduler() 
#     hnews = newsViewset()    
    
    
#             scheduler.start()
    
    
    