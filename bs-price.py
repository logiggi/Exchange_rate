# 네이버 금융에서 환율 정보 추출
from bs4 import BeautifulSoup
import urllib.request as req
import html

url = "http://finance.naver.com/marketindex/"   # 네이버 금융 시장지표 url
res = req.urlopen(url)

soup = BeautifulSoup(res, "html.parser", from_encoding = 'cp949')   # 한글 깨짐 방지를 위한 encoding

name_list = soup.select("h3.h_lst > span.blind")            # 환율 이름
price_list = soup.select("div.head_info > span.value")      # 환율 가격 정보
amount_list = soup.select("div.head_info > span.change")    # 변화량
change_list = soup.select("div.head_info > span.blind")     # 변화 (보합, 상승, 하락)

# 단위 추출을 위한 작업: 단위 태그가 txt_krw, txt_usd 등 여러개가 있기에 위와 다른 추가 작업이 필요
span_list = soup.find_all("span")   
unit_list = []

for span in span_list:
    if span.has_attr('class'):
        if "txt_" in span['class'][0]:  # span 태그의 class 이름이 "txt_"가 포함되어 있으면
            unit_list.append(span.string)

u = 0
for i in range(len(name_list)):
    if name_list[i].string == "달러인덱스": # 달러인덱스의 경우 단위가 따로 없으므로 예외처리
        print("{0:2d}".format(i+1), " " + name_list[i].string + ": " + price_list[i].string + ", 전날대비 " + amount_list[i].string + " " + change_list[i].string) 
    else:
        print("{0:2d}".format(i+1), " " + name_list[i].string + ": " + price_list[i].string + unit_list[u] + ", 전날대비 " + amount_list[i].string + " " + change_list[i].string) 
        u += 1
