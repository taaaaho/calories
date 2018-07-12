from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "http://calorie.slism.jp/"

def getData(searchUrl):
  html = urlopen(searchUrl)
  soup = BeautifulSoup(html, "html.parser")
  
  #各食材のカロリー取得
  calories = soup.find_all("strong", class_="soshoku_c")
  
  #各食材の詳細取得する用のリンク
  foodLinks = soup.find_all("a", class_="soshoku_a")

  for (food, calorie) in zip(foodLinks,calories):
    print(food.string + ":" + calorie.string + "kcal")
    
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

# 対象のカテゴリURLを取得
categoryLinks = soup.find_all(href=re.compile("/category/"))
for link in categoryLinks:
  #カテゴリのリンク開く
  categoryUrl = url + link.get("href")
  #1ページ目の取得
  getData(categoryUrl)
  
  #2ページ目が存在するかチェック
  html = urlopen(categoryUrl)
  soup = BeautifulSoup(html, "html.parser")
  
  #全件の表示を取得
  paging = soup.find("p", class_="pagerTxt")
  
  #1ページあたり最大50件表示なので割って残りのページ数計算
  point = int(paging.string[10:]) / 50 - 1
  
  #URL作成用
  pageCount = 2
  while point > 0:
    getData(categoryUrl + str(pageCount))
    pageCount += 1
    point -= 1

