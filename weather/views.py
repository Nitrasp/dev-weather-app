from config.settings import COUNTRY_NAME
from django.shortcuts import render
from django.views.generic.base import TemplateView
from enum import Enum
from .models import City
from . import utils
import collections, datetime, locale

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
        response_api_list = utils.weather_api_get(city, utils.Api_type.Daily)
        
        # APIの結果(JSON)を各テンプレートのデータに整形
        city_name, weather_list, date_dict = convertJson(response_api_list)
        
        wl = []
        for w in weather_list:
            if w['date_text'] == list(date_dict)[0]:
                wl.append(w)

        # テンプレート用のコンテキスト作成
        context = super().get_context_data()
        # 都市名を格納
        context['city_name'] = city_name
        # 時間毎の気象情報辞書を格納
        context['weather_list'] = wl
        #【テーブルヘッダ用】重複している日付の個数辞書の格納
        context['date_text'] = list(date_dict)[0]

        return render(request, template_name, context)
    
class WeeklyView(baseView):
    # GET通信
    def get(self, request, city=None):
        
        template_name = 'weekly.html'
        
        # 都市の気象情報を取得
        response_api_list = utils.weather_api_get(city, utils.Api_type.Weekly)
        
        # APIの結果(JSON)を各テンプレートのデータに整形
        city_name, list, date_dict = convertJson(response_api_list)
        
        # テンプレート用のコンテキスト作成
        context = super().get_context_data()
        # 都市名を格納
        context['city_name'] = city_name
        # 時間毎の気象情報辞書を格納
        context['list'] = list
        #【テーブルヘッダ用】重複している日付の個数辞書の格納
        context['date_dict'] = date_dict

        return render(request, template_name, context)

def convertJson(response_api_list):
        # 都市名の取得
        city_name = response_api_list['city']['name']
        
        # localeモジュールで時間のロケールを'ja_JP.UTF-8'に変更する
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        
        # 時間毎の気象情報リストを作成
        weather_list, date_list = [], []
        for res in response_api_list['list']:
            # UNIX時間の変換
            date_text = datetime.datetime.fromtimestamp(res['dt']).strftime('%m/%d(%a)')
            time_text = datetime.datetime.fromtimestamp(res['dt']).strftime('%H:%M')
            # 各気象情報辞書の作成
            weather_list.append(dict(date_text=date_text, time_text=time_text, main=res['main'], weather=res['weather'][0], wind=res['wind']))
            # 月日(E)辞書の作成
            date_list.append(date_text)
            
        # 【テーブルヘッダ用】重複している日付の個数取得
        date_list = dict(collections.Counter(date_list))
        
        # 都市名、気象情報リスト、日付リスト
        return city_name, weather_list, date_list