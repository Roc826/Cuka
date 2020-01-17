import json
import requests
import os

async def get_weather_of_city(city: str) -> str:
    citycode=getCityCode(city)
    if citycode:
        api = 'http://t.weather.sojson.com/api/weather/city/{}'.format(str(citycode))
        req = requests.get(api)
        weather = json.loads(req.text)
        ans = "日期:{ymd}  {week}\n" \
              "天气:{type}\n" \
              "当前温度:{wendu}\n" \
              "空气质量:{quality}\n" \
              "最高温:{high}\n" \
              "最低温:{low}\n" \
              "湿度:{shidu}\n" \
              "风向:{fx}\n" \
              "风力:{fl}\n" \
              "pm2.5:{pm25}\n" \
              "pm10:{pm10}\n" \
              "aqi:{aqi}\n" \
              "日出:{sunrise}\n" \
              "日落:{sunset}\n" \
              "注意事项:{notice}\n"
        ans =ans.format(
            ymd=weather['data']['forecast'][0]['ymd'],
            week=weather['data']['forecast'][0]['week'],
            type=weather['data']['forecast'][0]['type'],
            wendu=weather['data']['wendu'],
            quality=weather['data']['quality'],
            high=weather['data']['forecast'][0]['high'],
            low=weather['data']['forecast'][0]['low'],
            shidu=weather['data']['shidu'],
            fx=weather['data']['forecast'][0]['fx'],
            fl=weather['data']['forecast'][0]['fl'],
            pm25=weather['data']['pm25'],
            pm10=weather['data']['pm10'],
            aqi=weather['data']['forecast'][0]['aqi'],
            sunrise=weather['data']['forecast'][0]['sunrise'],
            sunset=weather['data']['forecast'][0]['sunset'],
            notice=weather['data']['forecast'][0]['notice']
        )
        return ans
    else:
        return "抱歉没能查到这个城市呢"


def getCityCode(cityname:str):
    with open(os.path.dirname(__file__)  + "/citycode.json", "r")as fp:
        citycode = json.load(fp)
    for province in citycode['城市代码']:
        for city in province['市']:
            if cityname == city['市名']:
                return city['编码']

    return False