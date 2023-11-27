import json
from django.shortcuts import render
from bs4 import BeautifulSoup as bs
from .models import TbCroll
from django.views import View
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from urllib.parse import quote_plus
from selenium import webdriver
from django.db import models, connection
from django.db.models.functions import TruncDate
from django.db.models import Count, F


# 크롤링용 임포트
import requests
import time

from bs4 import BeautifulSoup

context = {}
# 뷰 작성 시작
def croll_view(request):
    print("croll/croll_view.html")
    context = {}
    context['bo_type'] = 'OCR'
    context['sub_menu_title'] = '크롤링 리스트'

    return render(request, 'croll/croll_view.html', context)
def croll_iframe(request):
    print("croll/croll_iframe.html")
    context = {}
    context['bo_type'] = 'OCR'
    context['sub_menu_title'] = '크롤링 리스트'

    return render(request, 'croll/croll_iframe.html', context)
class SearchListView(View):
    def post(self, request):
        print("SearchListView-post")
        query = request.POST.get("query")#'부산 관광지'

        if query: # query가 없으면 오류
            tbc = TbCroll.objects.filter(posttitle=query)
            #print("<==query:"+str(tbc))
            if tbc: # data가 없으면 오류
                TbCroll.objects.all().delete()

        #data = json.loads(request.body)
        start_date = datetime(2023, 11, 25)
        start_date = str(start_date)[:10]
        end_date = datetime(2023, 11, 27)
        end_date = str(end_date)[:10]
        cd_min = start_date[6:7] + '/' + start_date[8:10] + '/' + start_date[:4]
        cd_max = end_date[6:7] + '/' + end_date[8:10] + '/' + end_date[:4]
        tbs = f'cdr:1,cd_min:{cd_min},cd_max:{cd_max}'
        params = {'q': query, 'hl': 'ko', 'tbm': 'nws', 'tbs': tbs}
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        cookie = {'CONSENT': 'YES'}
        url = f'https://www.google.com/search?tbm=nws&source=lnms&sa=X&'
        #print("url=" + url)

        req = requests.get(url, params=params, headers=header, cookies=cookie)

        soup = bs(req.text, 'lxml')
        list = soup.find_all('div', '.yuRUbf') #n0jPhd ynAwRc MBeuO nDgy9d
        print("list_text=" + str(list))
        for i in list:
            i_text = str(i.get_text())
            print("i_text=" + i_text)
            post_title = str(i.get_text())
            print("post_title=" + post_title)

            posting_date = soup.select(
                'dl > dd.txt_block > span'
            )
            posting_date = str(posting_date)
            print("posting_date="+posting_date)
            blog_url = soup.select(
                'dl > dd.txt_block > span > a.url'
            )
            blog_url= str(blog_url)
            print("blog_url=" + blog_url)
            rsData = TbCroll(posttitle=post_title, postingdate=posting_date, blogurl=blog_url)
            rsData.save()

        return HttpResponse(status=200)
    def get(self, request):
        print("SearchListView-get")
        return JsonResponse({'search list': list(TbCroll.objects.values())}, status=200)

def SeleniumListView(request):
    print("SeleniumListView")
    #group by 인 경우 이 형식으로 사용 할것
    query = 'SELECT search_txt, created_at, COUNT(id) AS cnt FROM TB_CROLL group by search_txt, created_at'
    cursor = connection.cursor()
    row = cursor.execute(query)
    datas = row.fetchall()
    data = list()
    for i in datas:
        d = dict()
        d['search_txt'] = i[0]
        d['created_at'] = i[1]
        d['cnt'] = i[2]
        data.append(d)
    #cursor = connection.cursor()
    #cursor.execute("""SELECT search_txt, created_at, COUNT(id) AS cnt FROM TB_CROLL group by search_txt, created_at""")
    #queryset = cursor.fetchall()
    #print("<=dental_list: " + str(a1))

    #context['queryset'] = queryset
    return render(request, 'croll/croll_list.html', {'data': data})

def SeleniumRunView(request):
    print("SeleniumDetailView")

    query = request.GET.get("search", '')

    # Check if the query is empty
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl + quote_plus(query)
    print("<--url:"+ str(url))
    # chromedriver path input
    driver = webdriver.Chrome()
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height == new_height:
            break
        else:
            last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html)
    v = soup.select('.yuRUbf')

    for i in v:
        post_title = str(i.select_one('.LC20lb.DKV0Md').text)
        #print(i.a.attrs['href'])
        blog_url = str(i.a.attrs['href'])
        rsData = TbCroll(posttitle=post_title, search_txt=query, blogurl=blog_url, createdat=datetime.now())
        rsData.save()
    driver.close()

    return render(request, 'croll/croll_list.html')