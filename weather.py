import requests
import json
import os
from dotenv import load_dotenv

# 載入環境變數從 .env 檔案中
load_dotenv()

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
        Wx_icon_url = {
            "多雲": "http://openweathermap.org/img/wn/03d@2x.png",
            "多雲時晴": "http://openweathermap.org/img/wn/02d@2x.png",
            "晴時多雲": "http://openweathermap.org/img/wn/02d@2x.png",
            "晴朗": "http://openweathermap.org/img/wn/01d@2x.png",
            "陰天": "http://openweathermap.org/img/wn/50d@2x.png",
            "小雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "多雲短暫陣雨或雷雨": "http://openweathermap.org/img/wn/10d@2x.png",
            "陣雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "雷陣雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "小雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "陣雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "雷陣雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "濃霧": "http://openweathermap.org/img/wn/50d@2x.png",
            "大雷雨": "http://openweathermap.org/img/wn/11d@2x.png",
            "大雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "豪雨": "http://openweathermap.org/img/wn/09d@2x.png",
            "暴風雨": "http://openweathermap.org/img/wn/13d@2x.png",
            "風雪": "http://openweathermap.org/img/wn/13d@2x.png",
            "冰雹": "http://openweathermap.org/img/wn/13d@2x.png",
            "霾": "http://openweathermap.org/img/wn/50d@2x.png",
            "沙塵暴": "http://openweathermap.org/img/wn/50d@2x.png",
            "乾燥": "http://openweathermap.org/img/wn/50d@2x.png"
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