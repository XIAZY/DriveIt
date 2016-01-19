import re
import webbrowser
import time
from nodejs.bindings import node_run
from base import SharedBase


class DM5(SharedBase):
    def __init__(self, url):
        self.general_formula = 'http://www.dm5.com/m%s/chapterfun.ashx?cid=%s&page=%s'
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url).decode('utf-8')
        self.name = re.findall(r'\<title\>(.*?)\_', self.flyleaf_data)[0]

    def get_name(self):
        return self.name

    def get_chapter_info(self):
        ref_box = {}
        chapter_match = re.compile(r'href\=\"\/m(\d+?)\/\"\stitle\=\"%s\s第(\d+?)话' % self.name)
        for cid, chapter in chapter_match.findall(self.flyleaf_data):
            if chapter not in ref_box.keys():
                ref_box[int(chapter)] = int(cid)
        return ref_box

    def get_page_info(self, cid):
        inner_page_data = self.get_data('http://www.dm5.com/m%d/' % cid).decode('utf-8')
        pages = re.findall(r'\/m%s\-p(\d+)?\/\'\>第\d+?页' % cid, inner_page_data)
        return int(pages[-1])

    def get_image_link(self, cid, page):
        node_script = ''
        while node_script is '':
            node_script = self.get_data(self.general_formula % (cid, cid, page),
                                        'http://www.dm5.com/m%d/' % cid).decode('utf-8')
            if node_script is '':
                webbrowser.open_new('http://www.dm5.com/m%d/' % cid)
                time.sleep(3)
        refined_script = 'process.stdout.write(' + node_script.strip() + ')\n'
        with open('towards_direct_link.js', 'w') as file:
            file.write(refined_script)
        stderr, stdout = node_run('towards_direct_link.js')
        return stdout.split(',')[0]

    def down(self, name, cid, link, parent, page, is_volume):
        img_data = self.get_data(link, 'http://www.dm5.com/m%s/' % cid)
        with open(self.get_path(name, parent, page, 'jpg'), 'wb+') as file:
            file.write(img_data)

    def is_volume(self):
        return False

    def get_volume_info(self):
        pass
