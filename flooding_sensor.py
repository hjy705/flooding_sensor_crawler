import json, psycopg2, os
from datetime import datetime
import api

now_time = datetime.now()


token_use = ""

if os.path.isfile("token.json"):
    with open('token.json',encoding='utf-8')as f:
        timedb = json.load(f)
    # 就去抓資料時間
    if (now_time - datetime(int(timedb["now_time"][0:4]), int(timedb["now_time"][5:7]), int(timedb["now_time"][8:10]), int(timedb["now_time"][11:13]), int(timedb["now_time"][14:16]), int(timedb["now_time"][17:19]))).total_seconds() > 72000:
        # 檔案時間跟現在時間差如果大於20小時
        token_use = api.request_token()
    else:
        # 使用token.json的token
        token_use = timedb["token"]
else:
    # 沒有檔案的話就直接去打token api
    token_use = api.request_token()
    

# 取淹水感知器資料
data = api.request_data(token_use)

# 資料庫連線
with open('db.json','r', encoding = 'utf-8') as f:
    db = json.load(f)
conn = psycopg2.connect(database=db["database"], user=db["user"] , password=db["password"], host=db["host"], port=db["port"])
cur = conn.cursor()

# 查找在資料庫中全部測站的最新一筆資料
cur.execute("SELECT stationid, Max(time) FROM flood_sensor_level GROUP BY stationid;")
lastest_data_in_local_db = cur.fetchall()
lastest_data_in_local_db_container = {}
for eachStation in lastest_data_in_local_db:
    stationid = eachStation[0]
    time = eachStation[1]
    lastest_data_in_local_db_container[stationid] = time

# 比對api資料以及資料庫資料
sql_string = ""
for value in data:
    # 單一測站最新一筆欄位資料
    stationid = value["StationId"]
    timevalue = value["Measurements"][0]["TimeStamp"]
    levelvalue = value["Measurements"][0]["Value"]
    # 判斷時間是否相同以及該測站目前有資料
    if stationid not in lastest_data_in_local_db_container.keys() :
        sql_string += "INSERT INTO public.flood_sensor_level (stationid, time, level) VALUES ('{a}','{b}',{c});".format(a= stationid, b=timevalue, c=str(levelvalue))
    else:
        # api資料時間跟db資料時間
        if  timevalue != lastest_data_in_local_db_container[stationid]:
            sql_string += "INSERT INTO public.flood_sensor_level (stationid, time, level) VALUES ('{a}','{b}',{c});".format(a= stationid, b=timevalue, c=str(levelvalue))          
        else:
            pass

# 執行insert
if len(sql_string) > 0:
    cur.execute(sql_string)
    conn.commit()
else:
    pass
conn.close()



# log_result = {
#     "time": "",
#     "status": ""
# }

# try:
#     
#     log_result["status"] = "執行成功"
# except:
#     log_result["status"] = "執行失敗"

# with open log_result
