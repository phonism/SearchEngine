import requests
from bs4 import BeautifulSoup
import logging
import time
import re
import os.path
import base64

# TODO is it good idea to set it at this point
logging.getLogger().setLevel(logging.DEBUG)
_r_learnprogramming_url = re.compile(r'http://(www.)?reddit.com/r/learnprogramming')


def download_reddit_url(url):
    # assert url.startswith('http://www.reddit.com/r/learnprogramming')
    assert _r_learnprogramming_url.match(url)
    headers = {
        'User-Agent': 'SearchingReddit bot version 0.1',
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception("Non-Ok status code: {}".format(r.status_code))
    return r.text


def parse_reddit_post(html):
    bs = BeautifulSoup(html)
    return bs.select('div.usertext-body')[1].text


class Crawler(object):
    def __init__(self, start_url, storage_dir):
        self.start_url = start_url
        self.storage_dir = storage_dir

    @staticmethod
    def _make_absolute_url(url):
        return 'http://www.reddit.com' + url

    @staticmethod
    def _next_url(url):
        return ' '

    def crawl(self):
        current_page_url = self.start_url
        while True:
            current_page = download_reddit_url(current_page_url)
            bs = BeautifulSoup(current_page)
            all_posts_links = bs.findAll('a', attrs={'class': 'title'})
            post_links = [Crawler._make_absolute_url(link['href']) for link in all_posts_links]
            for post_link in post_links:
                html = download_reddit_url(post_link)
                stored_text_file_name = os.path.join(self.storage_dir, base64.b16encode(post_link))
                stored_text_file = open(stored_text_file_name, 'w')
                stored_text_file.write(html.encode('utf8'))
                time.sleep(2)
            next_page_url = bs.find('a', attrs={'rel': 'next'})['href']
            logging.debug("First post is {}".format(post_links[0]))
            current_page_url = next_page_url
            logging.debug("Next page url is {}".format(next_page_url))
            time.sleep(2)


# Test
crawler = Crawler('http://www.reddit.com/r/learnprogramming', 'crawled_urls')
crawler.crawl()
# print parse_text(download_
# url('http://reddit.com/r/learnprogramming/comments/2nunkb/teaching_a_kid_how_to_program'))