import getopt
import glob
import sys
from multiprocessing.pool import ThreadPool

from base import SharedBase


def main_loop(ref_box, download_range):
    if download_range:
        ref_box = ref_box[-download_range:]
    for ref_tuple in ref_box:
        parent_title, parent_link = ref_tuple
        total_page = website_object.get_page_info(parent_link)
        jobs_comic_name = list()
        jobs_parent_link = list()
        jobs_link = list()
        jobs_parent_title = list()
        jobs_page = list()
        for page in range(1, total_page + 1):
            vague_path = website_object.get_path(comic_name, parent_title, page) + '*'
            if glob.glob(vague_path):
                print('%s page %d already existed.' % (parent_title, page))
            else:
                try:
                    link = website_object.get_image_link(parent_link, page)
                    jobs_comic_name.append(comic_name)
                    jobs_parent_link.append(parent_link)
                    jobs_link.append(link)
                    jobs_parent_title.append(parent_title)
                    jobs_page.append(page)
                except:
                    print('Error occurred when downloading %s, Page %d.' % (parent_title, page))
        pool_size = download_limit
        pool = ThreadPool(processes=pool_size)
        pool_outputs = pool.map(down_wrapper,
                                zip(jobs_comic_name, jobs_parent_link, jobs_link, jobs_parent_title, jobs_page))
        pool.close()
        pool.join()


try:
    opts, args = getopt.getopt(sys.argv[1:], 'hu:l:t:', ['url=', 'latest=', 'threading='])
    if opts == []:
        raise getopt.GetoptError('No argument provided.')
    for opt, arg in opts:
        fetch_latest = False
        download_limit = 1
        if opt == '-h':
            print('driveit.py\n\nUsage: python3 driveit.py [-u <URL>] [-l <number>] [-t <number>] [-h]')
            print('Options:\n\t-u\tDownload comics from specific origin')
            print('\t-l\tOptional. Download latest x chapters from origin')
            print('\t-t\tOptional. Max download concurrent number, 1 for default')
            print('\t-h\tPrint this help')
            sys.exit()
        elif opt in ('-u', '--url'):
            user_input_url = arg
        elif opt in ('-l', '--latest'):
            fetch_latest = int(arg)
        elif opt in ('-t', '--threading'):
            download_limit = int(arg)
except getopt.GetoptError as e:
    print('%s\n\nUsage: python3 driveit.py -u <URL>\nSee driveit.py -h for details' % e)
    sys.exit(2)

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


    def down_wrapper(args):
        try:
            website_object.down(*args)
            print('%s page %d has been downloaded successfully' % (
                args[3], args[4]))  # args[3] is parent_title and args[4] is page
        except:
            print('Error occurred when downloading %s, Page %d.' % (args[3], args[4]))


    comic_name = website_object.get_name()
    ref_box = website_object.get_parent_info()
    print('%s, total %d chapters detected.' % (comic_name, len(ref_box)))
    main_loop(ref_box, fetch_latest)
except ConnectionError as e:
    print('%s, consider using a proxy or a VPN.' % e)
