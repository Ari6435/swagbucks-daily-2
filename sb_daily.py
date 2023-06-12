import httpx,json,requests,time,re
import urllib.parse
from bs4 import BeautifulSoup
from dhooks import Webhook,Embed
import pymongo
import concurrent.futures

# from mod import get_highest_rating_index,count_occurrence
from methods import *
import traceback
hook = Webhook(hook_url)
# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb+srv://discord_outh2:discord_outh2@cluster0.qk9txqp.mongodb.net/?retryWrites=true&w=majority")
db = client["sb_daily"]
q_a = db["question_answer"]
            
hook.send(load_threads())
for i in T1:
    try:
        eg = enter_game(i["bearer"],i["uid"])
        if eg is True:
            for _ in range(10):
                time.sleep(4)
                ans = check_answer()                    
                if ans == 1:
                    aid = data["anid1"]          
                    send_get(i["bearer"],i["uid"],aid)
                    
                elif ans == 2:
                    aid = data["anid2"]
                    send_get(i["bearer"],i["uid"],aid)          
                else:
                    aid = data["anid3"]
                    send_get(i["bearer"],i["uid"],aid)                              
                    time.sleep(1)
                print(f"ans --> {ans}")
        
        else:
            print(f"{eg} {i['username']}")
            hook.send(f"{eg} {i['username']}")
        
    except Exception as e:
        print(f"error : {i['username']}",e)   
        tb = traceback.format_exc()
        hook.send(f"Error`python\n{tb}`")                    
         
