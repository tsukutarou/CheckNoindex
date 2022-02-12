import time
import re
import os

from bs4 import BeautifulSoup
from selenium import webdriver


def CheckNoindex(PageURL):

     #ファイルのある場所に移動
     os.chdir(os.path.dirname(__file__))

     #ドライバーの設定 
     options = webdriver.ChromeOptions()
     options.add_experimental_option('excludeSwitches', ['enable-logging'])
     options.add_argument('--headless')
     driver = webdriver.Chrome('.\chromedriver',options=options)

     try:
         #URL読み込み
         driver.get(PageURL)
         time.sleep(1)
         
         #htmlの情報を取得
         html = driver.page_source.encode('utf-8')
         soup = BeautifulSoup(html, "html.parser")
     finally:
         driver.close()

     #metaタグのうち「name="robots"」のものを抽出
     metas = soup.find_all('meta', {'name': 'robots'})

     #そもそもrobotsのname要素のmetaタグが無い場合はここで終了
     if len(metas)==0:
         print(f"{PageURL} に noindexタグはありません")
         return
     
     #metaタグからcontensにnoindexがあるかどうかの抽出
     meta_contents = [bool(re.search('noindex',tag["content"])) for tag in metas]

     #noindexの有無を出力
     if any(meta_contents):
         print(f"{PageURL} は noindexタグを含んでいます")
     else:
         print(f"{PageURL} に noindexタグはありません")



if __name__=="__main__":

     #テスト
     CheckNoindex("https://tsukutarou.com/entry/noindex")
     CheckNoindex("https://tsukutarou.com/entry/yesindex")

