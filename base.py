import os
import re
from urllib import parse

import requests


class SharedBase(object):
    def __init__(self, url):
        self.url = url

    def get_site_name(self):
        if re.match(r'http://(www|en).(dm5|dm9).com/.+?', self.url):
            return 'dm5'
        if re.match(r'http://comic.ck101.com/comic/\d+?.*', self.url):
            return 'ck101'
        if re.match(r'http://www.dmzj.com/info/.+?.html', self.url):
            return 'dmzj'
        if re.match(r'http://manhua.dmzj.com/[a-z]+?', self.url):
            return 'manhua_dmzj'
        if re.match(r'http://g.e-hentai.org/g/\d+?/[a-zA-Z0-9]+?', self.url):
            return 'ehentai'
        else:
            raise NameError(self.url)

    def get_data(self, url, referrer='', is_destop=False, is_file=False):
        if not is_destop:
            self.webheader = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
                'Referer': referrer, 'Accept-Encoding': 'gzip, deflate, sdch'}
        else:
            self.webheader = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
                'Referer': referrer, 'Accept-Encoding': 'gzip, deflate, sdch'}
        page_data = requests.get(url=url, headers=self.webheader)
        if is_file:
            return page_data.content
        return page_data.text

    def get_path(self, name, parent, page, ext='', dir=''):
        filename = str(page) + '.' + ext
        if dir != '':
            # path = os.path.join(dir, name, str(parent))
            path_safe = os.path.join(dir, self.purify(name), self.purify(str(parent)))
        else:
            # path = os.path.join(os.getcwd(), name, str(parent))
            path_safe = os.path.join(os.getcwd(), self.purify(name), self.purify(str(parent)))
        file_path = os.path.join(path_safe, filename)
        if not os.path.exists(path_safe):
            # try:
            #     try:
            #         if os.path.exists(path):
            #             pass
            #         else:
            #             os.makedirs(path)
            #     except FileExistsError as e:
            #         pass
            # except NotADirectoryError as e:
            #     try:
            #         if os.path.exists(path_safe):
            #             pass
            #         else:
            #             os.makedirs(path_safe)
            #     except FileExistsError as e:
            #         pass
            try:
                os.makedirs(path_safe)
            except FileExistsError as e:
                pass
        return file_path

    def purify(self, str):
        str_safe = str.replace('/', '').replace('\\', '').replace('*', '').replace('?', '').replace('<', '').replace(
            '>', '').replace('|', '').replace(':', '').replace('"', '')
        return str_safe

    def unicodeToURL(self, url):
        url_safe = parse.quote(url, '%/:=&?~#+!$,;\'@()*[]')
        return url_safe
