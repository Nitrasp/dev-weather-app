from django.db import models

# 都市情報マスタ
class City(models.Model):
    # 都市名
    name = models.CharField(max_length=256, null=False)
    # 国名
    country = models.CharField(max_length=256, null=False)
    # 経度
    lon = models.FloatField(null=False)
    # 緯度
    lat = models.FloatField(null=False)