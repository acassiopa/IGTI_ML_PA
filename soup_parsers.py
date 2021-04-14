from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import dateutil.parser
from pandas import DataFrame
from pathlib import Path
import urllib.request

class Soup_parser(ABC):
    news_source: str
    news_array = list()

    def __init__(self, urls_file_path, security_code):
        self.urls_file = urls_file_path
        self.security = security_code
        with open(urls_file_path, 'r') as _url_list_f:
            self.url_list = _url_list_f.read().split()


    @abstractmethod
    def parse():
        ...

    def to_csv(self, path: str):
        news_df = DataFrame(self.news_array, columns=['code', 'source', 'url', 'title', 'datetime', 'raw_text'])
        news_df.to_csv(path, index=False)

class InfoM_parser(Soup_parser):
    news_source = 'Infomoney'
    # def __init__(self, urls_file_path, security_code):
    #     super().__init__()

    def parse(self) -> None:
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:

            with urllib.request.urlopen(url) as url_request:
                page = url_request.read()

            soup = BeautifulSoup(page, "html.parser")

            try:
                time_tag = soup.find('time')
                article_date = time_tag['datetime']

                article_tag = soup.find(class_='article-content')

                p_list = article_tag.find_all('p', class_=False)

                for p in p_list:
                    for tag in p.find_all():
                        if tag.name not in valid_tags:
                            tag.decompose()
            except Exception as e:
                print('ERRO NO PARSE DA URL ', url)
                print(e)
                continue

            # dict to insert into collection
            news_data = {}
            news_data['code']       = self.security
            news_data['source']     = self.news_source
            news_data['url']        = url
            news_data['title']      = soup.title.text
            news_data['datetime']   = dateutil.parser.parse(article_date, ignoretz=True)
            news_data['raw_text']   = article_tag.get_text(separator=' ', strip=True)

            self.news_array.append(news_data)