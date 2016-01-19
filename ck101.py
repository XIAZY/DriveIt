from base import SharedBase
import re


class Ck101(SharedBase):
    def __init__(self, url):
        self.flyleaf_url = url
        self.flyleaf_data = self.get_data(self.flyleaf_url).decode('utf-8')

    def get_name(self):
        name = re.findall(r'<li><h1\sitemprop="name">(.+?)<\/h1><\/li>', self.flyleaf_data)[0]
        return name

    def get_chapter_info(self):
        ref_box = {}
        chapter_match = re.compile(r'\'詳情頁\-lists\'\,\'.+?\s(\d+?)集\'\,\'\/vols\/(\d+?)\/')
        for chapter, cid in chapter_match.findall(self.flyleaf_data):
            if chapter not in ref_box.keys():
                ref_box[int(chapter)] = int(cid)
        return ref_box

    def get_page_info(self, cid):
        inner_data = self.get_data('http://comic.ck101.com/vols/%s/1' % cid).decode('utf-8')
        pages = re.findall(r'第(\d+)頁', inner_data)
        return int(pages[-1])

    def get_image_link(self, cid, page):
        inner_page_data = self.get_data('http://m.comic.ck101.com/vols/%s/%s' % (cid, page)).decode('utf-8')
        link_and_extension = re.findall('img src\=\"(http:[^\s]*?(jpg|png|gif))', inner_page_data)[0]
        self.ext = link_and_extension[1]
        return link_and_extension[0]

    def down(self, name, cid, link, parent, page, is_volume=False):
        img_data = self.get_data(link, 'http://m.comic.ck101.com/vols/%s/' % cid)
        if is_volume is False:
            file_path = self.get_path(name, parent, page, self.ext)
        else:
            file_path = self.get_path(name, 'V' + str(parent), page, self.ext)
        with open(file_path, 'wb+') as file:
            file.write(img_data)

    def is_volume(self):
        if re.findall(r'\'詳情頁\-lists\'\,\'.+?\s(\d+?)集\'\,\'\/vols\/(\d+?)\/', self.flyleaf_data):
            return True
        else:
            return False

    def get_volume_info(self):
        ref_box_volume = {}
        chapter_match = re.compile(r'\'詳情頁\-lists\'\,\'.+?\s(\d+?)卷\'\,\'\/vols\/(\d+?)\/')
        for chapter, cid in chapter_match.findall(self.flyleaf_data):
            if chapter not in ref_box_volume.keys():
                ref_box_volume[int(chapter)] = int(cid)
        return ref_box_volume
