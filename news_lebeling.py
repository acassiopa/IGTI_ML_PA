from datetime import date, timedelta
from pandas import DataFrame, read_csv
from pathlib import Path

# Constants
theta = 0.000 # variation threshold to consider the effect as pos/neutral/neg

# news data
news_df = read_csv(Path('../arquivos/news_data.csv'), parse_dates=[4])
print(news_df.info())

# price series
price_hist = read_csv(Path('../arquivos/series_data.csv'), parse_dates=[0])
print(price_hist.info())

def label_by_price_trend(news_data: DataFrame, prices: DataFrame) -> list:
    """ Indica se apos data de publicação da noticia houve aumento ou diminuição
        significativo no preço da ação

        -1 : Impacto negativo
         0 : Não causou impacto (neutro)
        +1 : Impacto positivo
    """
    classification = []
    print(news_data.head())
    for _, row in news_data.iterrows():
        date = row['datetime'].date()
        # locate news date in time series
        i = prices.loc[(prices['Date'] == str(date)) & (prices['Code'] == row['code'])].index
        while i.size == 0: # not work day
            date = date + timedelta(days=1)
            i = prices.loc[prices['Date'] == str(date)].index

        previous_close = prices['Close'][i[0] - 1]
        news_day_close =  prices['Close'][i[0]]

        # price increase or decrease in %
        delta = (news_day_close - previous_close) / 100

        if abs(delta) >= theta:
            classification.append(1) if delta > 0 else classification.append(-1)
        else:
            classification.append(0)
        
    return classification

classification = label_by_price_trend(news_df, price_hist)
news_df['cls_influence'] = classification
# news_df['cls_influence'] = news_df.apply(label_by_price_trend, args=(price_hist,), axis=1)

news_df.to_csv(Path('../arquivos/news_data_CLS.csv'), index=False)