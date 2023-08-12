import requests
from config.settings import API_KEY, COUNTRY_NAME
from .models import City
        
# APIリクエストの発行
def weather_api_get(city):
    
    # 気象情報の取得
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=ja&units=metric'
    res_weather_inf = requests.get(url)
    data = res_weather_inf.json()  # レスポンスをJSON形式で取得
    
    return data