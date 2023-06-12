import httpx,json,dhooks

datas = []
acc = [
    "rahul40bansa@gmail.com:y5y3gegnxh:45348442114d31e342676968b2a9df3b",
    "13rahulbansa@gmail.com:y5y3gegnxh:5ff329ca05d1cf94d44c552f74973e63",
    "2swagemu@gmail.com:y5y3gegnxh:26eaf6d51bbec70f371452ec1182d065",
    "1swagemu@gmail.com:y5y3gegnxh:47f3c49e102f4998f2ef806816687cf2",
    "3swagemu@gmail.com:y5y3gegnxh:320a79fa8af661d44cf26fef77d37b9b",   
    "4swagemu@gmail.com:y5y3gegnxh:12fcec5bb709f95e5b979d82432928a8",
    "5swagemu@gmail.com:y5y3gegnxh:043f08653b148df40e32f793042d100d",
    "6swagemu@gmail.com:y5y3gegnxh:077a21740dabf66196fe3a98d73d63ca",
    "2swagrahul@gmail.com:y5y3gegnxh:c04fd0675945b56b72b5d4d7ae8c996f",
    "9swagemu@gmail.com:y5y3gegnxh:7abc6307a9d578e6eba5438762b3700c",
    "10swagemu@gmail.com:y5y3gegnxh:67e9ad8c9cd8e6f59dabed7a3210e5ea",
    "12swagemu@gmail.com:y5y3gegnxh:ebeec7d49669a9001d06a7ce116f82d7",
    # "14swagemu@gmail.com:y5y3gegnxh:f9e1e112d34bbf57ea821874c7b1273b",
    # "15swagemu@gmail.com:y5y3gegnxh:f6066581045f213e018d7b49f8d2a18e",    
]

#login
def bearer_finder(email,pswd,sig):
    headers = {
        'Host': 'app.swagbucks.com',
        'user-agent': 'SwagIQ-Android/35 (okhttp/3.10.0);Vivo 1801',
        # 'content-length': '226',
        # 'accept-encoding': 'gzip',
    }

    params = {
        'cmd': 'apm-1',
    }

    data = {
        "emailAddress": email,
        "pswd": pswd,
        "persist": "on",
        "showmeter": "0",
        "advertiserID": "115da33f-7d5e-4a58-9fc8-90ccf88186a7",
        "modelNumber": "RMX2027",
        "osVersion": "8.1.0",
        "appid": "37",
        "appversion": "37",
        "sig": sig
    }
    # data =json.dumps(data)
    response = httpx.post('https://app.swagbucks.com/',
                             params=params,
                             headers=headers,
                             data=data).json()
    member_id = response["member_id"]
    username = response["user_name"]
    p_hash = response["sig"]
  #  device = response["_device"]

    #bearer_finder
    headers = {
        'Host': 'api.playswagiq.com',
        'user-agent': 'SwagIQ-Android/35 (okhttp/3.10.0)',
        # 'content-length': '196',
        # 'accept-encoding': 'gzip',
    }

    data = {
        '_device': '2385df68-5df7-4fd2-8ae5-57661e97f408',
        'partnerMemberId': member_id,
        'partnerUserName': username,
        'verify': 'false',
        'partnerApim': '1',
        'partnerHash': p_hash,
    }

    response = httpx.post('https://api.playswagiq.com/auth/token',
                             headers=headers,
                             data=data).json()
    accessToken = response["accessToken"]
    refreshToken = response["refreshToken"]

#USER ID FIND START ..

    headers = {
        'Host': 'api.playswagiq.com',
        'user-agent': 'SwagIQ-Android/35 (okhttp/3.10.0)',
        'authorization': f'Bearer {accessToken}',
        # 'content-length': '146',
        # 'accept-encoding': 'gzip',
    }

    data = {
        '_refreshToken': f'{refreshToken}',
        '_device': '2385df68-5df7-4fd2-8ae5-57661e97f408',
    }

    response = httpx.post('https://api.playswagiq.com/session/verify', headers=headers, data=data).json()
    user_id = response["profile"]["id"]

#USER ID FIND END ..

#STORING ALL TOKENS/IDS IN DICT ..

    token = {}
    token["username"] = username
    token["bearer"] = accessToken 
    token["refresh"] = refreshToken 
    token["partner_hash"] = p_hash 
    token["member_id"] = member_id
    token["uid"] = user_id
    datas.append(token) 
    return token


for i in acc:
    print(i)
    i = i.split(":")
    print(i[0] + "\n" + i[1])
    bearer_finder(email=i[0],pswd=i[1],sig=i[2])
                                                                                                                                                                                          
datas = json.dumps(datas,indent=4)    
print(datas)
file = open("config.json",mode="w")
file.write(datas)
file.close()