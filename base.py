from urllib import request
import os
import re


class SharedBase(object):
    def __init__(self, url):
        self.url = url

    def get_site_name(self):
        if re.match(r'http://(www|en).dm5.com/.+?', self.url):
            return 'dm5'
        if re.match(r'http://comic.ck101.com/comic/\d+?.*', self.url):
            return 'ck101'
        else:
            raise NameError(self.url)

    def get_data(self, url, referrer=''):
        self.webheader = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
            'Referer': referrer}
        req = request.Request(url=url, headers=self.webheader)
        web_page = request.urlopen(req)
        page_data = web_page.read()
        return page_data

    def get_path(self, name, parent, page, ext):
        filename = str(page) + '.' + ext
        path = os.path.join(os.getcwd(), name, str(parent))
        file_path = os.path.join(path, filename)
        if os.path.exists(path) is False:
            os.makedirs(path)
        return file_path
