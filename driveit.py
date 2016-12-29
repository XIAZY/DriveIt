import argparse
import glob
from multiprocessing.pool import ThreadPool

from base import SharedBase


def main_loop(ref_box, download_range):
    ref_box = ref_box[-download_range:]

    for ref_tuple in ref_box:
        parent_title, parent_link = ref_tuple
        total_page = website_object.get_page_info(parent_link)
        jobs = list()
        for page in range(1, total_page + 1):
            jobs.append((parent_title, parent_link, page))
        pool_size = download_limit
        pool = ThreadPool(processes=pool_size)
        pool.map(loop_thread, jobs)
        pool.close()
        pool.join()


def loop_thread(args):
    parent_title, parent_link, page = args
    vague_path = website_object.get_path(comic_name, parent_title, page) + '*'
    if glob.glob(vague_path):
        print('%s page %d already existed.' % (parent_title, page))
    else:
        try:
            link = website_object.get_image_link(parent_link, page)
            website_object.down(comic_name, parent_link, link, parent_title, page)
            print('%s page %d has been downloaded successfully' % (parent_title, page))
        except:
            print('Error occurred when downloading %s, Page %d.' % (parent_title, page))


def argparser():
    parser = argparse.ArgumentParser(description='A multithreading comic crawler.')
    parser.add_argument('url', help='URL of the comic\'s cover page')
    parser.add_argument('-l', '--latest', help='Download latest x chapters from origin')
    parser.add_argument('-t', '--thread', help='Number of threads. Default to be 1')
    return parser


parser = argparser()
args = parser.parse_args()
user_input_url = args.url
if args.thread:
    download_limit = int(args.thread)
else:
    download_limit = 1
if args.latest:
    fetch_latest = int(args.latest)
else:
    fetch_latest = 0

base = SharedBase(user_input_url)
if base.get_site_name() is 'dm5':
    from sites import DM5 as SiteClass
elif base.get_site_name() is 'ck101':
    from sites import Ck101 as SiteClass
elif base.get_site_name() is 'dmzj':
    from sites import Dmzj as SiteClass
elif base.get_site_name() is 'manhua_dmzj':
    from sites import manhua_Dmzj as SiteClass
elif base.get_site_name() is 'ehentai':
    from sites import Ehentai as SiteClass
else:
    print('this site not available yet')
    exit()
try:
    website_object = SiteClass(user_input_url)
    comic_name = website_object.get_name()
    ref_box = website_object.get_parent_info()
    print('%s, total %d chapters detected.' % (comic_name, len(ref_box)))
    main_loop(ref_box, fetch_latest)
except ConnectionError as e:
    print('%s, consider using a proxy or a VPN.' % e)
