import requests, enum
from config.settings import API_KEY, COUNTRY_NAME
from .models import City


class Api_type(enum.Enum):
    Daily = 0
    Weekly = 1
    
# APIリクエストの発行
def weather_api_get(city, api_type):
    
    if city == None:
        # 都市が未選択の場合は「東京」を指定する。
        location = f'Tokyo,{COUNTRY_NAME}'
    else:
        location = f'{city},{COUNTRY_NAME}'
    
    if Api_type.Daily == api_type:
        # APIタイプが日次（Daily）の場合
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&lang=ja&units=metric'
    elif Api_type.Weekly == api_type:
        # APIタイプが週次（Weekly）の場合
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&lang=ja&units=metric'

    # 気象情報の取得
    res_weather_inf = requests.get(url)
    data = res_weather_inf.json()  # レスポンスをJSON形式で取得
    
    return data