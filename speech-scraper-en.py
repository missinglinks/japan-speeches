import requests
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = "https://japan.kantei.go.jp"

def get_index_pages():
    """ return all index pages of speeches and statements from prime minister abe """
    r = requests.get("https://japan.kantei.go.jp/97_abe/statement/201709/index.html")
    soup = BeautifulSoup(r.text, "html.parser")
    
    links = []

    for list_archive in soup.findAll("dl", {"class": "list-archives"}):
        for link in list_archive.findAll("a"):
            links.append(link["href"])

    return links

def get_speech_text(slug):
    r = requests.get(BASE_URL+slug)
    soup = BeautifulSoup(r.text, "html.parser")  
    speech = soup.find("div", {"id": "format"})
    return speech.text

def scrape_speeches(index_page, directory="output"):
    """ scrapes all speeches in index page and writes them to the output directory """
    if not os.path.exists(directory):
        os.makedirs(directory)

    r = requests.get(BASE_URL+index_page)
    soup = BeautifulSoup(r.text, "html.parser")    

    speech_list = soup.find("ul", {"class", "icolistA"})

    for li in speech_list.findAll("li"):
        title, date_str = li.text.split("[")
        link = li.find("a")["href"]
        link = link.replace("//japan.kantei.go.jp","")
        date = datetime.strptime(date_str, "%B %d, %Y]").isoformat()
        text = get_speech_text(link)

        data = {
            "title": title,
            "date": date,
            "text": text
        }

        filename = directory+"/"+date+"-"+title[:50]+".json"
        with open(filename,"w") as f:
            json.dump(data, f)

        print("scraping ... {}".format(title))



if __name__ == "__main__":
    links = get_index_pages()
    for link in links:
        scrape_speeches(link)