from pathlib import Path
from pickle import load
from soup_parsers import *
from text_preprocessing import apply_prep
from pandas import DataFrame

with open(Path(r'..\arquivos\urls.txt'), 'r') as urls_file:
    code_url_list = urls_file.read().split('\n')

# parse all urls
for code_url in code_url_list:
    code, url = code_url.split(';')
    if   'g1.globo.com' in url:
        parser = G1Parser([url], code)
    elif 'infomoney.com' in url:
        parser = InfoMoneyParser([url], code)
    elif 'investing.com' in url:
        parser = InvestingParser([url], code)
    elif 'moneytimes.com' in url:
        parser = MoneyTimesParser([url], code)
    elif 'suno.com' in url:
        parser = SunoParser([url], code)
    elif 'uol.com' in url:
        parser = UOLParser([url], code)

    parser.parse()

df = DataFrame(parser.news_array)
df['prep_text'] = df['raw_text'].apply(apply_prep)

# load all pickles
with open(Path(r'BBAS3_tfidf'), 'rb') as f:
    BBAS3_tfidf = load(f)
with open(Path(r'BBDC4_tfidf'), 'rb') as f:
    BBDC4_tfidf = load(f)
with open(Path(r'CSNA3_tfidf'), 'rb') as f:
    CSNA3_tfidf = load(f)
with open(Path(r'PETR4_tfidf'), 'rb') as f:
    PETR4_tfidf = load(f)
with open(Path(r'VALE3_tfidf'), 'rb') as f:
    VALE3_tfidf = load(f)
with open(Path(r'VVAR3_tfidf'), 'rb') as f:
    VVAR3_tfidf = load(f)

with open(Path(r'BBAS3_pickle'), 'rb') as f:
    BBAS3_model = load(f)
with open(Path(r'BBDC4_pickle'), 'rb') as f:
    BBDC4_model = load(f)
with open(Path(r'CSNA3_pickle'), 'rb') as f:
    CSNA3_model = load(f)
with open(Path(r'PETR4_pickle'), 'rb') as f:
    PETR4_model = load(f)
with open(Path(r'VALE3_pickle'), 'rb') as f:
    VALE3_model = load(f)
with open(Path(r'VVAR3_pickle'), 'rb') as f:
    VVAR3_model = load(f)

def predict(tfidf, model, prep_text):
    t = tfidf.transform(prep_text)
    p = model.predict(t)
    return p[0]

# predictions
pred = []
for i, row in df.iterrows():
    if   row['code'] == 'BBAS3':
        pred.append(predict(BBAS3_tfidf, BBAS3_model, [row['prep_text']]))
    elif row['code'] == 'BBDC4':
        pred.append(predict(BBDC4_tfidf, BBDC4_model, [row['prep_text']]))
    elif row['code'] == 'CSNA3':
        pred.append(predict(CSNA3_tfidf, CSNA3_model, [row['prep_text']]))
    elif row['code'] == 'PETR4':
        pred.append(predict(PETR4_tfidf, PETR4_model, [row['prep_text']]))
    elif row['code'] == 'VALE3':
        pred.append(predict(VALE3_tfidf, VALE3_model, [row['prep_text']]))
    elif row['code'] == 'VVAR3':
        pred.append(predict(VVAR3_tfidf, VVAR3_model, [row['prep_text']]))

df['pred'] = pred
webapp_df = df[['code', 'source', 'url', 'title', 'datetime', 'pred']]
webapp_df.to_csv('predictions.csv', index=False)