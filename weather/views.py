from config.settings import COUNTRY_NAME
from django.shortcuts import render
from django.views.generic.base import TemplateView
from enum import Enum
from .models import City
from . import util
import datetime, locale

# 共通処理クラス
class baseView(TemplateView):
    def get_context_data(self):
        
        context = super().get_context_data()
        
        # 都市一覧の取得
        cities = City.objects.filter(country=COUNTRY_NAME)
        
        # コンテキストに情報を設定
        context['cities'] = cities
        
        return context

# 初期表示ビュークラス
class InitView(baseView):
        
    # GET通信
    def get(self, request, country=None):
        
        template_name = 'index.html'
        
        if country == None:
            location = f'Tokyo,{COUNTRY_NAME}'
        else:
            location = f'{country},{COUNTRY_NAME}'
        
        # 都市の気象情報を取得
        weather_info = util.weather_api_get(location)
        
        # localeモジュールで時間のロケールを'ja_JP.UTF-8'に変更する
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        dt_text = datetime.datetime.fromtimestamp(weather_info['dt']).strftime ( '%m月 %d日(%a)' )
        print(dt_text)
        
        # コンテキストに情報を設定
        context = super().get_context_data()
        context['weather'] = weather_info
        context['dt_text'] = dt_text

        return render(request, template_name, context)