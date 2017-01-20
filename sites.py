import json
import re
import time
import webbrowser

import execjs
from bs4 import BeautifulSoup

from base import SharedBase


class Ck101(SharedBase):
    def __init__(self, url):
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url)
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        self.name = self.flyleaf_soup.title.text
        return self.name

    def get_parent_info(self):
        self.ref_box = []
        soup_box = self.flyleaf_soup.findAll('div', {'class': 'relativeRec'})
        for border in soup_box:
            for li in border.findAll('li'):
                ref_link = li.a['href']
                ref_title = li.a['title']
                self.ref_box.insert(0, (ref_title, ref_link))
        return self.ref_box

    def get_page_info(self, ref_link):
        inner_data = self.get_data('http://comic.ck101.com%s' % ref_link)
        pages = re.findall(r'第(\d+)頁', inner_data)
        return int(pages[-1])

    def get_image_link(self, ref_link, page):
        inner_page_data = self.get_data('http://m.comic.ck101.com%s/%s' % (ref_link[:-1], page))
        soup_box = BeautifulSoup(inner_page_data, 'html.parser')
        data = soup_box.findAll('div', {'class': 'img', 'id': 'comicimg'})
        for border in data:
            for img in border.findAll('img'):
                link = img['src']
        return link

    def down(self, comic_name, parent_link, link, parent_title, page, dir=''):
        img_data = self.get_data(link, 'http://m.comic.ck101.com%s' % parent_link, is_file=True)
        file_path = self.get_path(comic_name, parent_title, page, ext=link.split('.')[-1], dir=dir)
        with open(file_path, 'wb+') as file:
            file.write(img_data)


class DM5(SharedBase):
    def __init__(self, url):
        self.general_formula = 'http://www.dm5.com/%s/chapterfun.ashx?cid=%s&page=%s'
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url, is_destop=True)
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        soup_box = self.flyleaf_soup.findAll('h1', {'class': 'new_h2'})
        for i in soup_box:
            self.name = i.text
        return self.name

    def get_parent_info(self):
        self.ref_box = []
        soup_box = self.flyleaf_soup.findAll('ul', {'class': 'nr6 lan2'})
        for border in soup_box:
            for li in border.findAll('li'):
                if li.a.has_attr('title'):
                    ref_link = li.a['href']
                    ref_title = li.a['title']
                    self.ref_box.insert(0, (ref_title, ref_link))
        return self.ref_box

    def get_page_info(self, parent_link):
        inner_page_data = self.get_data('http://www.dm5.com%s' % parent_link, is_destop=True)
        # pages = re.findall(r'%s\-p(\d+)?\/\'\>第\d+?页' % parent_link[:-1], inner_page_data)
        # return int(pages[-1])
        page = re.findall(r'var DM5_IMAGE_COUNT=(\d+)', inner_page_data)
        return int(page[0])

    def get_image_link(self, parent_link, page):
        javascript_script = ''
        while javascript_script is '':
            javascript_script = self.get_data(self.general_formula % (parent_link, parent_link[2:-1], page),
                                              'http://www.dm5.com%s' % parent_link)
            if javascript_script is '':
                webbrowser.open_new('http://www.dm5.com%s' % parent_link)
                time.sleep(3)
        link = execjs.eval(javascript_script)[0]
        link_safe = self.unicodeToURL(link)
        return link_safe

    def down(self, comic_name, parent_link, link, parent_title, page, dir=''):
        img_data = self.get_data(link, 'http://www.dm5.com%s' % parent_link, is_file=True)
        filename_ext = re.compile('\.([a-zA-Z]*?)\?').search(link).groups()[0]
        with open(self.get_path(comic_name, parent_title, page, filename_ext, dir), 'wb+') as file:
            file.write(img_data)


