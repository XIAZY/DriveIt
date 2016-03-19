from base import SharedBase
import re
import webbrowser
import time
from bs4 import BeautifulSoup
import execjs

class Ck101(SharedBase):
    def __init__(self, url):
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url).decode('utf-8')
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        self.name = re.findall(r'<li><h1\sitemprop="name">(.+?)<\/h1><\/li>', self.flyleaf_data)[0]
        return self.name

    def get_parent_info(self):
        ref_box = []
        soup_box = self.flyleaf_soup.findAll('div', {'class': 'relativeRec'})
        for border in soup_box:
            for li in border.findAll('li'):
                ref_link = li.a['href']
                ref_title = li.a['title']
                ref_box.insert(0, (ref_title, ref_link))
        return ref_box

    def get_page_info(self, ref_link):
        inner_data = self.get_data('http://comic.ck101.com%s' % ref_link).decode('utf-8')
        pages = re.findall(r'第(\d+)頁', inner_data)
        return int(pages[-1])

    def get_image_link(self, ref_link, page):
        inner_page_data = self.get_data('http://m.comic.ck101.com%s/%s' % (ref_link[:-1], page)).decode('utf-8')
        soup_box = BeautifulSoup(inner_page_data, 'html.parser')
        data = soup_box.findAll('div', {'class': 'img', 'id': 'comicimg'})
        for border in data:
            for img in border.findAll('img'):
                link = img['src']
        return link

    def down(self, name, parent_link, link, parent, page):
        img_data = self.get_data(link, 'http://m.comic.ck101.com%s' % parent_link)
        file_path = self.get_path(name, parent, page, link.split('.')[-1])
        with open(file_path, 'wb+') as file:
            file.write(img_data)


class DM5(SharedBase):
    def __init__(self, url):
        self.general_formula = 'http://www.dm5.com/%s/chapterfun.ashx?cid=%s&page=%s'
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url).decode('utf-8')
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        soup_box = self.flyleaf_soup.findAll('h1', {'class': 'inbt_title_h2'})
        for i in soup_box:
            self.name = i.text
        return self.name

    def get_parent_info(self):
        ref_box = []
        soup_box = self.flyleaf_soup.findAll('ul', {'class': 'nr6 lan2', 'id': 'cbc_1'})
        for border in soup_box:
            for li in border.findAll('li'):
                ref_link = li.a['href']
                ref_title = li.a['title']
                ref_box.insert(0, (ref_title, ref_link))
        return ref_box

    def get_page_info(self, parent_link):
        inner_page_data = self.get_data('http://www.dm5.com%s' % parent_link).decode('utf-8')
        pages = re.findall(r'%s\-p(\d+)?\/\'\>第\d+?页' % parent_link[:-1], inner_page_data)
        return int(pages[-1])

    def get_image_link(self, parent_link, page):
        node_script = ''
        while node_script is '':
            node_script = self.get_data(self.general_formula % (parent_link, parent_link[2:-1], page),
                                        'http://www.dm5.com%s' % parent_link).decode('utf-8')
            if node_script is '':
                webbrowser.open_new('http://www.dm5.com%s' % parent_link)
                time.sleep(3)
        link=execjs.eval(node_script)[0]
        return link

    def down(self, name, parent_link, link, parent_title, page):
        img_data = self.get_data(link, 'http://www.dm5.com%s' % parent_link)
        with open(self.get_path(name, parent_title, page, 'jpg'), 'wb+') as file:
            file.write(img_data)
