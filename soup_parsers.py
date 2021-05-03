from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import dateutil.parser
from pandas import DataFrame
from urllib.request import Request, urlopen

class SoupParser(ABC):
    news_source: str
    news_array = list()

    def __init__(self, url_list, stock_symbol):
        self.url_list = url_list
        self.stock_symbol = stock_symbol

    @abstractmethod
    def parse():
        ...

    def _create_append_news_dict(self, url, title, date, text):
        news_data = dict()
        news_data['code']       = self.stock_symbol
        news_data['source']     = self.news_source
        news_data['url']        = url
        news_data['title']      = title
        news_data['datetime']   = dateutil.parser.parse(date, ignoretz=True)
        news_data['raw_text']   = text
        self.news_array.append(news_data)

    def to_csv(self, path: str):
        news_df = DataFrame(self.news_array, columns=['code', 'source', 'url', 'title', 'datetime', 'raw_text'])
        news_df.to_csv(path, index=False)

class InfoMoneyParser(SoupParser):
    news_source = 'InfoMoney'

    def parse(self) -> None:
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
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
            
            self._create_append_news_dict(url,
                                     soup.title.text,
                                     article_date,
                                     article_tag.get_text(separator=' ', strip=True))

class InvestingParser(SoupParser):
    news_source = 'Investing'

    def parse(self):
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")

            try:
                article_date = soup.find(class_='contentSectionDetails').span.get_text()
                article_tag = soup.find(class_='articlePage')
                p_list = article_tag.find_all('p', class_=False)
                for p in p_list:
                    for tag in p.find_all():
                        if tag.name not in valid_tags:
                            tag.decompose()
            except Exception as e:
                print('ERRO NO PARSE DA URL ', url)
                print(e)
                continue

            self._create_append_news_dict(url,
                                     soup.title.text,
                                     article_date,
                                     article_tag.get_text(separator=' ', strip=True))


class MoneyTimesParser(SoupParser):
    news_source = 'MoneyTimes'

    def parse(self):
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")

            try:
                article_date = soup.find(class_='single-meta__date').get_text()
                article_tag = soup.find(class_='single__text')
                p_list = article_tag.find_all('p', class_=False)
                for p in p_list:
                    for tag in p.find_all():
                        if tag.name not in valid_tags:
                            tag.decompose()
            except Exception as e:
                print('ERRO NO PARSE DA URL ', url)
                print(e)
                continue

            self._create_append_news_dict(url,
                                     soup.title.text,
                                     article_date,
                                     article_tag.get_text(separator=' ', strip=True))
                

class SunoParser(SoupParser):
    news_source = 'Suno'

    def parse(self) -> None:
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")

            try:
                time_tag = soup.find('time')
                article_date = time_tag['datetime']
                article_tag = soup.find(class_='newsContent__article')
                p_list = article_tag.find_all('p', class_=False)
                for p in p_list:
                    for tag in p.find_all():
                        if tag.name not in valid_tags:
                            tag.decompose()
            except Exception as e:
                print('ERRO NO PARSE DA URL ', url)
                print(e)
                continue

            self._create_append_news_dict(url,
                                     soup.title.text,
                                     article_date,
                                     article_tag.get_text(separator=' ', strip=True))
                

class G1Parser(SoupParser):
    news_source = 'G1'

    def parse(self) -> None:
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")

            try:
                time_tag = soup.find('time')
                article_date = time_tag['datetime']
                article_tag = soup.find('article')
                p_list = article_tag.find_all('p', class_='content-text__container')
                for p in p_list:
                    for tag in p.find_all():
                        if tag.name not in valid_tags:
                            tag.decompose()
            except Exception as e:
                print('ERRO NO PARSE DA URL ', url)
                print(e)
                continue

            self._create_append_news_dict(url,
                                     soup.title.text,
                                     article_date,
                                     article_tag.get_text(separator=' ', strip=True))


class UOLParser(SoupParser):
    news_source = 'UOL'

    def parse(self) -> None:
        valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a', 'spam']

        for url in self.url_list:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, "html.parser")

            try:
                article_date = soup.find(p, class_='p-author time').get_text()
                article_tag = soup.find('div', class_='text  ')
                p_list = article_tag.find_all('p', class_=False)
                for p in p_list:
                    for tag in p.find_all():
                        if tag.name not in valid_tags:
                            tag.decompose()
            except Exception as e:
                print('ERRO NO PARSE DA URL ', url)
                print(e)
                continue

            self._create_append_news_dict(url,
                                     soup.title.text,
                                     article_date,
                                     article_tag.get_text(separator=' ', strip=True))