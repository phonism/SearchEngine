import requests
from bs4 import BeautifulSoup


def download_url(url):
    r = requests.get(url)
    while r.status_code != 200:
        r = requests.get(url)
    return r.text


def parse_text(html):
    bs = BeautifulSoup(html)
    return bs.select('div.usertext-body')[1].text

# Test
# print parse_text(download_url(
# 'http://www.reddit.com/r/learnprogramming/comments/2nunkb/teaching_a_kid_how_to_program'))