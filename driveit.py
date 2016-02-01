from base import SharedBase


def main_loop(refer_box):
    # total_parents = max(refer_box.keys())
    # if is_volume is True:
    #     parent_str = 'Volume'
    # else:
    #     parent_str = 'Chapter'
    # for parent in range(1, total_parents + 1):
    #     if parent in refer_box.keys():
    #         cid = refer_box[parent]
    #         for page in range(1, website_object.get_page_info(cid) + 1):
    #             link = website_object.get_image_link(cid, page)
    #             try:
    #                 website_object.down(comic_name, cid, link, parent, page, is_volume)
    #                 print('%s %d page %d has been downloaded successfully' % (parent_str, parent, page))
    #             except:
    #                 print('Error occurred when downloading %s %d, Page %d.' % (parent_str, parent, page))
    #     else:
    #         print('Chapter %d cannot be found.' % parent)
    for ref_tuple in refer_box:
        title, parent_link = ref_tuple
        total_page = website_object.get_page_info(parent_link)
        for page in range(1, total_page + 1):
            link = website_object.get_image_link(parent_link, page)
            try:
                website_object.down(comic_name, parent_link, link, title, page)
                print('%s page %d has been downloaded successfully' % (title, page))
            except:
                print('Error occurred when downloading %s, Page %d.' % (title, page))


user_input_url = input('URL?\n')
base = SharedBase(user_input_url)
if base.get_site_name() is 'dm5':
    from sites import DM5 as SiteClass
elif base.get_site_name() is 'ck101':
    from sites import Ck101 as SiteClass
website_object = SiteClass(user_input_url)
comic_name = website_object.get_name()
ref_box = website_object.get_parent_info()
print('%s, total %d chapters detected.' % (comic_name, len(ref_box)))

main_loop(ref_box)