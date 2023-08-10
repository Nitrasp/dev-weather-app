from django.shortcuts import render
from django.views.generic.base import TemplateView
import requests, json
from django.http import JsonResponse
from config.settings import API_KEY

# 初期表示ビュークラス
class InitView(TemplateView):
    
    template_name = 'index.html'
    
    # 変数を渡す
    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        
        location = 'Tokyo,JP'
        
        # 都市の気象情報を取得
        weather_info = self.weather_api_get(location)
        
        # コンテキストに情報を設定
        context['weather'] = weather_info
        
        return context
    
    # APIリクエストの発行
    def weather_api_get(self, city):
        
        # 気象情報の取得
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=ja&units=metric'
        res_weather_inf = requests.get(url)
        data = res_weather_inf.json()  # レスポンスをJSON形式で取得

        print(type(data))
        
        # 気象アイコンの取得
        url = f'https://openweathermap.org/img/wn/10d@2x.png'
        res_weather_icon = requests.get(url)
        
        return data
    