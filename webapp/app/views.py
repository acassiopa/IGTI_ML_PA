import csv
from pathlib import Path

from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    news_data = []
    with open(Path(r'app/static/predictions.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            news_data.append(dict(row))
    return render_template('home.html', news_data=news_data)