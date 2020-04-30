from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.models import load_model
from keras.models import model_from_json

# Create your views here.
def index(request):
    with open('models/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    json_file = open('models/lstm_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("models/lstm_model.h5")
    headlines = []
    dates = []
    imageurls = []
    descriptions = []
    sources = []

    url = 'https://inshorts.com/en/read/national'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html5lib")
    for i in soup.find_all("div", {"class": "news-card z-depth-1"}):
        headline = i.find("span", {"itemprop": "headline"}).text
        text = [headline]
        twt = tokenizer.texts_to_sequences(text)
        twt = pad_sequences(twt, maxlen=19, dtype='int32', value=0)
        sentiment = loaded_model.predict(twt, batch_size=1, verbose=2)[0]
        if sentiment[1] > 0.5 :
            headlines.append(i.find("span", {"itemprop": "headline"}).text)
            dates.append(i.find("span", {"clas": "date"}).text)
            imageurls.append(i.find("div", {"class": "news-card-image"}).get("style").replace("background-image: url(\'", "").replace("?\')", ""))
            descriptions.append(i.find("div", {"itemprop": "articleBody"}).text)
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
    url = 'https://inshorts.com/en/read/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    headline = []
    date = []
    imageurl = []
    description = []
    source = []
    for i in soup.find_all("span", {"itemprop": "headline"}):
        headline.append(i.text)
    for i in soup.find_all("span", {"clas": "date"}):
        date.append(i.text)
    for i in soup.find_all("div", {"class": "news-card-image"}):
        url = i.get("style").replace("background-image: url(\'", "")
        url = url.replace("?\')", "")
        imageurl.append(url)
    for i in soup.find_all("div", {"itemprop": "articleBody"}):
        description.append(i.text)
    for i in soup.find_all("a", {"class": "source"}):
        source.append(i.get("href"))

    context = {
        "Headlines" : headline,
        "Descriptions" : description,
        "BottomTexts" : source,
        "ImageURLs": imageurl,
        "Dates" : date
    }
    return render(request, "pos_d/7days.html", context)

def thirtydays(request):
    url = 'https://inshorts.com/en/read/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    headline = []
    date = []
    imageurl = []
    description = []
    source = []
    for i in soup.find_all("span", {"itemprop": "headline"}):
        headline.append(i.text)
    for i in soup.find_all("span", {"clas": "date"}):
        date.append(i.text)
    for i in soup.find_all("div", {"class": "news-card-image"}):
        url = i.get("style").replace("background-image: url(\'", "")
        url = url.replace("?\')", "")
        imageurl.append(url)
    for i in soup.find_all("div", {"itemprop": "articleBody"}):
        description.append(i.text)
    for i in soup.find_all("a", {"class": "source"}):
        source.append(i.get("href"))

    context = {
        "Headlines" : headline,
        "Descriptions" : description,
        "BottomTexts" : source,
        "ImageURLs": imageurl,
        "Dates" : date
    }
    return render(request, "pos_d/30days.html", context)

def about(request):
    return render(request, "pos_d/about.html")