class Dmzj(SharedBase):
    def __init__(self, url):
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url)
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        soup_box = self.flyleaf_soup.findAll('h1')
        for border in soup_box:
            self.name = border.text
        return self.name

    def get_parent_info(self):
        self.ref_box = []
        soup_box = self.flyleaf_soup.findAll('div', {'class': 'tab-content zj_list_con autoHeight'})
        for border in soup_box:
            for li in border.findAll('li'):
                ref_link = li.a['href']
                ref_title = li.text
                self.ref_box.append((ref_title, ref_link))
        return self.ref_box

    def get_page_info(self, parent_link):
        inner_page_data = self.get_data(parent_link)
        inner_page_soup = BeautifulSoup(inner_page_data, 'html.parser')
        inner_script = inner_page_soup.find('script', {'type': 'text/javascript'})
        inner_script_refined = inner_script.text.split('\n')[3].strip().replace('eval(', '')[:-1]
        result = execjs.eval(inner_script_refined)
        self.info_dict = json.loads(result.replace('var pages=pages=\'', '').rstrip('\';'))
        return int(self.info_dict['sum_pages'])

    def get_image_link(self, parent_link, page):
        link_combined = self.info_dict['page_url']
        link_list = link_combined.split('\r\n')
        link = 'http://images.dmzj.com/' + link_list[page - 1]
        return link

    def down(self, comic_name, parent_link, link, parent_title, page, dir=''):
        img_data = self.get_data(link, parent_link, is_file=True)
        with open(self.get_path(comic_name, parent_title, page, link.split('.')[-1], dir=dir), 'wb+') as file:
            file.write(img_data)


class manhua_Dmzj(SharedBase):
    def __init__(self, url):
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url)
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        soup_box = self.flyleaf_soup.findAll('h1')
        for border in soup_box:
            self.name = border.text
        return self.name

    def get_parent_info(self):
        self.ref_box = []
        soup_box = self.flyleaf_soup.findAll('div', class_=re.compile("cartoon_online_border.*"))
        for border in soup_box:
            for li in border.findAll('li'):
                ref_link = li.a['href']
                ref_title = li.text
                self.ref_box.append((ref_title[0:-2], ref_link))
        return self.ref_box

    def get_page_info(self, parent_link):
        inner_page_data = self.get_data('http://manhua.dmzj.com%s' % parent_link, is_destop=True)
        inner_page_soup = BeautifulSoup(inner_page_data, 'html.parser')
        inner_script = inner_page_soup.find('script', {'type': 'text/javascript'})
        inner_script_refined = inner_script.text.split('\n')[3].strip().replace('eval(', '')[:-1]
        result = execjs.eval(inner_script_refined)
        self.image_list = json.loads(result.replace('var pages=pages=\'', '').rstrip('\';'))
        return len(self.image_list)

    def get_image_link(self, parent_link, page):
        link = 'http://images.dmzj.com/' + self.image_list[page - 1]
        return link

    def down(self, comic_name, parent_link, link, parent_title, page, dir=''):
        img_data = self.get_data(link, 'http://manhua.dmzj.com' + parent_link, is_destop=True, is_file=True)
        with open(self.get_path(comic_name, parent_title, page, link.split('.')[-1], dir=dir), 'wb+') as file:
            file.write(img_data)


class Ehentai(SharedBase):
    def __init__(self, url):
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url)
        self.flyleaf_soup = BeautifulSoup(self.flyleaf_data, 'html.parser')

    def get_name(self):
        self.name = self.flyleaf_soup.title.text
        return self.name

    def get_parent_info(self):
        self.ref_box = [(self.name, self.flyleaf_url)]
        return self.ref_box

    def get_page_info(self, parent_link):
        self.page_box = []
        soup_box = self.flyleaf_soup.find_all(attrs={'class': 'gdtm'})
        for item in soup_box:
            ref_link = item.a['href']
            self.page_box.append(ref_link)
        return len(self.page_box)

    def get_image_link(self, parent_link, page):
        page_link = self.page_box[page - 1]
        inner_page_data = self.get_data(page_link)
        inner_page_soup = BeautifulSoup(inner_page_data, 'html.parser')
        box = inner_page_soup.find('iframe')
        img_link = box.findNext('img')['src']
        return img_link

    def down(self, comic_name, parent_link, link, parent_title, page, dir=''):
        img_data = self.get_data(link, parent_link, is_file=True)
        with open(self.get_path(comic_name, parent_title, page, link.split('.')[-1], dir=dir), 'wb+') as file:
            file.write(img_data)
