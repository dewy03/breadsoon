import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','breadsoon.settings') #pro_3은 프로젝트 이름 입니다. 변경해서 사용
import django
django.setup()

from map.models import Bakery_Info, Bakery_Location, Bakery_Review

baseurl = 'https://www.siksinhot.com/theme/magazine/1964'
# url = baseurl + urllib.parse.quote_plus(plusUrl)
html = urllib.request.urlopen(baseurl).read()
soup = BeautifulSoup(html, 'html.parser')
bread_url = soup.select('p > a')
# count=1

def Bakery_Crawler():
    result=[]

    for i in bread_url:
        url=i.attrs['href']
        new_html=urllib.request.urlopen(url).read()
        new_soup = BeautifulSoup(new_html,'html.parser')
        bread_address=new_soup.find(class_='txt_adr')
        bread_google_url=new_soup.find(class_='btnTy1 btn_google_map') 
        split_temp=bread_google_url.attrs['href'].split('=')
        google_positon=split_temp[1].split(',')

        bakery_reviewers = [
            soup_obj.text for soup_obj in new_soup.select('div.name_data strong')]
        bakery_reviews = [
            soup_obj.text for soup_obj in new_soup.select('div.score_story p')]
        bakery_menu = [
            soup_obj.text for soup_obj in new_soup.select('ul.menu_ul span.tit')]
     
        bakery_obj = {
            'Bakery_name': i.text,
            'Bakery_address': bread_address.text,
            'Bakery_menu' : str(bakery_menu),
            'latitude': float(google_positon[0]),
            'longitude': float(google_positon[1]),
            'reviews': zip(bakery_reviewers,bakery_reviews)
            }

        result.append(bakery_obj)
    return result

if __name__=='__main__':
    bakery_data = Bakery_Crawler()
    for item in bakery_data:
        Info = Bakery_Info(
            Bakery_name = item['Bakery_name'], 
            Bakery_address = item['Bakery_address'],
            Bakery_menu = item['Bakery_menu']
            )
        Info.save()
        Bakery_Location(info=Info,Latitude = item['latitude'],Longitude=item['longitude']).save()

        for reviewer, review in item['reviews']:
            Bakery_Review(info=Info, Bakery_Reviewer=reviewer, Bakery_Contents=review).save()
        