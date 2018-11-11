from selenium import webdriver
from psycopg2 import connect
from newspaper import Article
from psycopg2.extensions import AsIs
import psycopg2
import requests


import csv

url = "https://timesofindia.indiatimes.com"
m = input("Enter month(1-9 and 10,11 and 12)")
y = input("Enter year yyyy")
d = input("Enter date 1-30 and 31")
table_name = 'news'

# con = connect(datbase='postgres')
conn = psycopg2.connect(host='localhost', user='postgres',
                        password='postgres', dbname='news_articles', port=5432)
cursor = conn.cursor()

# con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


browser = webdriver.Chrome()
f = csv.writer(open("contents.csv", "w"))


if d=='\n':
    if m == "1" or m == "3" or m == "5" or m == "7" or m == "8" or m == "10" or m == "12":
        k = 32
    else:
        k = 31

    for i in range(k):
        weblink = url + "/archive/year-" + y + ",month-" + m + ".cms"
        browser.get(weblink)
        tab = browser.find_element_by_id('calender')

        link = tab.find_element_by_link_text(str(i + 1))
        weblink = link.get_attribute('href')
        browser.get(weblink)
        links = browser.find_element_by_xpath(
            "/html/body/div[1]/table[2]/tbody/tr[2]/td[1]/div[3]/table")
        link = links.find_elements_by_css_selector('a')
        print(links)
        for l in link:
            h = l.get_attribute('href')
            t = l.get_attribute('text')
            '''request = requests.get(h)
            if request.status_code == 200:
                status = "Ok!"
                toi_article = Article(h, language="en")
                toi_article.download()
                toi_article.parse()
                toi_article.nlp()
                content = toi_article.text
            else:
                status = "Not Ok!"
                content = ""
            sql = "INSERT INTO news VALUES (default, %s, %s, %s,%s);"
            data = (t, h, status, content)
            cursor.execute(sql, data)
            conn.commit()'''
            f.writerow([t, h])


else:
    print(1)
    weblink = url + "/archive/year-" + y + ",month-" + m + ".cms"
    browser.get(weblink)
    tab = browser.find_element_by_id('calender')

    link = tab.find_element_by_link_text(d)
    weblink = link.get_attribute('href')
    browser.get(weblink)
    links = browser.find_element_by_xpath(
        "/html/body/div[1]/table[2]/tbody/tr[2]/td[1]/div[3]/table")
    link = links.find_elements_by_css_selector('a')
    for l in link:
        h = l.get_attribute('href')
        t = l.get_attribute('text')
        print(type(h))
        toi_article = Article(h, language="en")
        toi_article.download()
        toi_article.parse()
        toi_article.nlp()
        content = toi_article.text
        request = requests.get(h)
        if request.status_code == 200:
            status = "Ok!"
        else:
            status = "Not Ok!"
        # print(h)
        # print(t)
        # print(status)
        # t = str(t.replace('"', '\\"').replace("'", "\\'"))
        # h = str(h.replace('"', '\\"').replace("'", "\\'"))
        # content = str(content.replace('"', '\\"').replace("'", "\\'"))
        sql = "INSERT INTO news VALUES (default, %s, %s, %s,%s);"
        data = (t, h, status, content)
        cursor.execute(sql, data)
        conn.commit()
        f.writerow([t, h])
conn.close()
