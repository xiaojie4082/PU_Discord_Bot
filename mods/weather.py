import requests
import json
import os
from dotenv import load_dotenv

# 載入環境變數從 .env 檔案中
load_dotenv()

# 取得天氣資訊
# return: weather_data(天氣資訊), weather_info(天氣資訊), icon_url(天氣圖示網址)
def today_weather():
    
    key = os.getenv("CWA_KEY")
    url_FC0032001 = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + key + "&locationName=%E8%87%BA%E4%B8%AD%E5%B8%82"
    url_FC0032021 = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-021?Authorization=" + key + "&downloadType=WEB&format=JSON"
    weather_data = []

    try:
        data = requests.get(url_FC0032001)
        data = json.loads(data.text)
        for location in data["records"]["location"]:
            weather = {"locationName": location["locationName"]} 
            for weather_element in location["weatherElement"]:
                weather[weather_element["elementName"]] = weather_element["time"][0]["parameter"]
            weather_data.append(weather)
    except Exception as e:
        print(f"Error fetching data for CWA: {str(e)}")

    try:
        # https://openweathermap.org/weather-conditions
        # https://opendata.cwa.gov.tw/opendatadoc/MFC/A0012-001.pdf
        Wx_icon_url = {
            "晴天 ": "http://openweathermap.org/img/wn/01d@2x.png",
            "晴時多雲 ": "http://openweathermap.org/img/wn/02d@2x.png",
            "多雲時晴 ": "http://openweathermap.org/img/wn/02d@2x.png",
            "多雲": "http://openweathermap.org/img/wn/03d@2x.png",
            "多雲時陰 ": "http://openweathermap.org/img/wn/04d@2x.png",
            "時陰多雲 ": "http://openweathermap.org/img/wn/04d@2x.png",
            "陰天": "http://openweathermap.org/img/wn/04d@2x.png",
            "多雲陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "午後短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時晴短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "多雲時晴短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴時多雲短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "雨天 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "晴午後陰短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後陰短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "陰短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰午後短暫陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "晴時多雲陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "多雲時晴陣雨 ": "http://openweathermap.org/img/wn/10d@2x.png",
            "陰時多雲有雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰有雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰有陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "午後陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "有雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲短暫陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "短暫陣雨或雷雨後多雲 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "短暫雷陣雨後多雲": "http://openweathermap.org/img/wn/11d@2x.png",
            "短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴時多雲短暫陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時晴短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴時多雲陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時晴陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲有雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰有雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陰短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陰短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰短暫雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陣雨或雷雨後多雲": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰陣雨或雷雨後多雲": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰短暫陣雨或雷雨後多雲": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰短暫雷陣雨後多雲 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰雷陣雨後多雲": "http://openweathermap.org/img/wn/11d@2x.png",
            "雷陣雨後多雲": "http://openweathermap.org/img/wn/11d@2x.png",
            "陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "午後雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲局部雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後多雲局部陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後多雲局部短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後多雲局部短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後多雲短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後多雲短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後局部雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後局部陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後局部短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後局部短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴時多雲午後短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "多雲午後局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲午後局部陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲午後局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲午後局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲午後陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲午後短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲午後短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰午後短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲午後短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "多雲時晴午後短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後多雲陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後多雲短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後短暫雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後短暫雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴時多雲雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴時多雲午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後局部陣雨或雷雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲午後雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時晴雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時晴午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰午後短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部陣雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰有雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰短暫雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有雪 ": "http://openweathermap.org/img/wn/13d@2x.png",
            "多雲時陰短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "多雲短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "陰有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "陰時多雲有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "陰時多雲短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "陰短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "有雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "有雨或短暫雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰有雨或短暫雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有雨或短暫雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有雨或短暫雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有雨或短暫雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時晴有雨或雪": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴時多雲有雨或雪 ": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴有雨或雪 ": "http://openweathermap.org/img/wn/10d@2x.png",
            "短暫雨或雪": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時晴短暫雨或雪": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴時多雲短暫雨或雪": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴短暫雨或雪": "http://openweathermap.org/img/wn/10d@2x.png",
            "有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "多雲有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "多雲時晴有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "晴時多雲有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "晴有雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "晴有雪": "http://openweathermap.org/img/wn/13d/@2x.png",
            "多雲時晴短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "晴時多雲短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "晴短暫雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "晴有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "晴晨霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "晴時多雲有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "晴時多雲晨霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲時晴有霧 ": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲時晴晨霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲晨霧 ": "http://openweathermap.org/img/wn/50d@2x.png",
            "有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "晨霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "陰有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "陰晨霧 ": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲時陰有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲時陰晨霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "陰時多雲有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "陰時多雲晨霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "晴午後陰局部雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後陰局部陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後陰局部短暫雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "晴午後陰局部短暫陣雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "陰局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有局部陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有短暫雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲有霧有短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部雨有霧 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部短暫雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部短暫陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫雨晨霧 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲短暫陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "有霧有短暫雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "有霧有短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有局部陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰有霧有短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰短暫陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰有霧有陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有局部雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有局部陣雨 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有局部短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有局部短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有短暫雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲有霧有短暫陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫陣雨有霧 ": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲短暫陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰短暫雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰短暫陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陰局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陰局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陰局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "晴午後陰局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部短暫雷陣雨 ": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部短暫陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部短暫雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲有陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲有雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲有霧有陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲有霧有雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時晴短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰有陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰有雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰有霧有陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰有霧有雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "有霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "多雲時陰局部短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰局部雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲時陰雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰局部雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲有陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲有雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲有霧有陣雨或雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲有霧有雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲局部雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰時多雲雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陰短暫雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "雷陣雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "多雲局部雨或雪有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "多雲時陰局部雨或雪有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰時多雲局部雨或雪有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陰局部雨或雪有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫雨或雪有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "有雨或雪有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫陣雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫雨晨霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "有雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "陣雨有霧": "http://openweathermap.org/img/wn/09d@2x.png",
            "短暫陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "陣雨或雷雨有霧": "http://openweathermap.org/img/wn/11d@2x.png",
            "下雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "積冰": "http://openweathermap.org/img/wn/13d@2x.png",
            "暴風雪": "http://openweathermap.org/img/wn/13d@2x.png"

        }
        icon_url = Wx_icon_url[weather_data[0]["Wx"]["parameterName"]]
    except Exception as e:
        icon_url = ""
        print(f"Error occurred while getting weather icon URL: {str(e)}")

    try:
        data = requests.get(url_FC0032021)
        data = json.loads(data.text)
        weather_info = data["cwaopendata"]["dataset"]["parameterSet"]["parameter"][0]["parameterValue"]
    except Exception as e:
        weather_info = ""
        print(f"Error occurred while getting weather info: {str(e)}")

    return weather_data, weather_info, icon_url