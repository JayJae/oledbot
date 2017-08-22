from bs4 import BeautifulSoup
import requests


class BaseCrawler() :
    html = None
    header = None
    soup = None

    def __init__(self, url) :
        self.url = url


    def request_url(self) :
        with requests.Session() as s :
            res = s.get(self.url)
            if res.status_code != 200 :
                return False
            else :
                self.html = res.text
                self.header = res.headers
                self.soup = BeautifulSoup(self.html, 'lxml')
                return True




