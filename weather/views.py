from config.settings import COUNTRY_NAME
from django.shortcuts import render
from django.views.generic.base import TemplateView
from enum import Enum
from .models import City
from . import Utils
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
    def get(self, request, city=None):
        
        template_name = 'index.html'
        
        # 都市の気象情報を取得
        weather_info = Utils.weather_api_get(city, Utils.Api_type.Daily)
        
        # localeモジュールで時間のロケールを'ja_JP.UTF-8'に変更する
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        # UNIX時間の変換
        dt_text = datetime.datetime.fromtimestamp(weather_info['dt']).strftime ( '%m月 %d日(%a)' )
        
        # コンテキストに情報を設定
        context = super().get_context_data()
        context['weather'] = weather_info
        context['dt_text'] = dt_text

        return render(request, template_name, context)
    
class WeeklyView(baseView):
    # GET通信
    def get(self, request, city=None):
        
        template_name = 'weekly.html'
        
        # 都市の気象情報を取得
        response_api_list = Utils.weather_api_get(city, Utils.Api_type.Weekly)
        
        # 都市名の取得
        city_name = response_api_list['city']['name']
        
        # localeモジュールで時間のロケールを'ja_JP.UTF-8'に変更する
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        
        # 時間毎の気象情報リストを作成
        list = []
        for res in response_api_list['list']:
            # UNIX時間の変換
            dt_text = datetime.datetime.fromtimestamp(res['dt']).strftime('%m月 %d日(%a)')
            # 月日(E)、各気象情報辞書の作成
            list.append(dict(dt_text=dt_text, main=res['main'], weather=res['weather'], wind=res['wind']))
        
        # テンプレート用のコンテキスト作成
        context = super().get_context_data()
        # 都市名を格納
        context['city_name'] = city_name
        # 時間毎の気象情報辞書を格納
        context['list'] = list

        return render(request, template_name, context)
