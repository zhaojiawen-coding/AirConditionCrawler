
import requests
from bs4 import BeautifulSoup

def get_city_coding():
    CITY_CODING='./city_coding'

    city_coding={}
    with open(CITY_CODING,'r') as f:
        for line in f.readlines():
            line=line.strip()
            try:
                city,coding=line.split('\t')
                city_coding[city.strip()]=coding.strip()
            except ValueError as e:
                continue
    return city_coding

def build_url(city_coding,year=None,month=None):
    BASE='http://www.tianqihoubao.com/aqi/'
    city_base_url=BASE+"{}.html"
    city_data_base_url=BASE+"{}-{}{}.html"
    if year is not None and month is not None:
        month=str(month) if month>=10 else '0'+str(month)
        return city_data_base_url.format(city_coding,year,month)
    else:
        return city_base_url.format(city_coding)

def get_some_day_air_condition(city_coding,url):
    try:
        r=requests.get(url)
        if r.status_code == 200:
            r.encoding='GBK'
            html_file=r.text
            soup=BeautifulSoup(html_file,'html.parser')

            # data_table=soup.find_all('table')
            data_table=soup.table
            return parse(city_coding,data_table)
        else:
            return None
    except Exception as e:
        print('connect error')
        print(e)
        return None

def parse(city_coding,data):
    name_index=1
    content=data.contents[name_index:]
    result=[]

    for index,c in enumerate(content[::2]):
        if index==0:
            result.append(tuple(['city']+c.text.split()))
        else:
            result.append(tuple([city_coding]+c.text.split()))
    return result

def get_from_http(city_coding,year=None,month=None):
    '''

        :param city_coding: city Chinese Name, e.g hangzhou
        :param year: e.g 2016
        :param month: e.g 10
        :param day:  e.g 5
        :return: {
                    'city': string,
                    'air_conditions': [air_condition]
                 }

                 air_condition = (Date, AQI, Pm2.5, Pm10, No2, So2, Co, O3)

        '''
    url=build_url(city_coding,year,month)
    content=get_some_day_air_condition(city_coding,url)
    return content

if __name__=='__main__':
    city_coding=get_city_coding()
    assert city_coding['杭州']=='hangzhou'

    hangzhou=city_coding['杭州']

    print('testing')

    assert build_url(hangzhou,2020,5)=='http://www.tianqihoubao.com/aqi/hangzhou-202005.html'
    assert build_url(hangzhou,2020)=='http://www.tianqihoubao.com/aqi/hangzhou.html'
    assert build_url(hangzhou)=='http://www.tianqihoubao.com/aqi/hangzhou.html'

    assert get_some_day_air_condition("hangzhou","http://www.tianqihoubao.com/aqi/hangzhou-202005.html") is not None

    data=get_some_day_air_condition("hangzhou","http://www.tianqihoubao.com/aqi/hangzhou-202005.html")

    city_data=get_from_http('hangzhou',2016,5)
    print(city_data)
    print('test done')

