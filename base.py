import os
import re
from urllib import request, parse


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
        if re.match(r'http://g.e-hentai.org/g/\d+?/[a-zA-Z0-9]+?', self.url):
            return 'ehentai'
        else:
            raise NameError(self.url)

    def get_data(self, url, referrer='', is_destop=False):
        if not is_destop:
            self.webheader = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
                'Referer': referrer}
        else:
            self.webheader = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'Referer': referrer}
        req = request.Request(url=url, headers=self.webheader)
        web_page = request.urlopen(req)
        page_data = web_page.read()
        return page_data

    def get_path(self, name, parent, page, ext=''):
        filename = str(page) + '.' + ext
        path = os.path.join(os.getcwd(), name, str(parent))
        path_safe = os.path.join(os.getcwd(), self.safe(name), self.safe(str(parent)))
        file_path = os.path.join(path, filename)
        if os.path.exists(path) is False and os.path.exists(path_safe) is False:
            try:
                os.makedirs(path)
            except NotADirectoryError as e:
                os.makedirs(path_safe)
        if os.path.exists(path) is True:
            return file_path
        else:
            return os.path.join(path_safe, filename)

    def safe(self, str):
        str_safe = str.replace('/', '').replace('\\', '').replace('*', '').replace('?', '').replace('<', '').replace(
                '>', '').replace('|', '').replace(':', '').replace('"', '')
        return str_safe

    def unicodeToURL(self, url):
        url_safe = parse.quote(url, '%/:=&?~#+!$,;\'@()*[]')
        return url_safe
