
'''
get location map information,such as map 杭州 => hangzhou
'''

import requests
from bs4 import BeautifulSoup

def get_location_html():
    http_url='http://www.tianqihoubao.com/aqi/'

    r=requests.get(http_url)

    r.encoding='GBK'

    html_file=r.text
    return html_file

def parse_location(html_doc):
    soup=BeautifulSoup(html_doc,'html.parser')

    """
    BeautifulSoup 的select方法
    https://www.cnblogs.com/yizhenfeng168/p/6979339.html
    标签名不加任何修饰   类名前加 .  id名前加 #     >代表组合 也可空格代表组合
    """
    CITY_CHECK='.citychk > dl > dd > a'

    city_map=[]

    city_check=soup.select(CITY_CHECK)

    #<a href="/aqi/taiyuan.html">太原 </a>
    for c in city_check:
        coding=c['href'].split('/')[2].replace('.html','')
        city=c.string
        city_map.append((city,coding))

    return city_map

def save_city_map(city_map):
    with open('city_coding','w+') as f:
        for c in city_map:
            if c:
                f.write(c[0]+'\t'+c[1]+'\n')
    print('write done!')

if __name__=='__main__':
    save_city_map(parse_location(html_doc=get_location_html()))
