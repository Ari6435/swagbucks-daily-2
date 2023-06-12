import httpx,json,requests,time,re
import urllib.parse
from bs4 import BeautifulSoup
from dhooks import Webhook,Embed
import pymongo
import concurrent.futures

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb+srv://discord_outh2:discord_outh2@cluster0.qk9txqp.mongodb.net/?retryWrites=true&w=majority")
db = client["sb_daily"]
q_a = db["question_answer"]



data ={}
hook_url = "https://discord.com/api/webhooks/1117823682052624444/etY5xJgAc3SpLPSGcqDTyfAq_Uv0Piwu3YijbzeMHI2VcBrFC6_MTpXqW8Ej59JJcrGV"
main_api_endpoint = 'https://api.playswagiq.com/dailygame'
hook2 = Webhook(hook_url)
T1 = []


#-------------------enterin the game------------------------#
def enter_game(bearer,uid):#(bearer,uid)
    headers = {
    'Host': 'api.playswagiq.com',
    'user-agent': 'SwagIQ-Android/37 (okhttp/3.14.9)',
    'authorization': f'Bearer {bearer}',
    # 'content-length': '0',
    # 'accept-encoding': 'gzip',
    }

    ent_gm = httpx.post(f'{main_api_endpoint}/enter?_uid={uid}', headers=headers).json()
    if ent_gm["success"] is True:

        data["entryid"] = ent_gm["entryIdSigned"]
        answers = ent_gm["firstQuestion"]["answers"]   
        data["id1"] = answers[0]["id"]
        data["id2"] = answers[1]["id"]
        data["id3"] = answers[2]["id"]
        data["question_text"] = ent_gm["firstQuestion"]["text"]
        data["answer1"] = answers[0]["text"]
        data["answer2"] = answers[1]["text"]
        data["answer3"] = answers[2]["text"]
        data["anid1"] = answers[0]["idSigned"]
        data["anid2"] = answers[1]["idSigned"]
        data["anid3"] = answers[2]["idSigned"]  
        return ent_gm["success"]

    else:
        return ent_gm




#-------------load all accounts
def load_threads():
    C = 0
    file = open("config.json","r")
    file = json.loads(file.read())
    for i in file:
        T1.append(i)
        C += 1
    for i in T1:
        print(i["username"])
    return (f"**__{C} Accounts Connected.__**")




#--------------------------------send and get answers----------------#
def send_get(bearer,uid,aid):
    # print(aid)
    entryid = data["entryid"]

    headers = {
    "Host": "api.playswagiq.com",
    "user-agent": "SwagIQ-Android/37 (okhttp/3.14.9)",
    "authorization": f"Bearer {bearer}",
    "content-type": "application/x-www-form-urlencoded",
    "content-length": "134",
    "accept-encoding": "gzip"
    }

    data_ = {
    'entryid': entryid,
    'aid': aid,
    }
    
    url = f'{main_api_endpoint}/answer?_uid={uid}'
    response = requests.post(url, headers=headers, data=urllib.parse.urlencode(data_)).json()
    
    print("Question : ",data["question_text"])
    # print("Question num: ",question_num)                
    print("Answer 1:", data["answer1"])
    print("Answer 2:", data["answer2"])
    print("Answer 3:", data["answer3"])       
    print(f"correct status : {response['correct']}")
    check = q_a.find_one({"question": data["question_text"]})
    if check is None:
        if int(response["correctAnswerId"]) == int(data["id1"]):
            print(data["answer1"])
            q_a.insert_one({"question": data["question_text"],"answer": data["answer1"]})

        if int(response["correctAnswerId"]) == int(data["id2"]):
            print(data["answer2"])
            q_a.insert_one({"question": data["question_text"],"answer": data["answer2"]})

        if int(response["correctAnswerId"]) == int(data["id3"]):
            print(data["answer3"])       
            q_a.insert_one({"question": data["question_text"],"answer": data["answer3"]})


    try:

     
        answers = response["nextQuestion"]["answers"]
        data["question_text"] = response["nextQuestion"]["text"]
        data["answer1"] = answers[0]["text"]
        data["answer2"] = answers[1]["text"]
        data["answer3"] = answers[2]["text"]
        data["anid1"] = answers[0]["idSigned"]
        data["anid2"] = answers[1]["idSigned"]
        data["anid3"] = answers[2]["idSigned"]
        data["id1"] = answers[0]["id"]
        data["id2"] = answers[1]["id"]
        data["id3"] = answers[2]["id"]  

    except:
        print(response['summary'])
        cldd = response['summary']
        hook2.send(f'**{cldd}**')
        claim(bearer,uid)



