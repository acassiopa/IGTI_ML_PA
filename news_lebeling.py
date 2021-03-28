from datetime import date, timedelta
from pandas import DataFrame, read_csv
from pathlib import Path

# Constants
theta = 0.003 # variation threshold to consider the effect as pos/neutral/neg

# news data
news_df = read_csv(Path('../arquivos/BBAS3_prep.csv'), parse_dates=[4])

# price series
price_hist = read_csv(Path('../arquivos/BBAS3_yahoo.csv'), parse_dates=[0])

def label_by_price_trend(news_date: date, prices: DataFrame) -> int:
    """ Indica se apos data de publicação da noticia houve aumento ou diminuição
        significativo no preço da ação

        -1 : Impacto negativo
         0 : Não causou impacto (neutro)
        +1 : Impacto positivo
    """
    date = news_date
    # locate news date in time series
    i = prices.loc[prices['Date'] == str(news_date.date())].index
    while i.size == 0: # dia não util
        date = date + timedelta(days=1)
        i = prices.loc[prices['Date'] == str(date.date())].index


    previous_close = prices['Close'][i[0] - 1]
    news_day_close =  prices['Close'][i[0]]

    # price increase or decrease in %
    delta = (news_day_close - previous_close) / 100
    

    if abs(delta) >= theta:
        return 1 if delta > 0 else -1
    else:
        return 0

news_df['cls_influence'] = news_df['datetime'].apply(label_by_price_trend, args=(price_hist,))

news_df.to_csv(Path('../arquivos/BBAS3_cls.csv'), index=False)