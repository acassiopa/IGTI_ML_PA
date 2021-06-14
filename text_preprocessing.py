from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
from nltk import RSLPStemmer
from re import findall, sub

def apply_prep(raw_text: str) -> str:
    raw_text = remove_special_chars(raw_text)
    raw_text = remove_pt_stop_words(raw_text)
    raw_text = tokenize(raw_text)
    raw_text = stemmize(raw_text)
    return ' '.join(raw_text)


def tokenize(text: str) -> list:
    """ Divide the text into token """
    toknzr = WhitespaceTokenizer()
    return toknzr.tokenize(text)

def remove_pt_stop_words(text: str) -> str:
    """ remove stop words from text in portuguese"""
    stop_words = stopwords.words("portuguese")
    no_stop_text = [word for word in text.split() if word not in stop_words]

    return ' '.join(no_stop_text)

def remove_special_chars(text: str) -> str:
    """ Remove punctuation from text """
    clean_text = ' '.join(findall('[\w&$]+', text))
    clean_text = sub('[\d]|R\$|US\$|\$', ' ', clean_text)
    return clean_text

def stemmize(tokens: list) -> list:
    stemmer = RSLPStemmer()
    return [stemmer.stem(tok) for tok in tokens]