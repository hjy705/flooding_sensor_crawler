import random,requests
from datetime import datetime


def notify_send(data, token, type):    
    result = {
        "flooding": [],
        "puddle": []
    }
    now_time = datetime.now()
    
    # 處理達到示警的測站資訊
    for value in data:
        datatime = value["Measurements"][0]["TimeStamp"]
        if type == "testing":
            datatime = now_time.strftime("%Y-%m-%d %H:%M:%S")
            value["Measurements"][0]["Value"] = random.randrange(10, 70) 
        else:
            pass
    if (now_time - datetime(int(datatime[0:4]), int(datatime[5:7]), int(datatime[8:10]), int(datatime[11:13]), int(datatime[14:16]), int(datatime[17:19]))).total_seconds() <= 600:
        if value["Measurements"][0]["Value"] >= 30 :
            result["flooding"].append(value["Name"])
        if 30 > value["Measurements"][0]["Value"] >= 10:
            result["puddle"].append(value["Name"])
    else:
        pass


    # 組notify字串並判斷發送動作
    message = str(now_time.strftime("%m-%d %H:%M:%S")) + "\n"+"淹水" + str(len(result["flooding"])) +'處' +'(' + ','.join(result["flooding"])+')' + "\n"+ "積水" + str(len(result["puddle"])) +'處' + '(' +','.join(result["puddle"])+')'
    print(message)
    if len(result["flooding"]) + len(result["puddle"]) > 0 :
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }

        payload = {'message': message}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)