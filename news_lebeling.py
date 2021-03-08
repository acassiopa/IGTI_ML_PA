from datetime import date, timedelta
from pandas import DataFrame, read_csv, DatetimeIndex
from pathlib import Path

# Obtem dados de notícias
news_df = read_csv(Path('../arquivos/mongo_export.csv'), parse_dates=[5])

# Obtem séries temporais de preço por empresa
price_hist = read_csv(Path('../arquivos/BBAS3.SA.csv'), parse_dates=[0])
# price_hist.set_index(DatetimeIndex(price_hist['Date']), inplace=True)

def label_by_price_trend(news_date: date, prices: DataFrame) -> int:
    """ Indica se apos data de publicação da noticia houve aumento ou diminuição
        significativo no preço da ação

        -1 : Impacto negativo
         0 : Não causou impacto (neutro)
        +1 : Impacto positivo
    """
    # Constants
    theta = 0.02 # variation threshold to consider the effect as pos/neutral/neg
    future_amount = 3 # amount of days into the future to consider

    i = prices.loc[prices['Date'] == str(news_date.date())].index
    while i.size == 0: # dia não util
        date = date + timedelta(days=1)
        i = prices.loc[prices['Date'] == str(date.date())].index


    current_value = prices['Close'][i]
    future_value =  prices['Close'][i+future_amount]

    # price increase or decrease in %
    delta = (future_value - current_value) / 100
    

    if abs(delta) >= theta:
        return 1 if delta > 0 else -1
    else:
        return 0

news_df['cls_influence'] = news_df['datetime'].apply(label_by_price_trend, args=(price_hist,))

news_df.to_csv(Path('../arquivos/news_data_cls.csv'))