from base import SharedBase
import os

def main_loop(ref_box):
    for ref_tuple in ref_box:
        parent_title, parent_link = ref_tuple
        total_page = website_object.get_page_info(parent_link)
        for page in range(1, total_page + 1):
            try:
                if os.path.exists(base.get_path(comic_name, parent_title, page, 'jpg')):
                    print('%s page %d has been downloaded before' % (parent_title, page))
                else:
                    link = website_object.get_image_link(parent_link, page)
                    website_object.down(comic_name, parent_link, link, parent_title, page)
                    print('%s page %d has been downloaded successfully' % (parent_title, page))
            except:
                print('Error occurred when downloading %s, Page %d.' % (parent_title, page))


user_input_url = input('URL?\n')
base = SharedBase(user_input_url)
if base.get_site_name() is 'dm5':
    from sites import DM5 as SiteClass
elif base.get_site_name() is 'ck101':
    from sites import Ck101 as SiteClass
elif base.get_site_name() is 'dmzj':
    from sites import Dmzj as SiteClass
elif base.get_site_name() is 'ehentai':
    from sites import Ehentai as SiteClass
try:
    website_object = SiteClass(user_input_url)
    comic_name = website_object.get_name()
    ref_box = website_object.get_parent_info()
    print('%s, total %d chapters detected.' % (comic_name, len(ref_box)))
    main_loop(ref_box)
except ConnectionError as e:
    print('%s, consider using a proxy or a VPN.' % e)
