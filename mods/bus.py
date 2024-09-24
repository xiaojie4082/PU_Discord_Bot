import requests
import json
import time
import threading

import os
from dotenv import load_dotenv

# 載入環境變數從 .env 檔案中
load_dotenv()
app_id = os.getenv("TDX_ID")
app_key = os.getenv("TDX_KEY")
auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

# 公車站牌代碼
# 162 靜宜大學(校門), 主顧樓, 聖母堂(終), 聖母堂(起)
# 301 靜宜大學(校門), 主顧樓, 靜園餐廳(終), 靜園餐廳(起)
# 368 靜宜大學(校門), 主顧樓, 聖母堂(終), 聖母堂(起)
# 300、302~310 靜宜大學(專用道), 往市區, 往海線
stop_dict = {
    '162': ['TXG20091','TXG20092','TXG20093','TXG20094'], 
    # '300': ['TXG13567','TXG21478'],
    '301': ['TXG20091','TXG20092','TXG15247','TXG15230'], 
    # '302': ['TXG13567','TXG19438'],
    # '303': ['TXG13567','TXG19438'],
    # '304': ['TXG13567','TXG19438'],
    # '305': ['TXG13567','TXG19438'],
    # '306': ['TXG13567','TXG19438'],
    # '307': ['TXG13567','TXG19438'],
    # '308': ['TXG13567','TXG19438'],
    # '309': ['TXG13567','TXG19438'],
    # '310': ['TXG13567','TXG19438'],
    '368': ['TXG24503','TXG24504','TXG24505','TXG24506']
} 

# 取得公車即時到站時間
# return: EstimateTime(公車即時到站時間)
# {route: [time1, time2, time3, ...]}
def EstimateTime():

    class Auth():
        def __init__(self, app_id, app_key):
            self.app_id = app_id
            self.app_key = app_key
        def get_auth_header(self):
            content_type = 'application/x-www-form-urlencoded'
            grant_type = 'client_credentials'
            return{
                'content-type' : content_type,
                'grant_type' : grant_type,
                'client_id' : self.app_id,
                'client_secret' : self.app_key
            }

    class data():
        def __init__(self, app_id, app_key, auth_response):
            self.app_id = app_id
            self.app_key = app_key
            self.auth_response = auth_response
        def get_data_header(self):
            auth_JSON = json.loads(self.auth_response.text)
            access_token = auth_JSON.get('access_token')
            return{
                'authorization': 'Bearer ' + access_token
            }

    try:
        d = data(app_id, app_key, auth_response)     
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)

    EstimateTime = {}
    now = time.mktime(time.localtime())

    def fetch_thread(route,uid):
        url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/Taichung/{route}?%24filter=StopUID%20eq%20%27{uid}%27&%24orderby=StopSequence&%24format=JSON"
        try:          
            data_response = requests.get(url, headers=d.get_data_header())  
            data = json.loads(data_response.text)
            if data[0]["EstimateTime"] is not None:
                if data[0]["EstimateTime"]/60 > 3:
                    EstimateTime[route].append(str(int(data[0]["EstimateTime"]/60)) + " 分鐘")
                else:
                    EstimateTime[route].append("進站中...")
            else:    
                print("flag")
                target_time = time.strptime(data[0]["NextBusTime"], "%Y-%m-%dT%H:%M:%S%z")
                target_time = time.mktime(target_time)
                diff_minute = int(target_time - now) / 60
                if diff_minute > 3:
                    EstimateTime[route].append(str(int(diff_minute)) + " 分鐘")
                elif diff_minute > 0:
                    EstimateTime[route].append("即將進站") 
                else:
                    EstimateTime[route].append("尚未發車")         
        except Exception as e:
            EstimateTime[route].append("尚未發車")
            # print(f"Error fetching data for route {route} and uid {uid}: {e}")

    for route, uids in stop_dict.items(): 
        EstimateTime[route] = []
        for uid in uids: 
            thread = threading.Thread(target=fetch_thread, args=(route, uid))                                                                
            thread.start()
            thread.join()

    return EstimateTime