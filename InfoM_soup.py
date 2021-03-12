import urllib.request
from bs4 import BeautifulSoup
from pandas import DataFrame
from pathlib import Path
from dateutil.parser import parse

# setup constants
security    = 'BBAS3'
news_source = 'Infomoney'

# Obtain urls
urls_file = Path('../arquivos/input_test.txt')
# urls_file = Path('../arquivos/BBAS3_InfoMoney.txt')
with open(urls_file, 'r') as url_list_f:
    url_list = url_list_f.read().split()

news_array = list()
valid_tags = ['strong', 'b', 'em', 'i', 'p', 'a']

for url in url_list:

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
    news_data['code']       = security
    news_data['source']     = news_source
    news_data['url']        = url
    news_data['title']      = soup.title.text
    news_data['datetime']   = parse(article_date, ignoretz=True)
    news_data['raw_text']   = article_tag.get_text(separator=' ', strip=True)

    news_array.append(news_data)

news_df = DataFrame(news_array, columns=['code', 'source', 'url', 'title', 'datetime', 'raw_text'])
news_df.to_csv(Path('../arquivos/Test.csv'), sep=';')

