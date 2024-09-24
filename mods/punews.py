import requests
from bs4 import BeautifulSoup

# 取得靜宜大學最新消息摘要
# return: summary(摘要)
def get_summary(href):
    try:
        html = requests.get(href)
        soup = BeautifulSoup(html.text, 'html.parser')
        summary = soup.find('meta', {'name': 'description'})['content'].strip()
        summary = BeautifulSoup(summary, 'html.parser').get_text()
    except Exception as e:
        summary = ""
    return summary

# 回傳靜宜大學最新消息
# return: title(標題), href(連結), summary(摘要)
def get_pu_news():
    try:
        url = 'https://www.pu.edu.tw/p/422-1000-1011.php?Lang=zh-tw'
        html = requests.get(url)

        soup = BeautifulSoup(html.text, 'html.parser')
        info_items = soup.find_all('div', 'mtitle')

        title = info_items[0].find('a').text.strip()
        href = info_items[0].find('a')['href']

        if href.startswith('/'):
            href = "https://www.pu.edu.tw" + href

        summary = get_summary(href)
    except Exception as e:
        print(f"[get_pu_news()] Error occurred: {e}")
        title = ""
        href = ""
        summary = ""
    return title, href, summary
