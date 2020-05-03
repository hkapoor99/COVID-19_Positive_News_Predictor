from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.models import load_model
from keras.models import model_from_json
from keras.backend import clear_session
import pandas as pd

# Create your views here.
def index(request):
    with open('models/tokenizer_c.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    json_file_c = open('models/lstm_model_c.json', 'r')
    loaded_model_json_c = json_file_c.read()
    json_file_c.close()
    loaded_model_c = model_from_json(loaded_model_json_c)
    loaded_model_c.load_weights("models/lstm_model_c.h5")

    json_file_s = open('models/lstm_model_s.json', 'r')
    loaded_model_json_s = json_file_s.read()
    json_file_s.close()
    loaded_model_s = model_from_json(loaded_model_json_s)
    loaded_model_s.load_weights("models/lstm_model_s.h5")

    headlines = []
    dates = []
    imageurls = []
    descriptions = []
    sources = []

    url = 'https://inshorts.com/en/read/national'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html5lib")
    for i in soup.find_all("div", {"class": "news-card z-depth-1"}):
        t = i.find("span", {"itemprop": "headline"}).text + " " + i.find("div", {"itemprop": "articleBody"}).text
        text = [t]
        twt = tokenizer.texts_to_sequences(text)
        twt = pad_sequences(twt, maxlen=86, dtype='int32', value=0)
        sentiment_c = loaded_model_c.predict(twt, batch_size=1, verbose=2)[0]
        sentiment_s = loaded_model_s.predict(twt, batch_size=1, verbose=2)[0]
        if sentiment_c[1] > 0.5 and sentiment_s[1]>0.8:
            headlines.append(i.find("span", {"itemprop": "headline"}).text)
            dates.append(i.find("span", {"clas": "date"}).text)
            imageurls.append(i.find("div", {"class": "news-card-image"}).get("style").replace("background-image: url(\'", "").replace("?\')", ""))
            descriptions.append(i.find("div", {"itemprop": "articleBody"}).text)
            if i.find("a", {"class": "source"}) is None:
                sources.append("www.covid-positive-news.herokuapp.com")
            else:
                sources.append(i.find("a", {"class": "source"}).get("href"))
        else:
            continue;

    context = {
        "Headlines" : headlines,
        "Descriptions" : descriptions,
        "BottomTexts" : sources,
        "ImageURLs": imageurls,
        "Dates" : dates
    }

    return render(request, "pos_d/index.html", context)


def sevendays(request):
    with open('models/tokenizer_c.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    json_file_c = open('models/lstm_model_c.json', 'r')
    loaded_model_json_c = json_file_c.read()
    json_file_c.close()
    loaded_model_c = model_from_json(loaded_model_json_c)
    loaded_model_c.load_weights("models/lstm_model_c.h5")

    json_file_s = open('models/lstm_model_s.json', 'r')
    loaded_model_json_s = json_file_s.read()
    json_file_s.close()
    loaded_model_s = model_from_json(loaded_model_json_s)
    loaded_model_s.load_weights("models/lstm_model_s.h5")

    headlines = []
    dates = []
    imageurls = []
    descriptions = []
    sources = []

    data = pd.read_csv("models/data_30.csv")
    date2 = []
    for i in data["Date"]:
        date2.append(datetime.strptime(i, '%Y-%m-%d').date())
    data["Date"] = date2
    data_30 = data.loc[data["Date"] >= (datetime.now().date() - timedelta(days=7))]

    for i, row  in data_30.iterrows() :
        t = row["Text"]
        text = [t]
        twt = tokenizer.texts_to_sequences(text)
        twt = pad_sequences(twt, maxlen=86, dtype='int32', value=0)
        sentiment_c = loaded_model_c.predict(twt, batch_size=1, verbose=2)[0]
        sentiment_s = loaded_model_s.predict(twt, batch_size=1, verbose=2)[0]
        if sentiment_c[1] > 0.5 and sentiment_s[1]>0.8:
            headlines.append(row["Headline"])
            dates.append(row["Date"])
            imageurls.append(row["Image"])
            descriptions.append(row["Description"])
            sources.append(row["Source"])
        else:
            continue;

    context = {
        "Headlines" : headlines,
        "Descriptions" : descriptions,
        "BottomTexts" : sources,
        "ImageURLs": imageurls,
        "Dates" : dates
    }
    return render(request, "pos_d/7days.html", context)

def thirtydays(request):
    with open('models/tokenizer_c.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    json_file_c = open('models/lstm_model_c.json', 'r')
    loaded_model_json_c = json_file_c.read()
    json_file_c.close()
    loaded_model_c = model_from_json(loaded_model_json_c)
    loaded_model_c.load_weights("models/lstm_model_c.h5")

    json_file_s = open('models/lstm_model_s.json', 'r')
    loaded_model_json_s = json_file_s.read()
    json_file_s.close()
    loaded_model_s = model_from_json(loaded_model_json_s)
    loaded_model_s.load_weights("models/lstm_model_s.h5")

    headlines = []
    dates = []
    imageurls = []
    descriptions = []
    sources = []

    data = pd.read_csv("models/data_30.csv")
    date2 = []
    for i in data["Date"]:
        date2.append(datetime.strptime(i, '%Y-%m-%d').date())
    data["Date"] = date2
    data_7 = data.loc[data["Date"] >= (datetime.now().date() - timedelta(days=30))]

    for i, row  in data_7.iterrows() :
        t = row["Text"]
        text = [t]
        twt = tokenizer.texts_to_sequences(text)
        twt = pad_sequences(twt, maxlen=86, dtype='int32', value=0)
        sentiment_c = loaded_model_c.predict(twt, batch_size=1, verbose=2)[0]
        sentiment_s = loaded_model_s.predict(twt, batch_size=1, verbose=2)[0]
        if sentiment_c[1] > 0.5 and sentiment_s[1]>0.8:
            headlines.append(row["Headline"])
            dates.append(row["Date"])
            imageurls.append(row["Image"])
            descriptions.append(row["Description"])
            sources.append(row["Source"])
        else:
            continue;

    context = {
        "Headlines" : headlines,
        "Descriptions" : descriptions,
        "BottomTexts" : sources,
        "ImageURLs": imageurls,
        "Dates" : dates
    }
    return render(request, "pos_d/30days.html", context)

def about(request):
    return render(request, "pos_d/about.html")