#-------------------claim----------------------#
def claim(bearer,uid):
    entryid = data["entryid"]
    headers = {
        'Host': 'api.playswagiq.com',
        'user-agent': 'SwagIQ-Android/37 (okhttp/3.14.9)',
        'authorization': f'Bearer {bearer}',
        'content-type': 'application/x-www-form-urlencoded',
        'accept-encoding': 'gzip'
    }
    data_ = {
    'entryid': entryid,
    }

    url = f'{main_api_endpoint}/claim?_uid={uid}'
    response = httpx.post(url, headers=headers, data=urllib.parse.urlencode(data_)).json()
    print(response)    


#------------------answer check---------------------------#
def check_answer():
    check2 = q_a.find_one({"question": data["question_text"]})
    if check2 is None:
        ans_ = get_highest_rating_index(question=data["question_text"].lower(),options=[data["answer1"].lower(),data["answer2"].lower(),data["answer3"].lower()])
        return ans_
    else:
        print(f"answer found : {check2['answer']}")
        if check2['answer'].lower() == data["answer1"].lower():
            ans_ = 1
        elif check2['answer'].lower() == data["answer2"].lower():
            ans_ = 2
        else:
            ans_ = 3
        return ans_


#---------------google answer----------------------#
# def count_occurrence(text, option):
#     import re
#     words = option.split()
#     count = 0
#     for word in words:
#         if word not in ["of", "in", "the", "these", "was","a", "an","not","never","except"]:
#             pattern = re.compile(r"\b" + word + r"\b")
#             count += len(pattern.findall(text))
#     return count

# def get_highest_rating_index(question, options):
#     import re,requests
#     from bs4 import BeautifulSoup
#     url = f'https://www.google.com/search?q={question}'.replace("not","").replace("never","")
#     r = requests.get(url)
#     doc = BeautifulSoup(r.content, "html.parser")
#     all_text =doc.get_text().strip()
#     text = all_text.lower()

#     total_count = 0
#     for option in options:
#         count = count_occurrence(text, option)
#         total_count += count
#     highest_rating = ""
#     for option in options:
#         count = count_occurrence(text, option)
#         if highest_rating == "" or count > count_occurrence(text, highest_rating):
#             highest_rating = option

#     return options.index(highest_rating) + 1


#-------------google Threading-------------
def count_occurrence(text, option):
    words = option.split()
    count = 0
    for word in words:
        if word not in ["of", "in", "the", "these", "was","a", "an","not","never","except"]:
            pattern = re.compile(r"\b" + word + r"\b")
            count += len(pattern.findall(text))
    return count

def get_highest_rating_index(question, options):
    url = f'https://www.google.com/search?q={question}'.replace("not","").replace("never","")
    r = requests.get(url)
    doc = BeautifulSoup(r.content, "html.parser")
    all_text = doc.get_text().strip()
    text = all_text.lower()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        counts = list(executor.map(count_occurrence, [text]*len(options), options))


    if "not" in question.lower():
        highest_rating = options[counts.index(min(counts))]
        return options.index(highest_rating) + 1

    highest_rating = options[counts.index(max(counts))]
    return options.index(highest_rating) + 1
