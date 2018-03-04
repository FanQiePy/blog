# -*- coding: utf-8 -*-
import requests
from lxml import html as HTML
from lxml import etree


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {
    'User-Agent': USER_AGENT,
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml, image/jpeg',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh'
}

COLUMNS = [
    ('Ehco-python', '从零开始写Python爬虫', 'scrapy-zero'),
    ('djstudyteam', 'Django 学习小组', 'django'),
    ('zimei', 'Python中文社区', 'python'),
    ('gooseeker', '学习python网络爬虫建设智慧时空数据库', 'scrapy-database'),
]


def zhihu_zhuanlang(column_name):
    url = 'https://zhuanlan.zhihu.com/{}'.format(column_name)
    base_url = 'https://zhuanlan.zhihu.com'
    try:
        response = requests.get(url, headers=headers)
    except requests.HTTPError:
        return None
    # html = etree.fromstring(response.text, parser=etree.HTMLParser())
    html = HTML.fromstring(response.text)
    div = html.cssselect('#react-root div div div.Layout-main div.ColumnPostList ul li:nth-child(1) div div')[0]

    title = div.cssselect('a span.PostListItem-title')[0].text
    summary = div.cssselect('a p.PostListItem-summary')[0].text
    href = base_url + div.cssselect('a')[0].get('href')
    time = div.cssselect('div span:nth-child(1) div time')[0].get('datetime')
    favour = div.cssselect('div > span:nth-child(2) > a:nth-child(1)')[0].text
    data = {'title': title, 'summary': summary, 'href': href, 'time': time, 'favour': favour}
    return data
