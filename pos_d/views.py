from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Create your views here.
def index(request):
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
