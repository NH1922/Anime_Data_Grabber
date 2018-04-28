from xml.etree import ElementTree
import os
import requests
import re
import bs4
import json
import urllib.request

def find_animeid(AnimeName):
    AnimeName = AnimeName.replace(" ","_")
    file = open('data/anime.xml','r',encoding='utf-8')
    contents  = file.read()
    soup = bs4.BeautifulSoup(contents,'lxml')
    #links  = soup.find_all('url')
    links = soup.find(string = re.compile(AnimeName,re.IGNORECASE))
    data = links.split("/")
    return(data[4])

def get_anime_data(AnimeID):
    base_url = "https://api.jikan.moe/anime/"
    request_url = base_url +  str(AnimeID)
    response = urllib.request.urlopen(request_url).read()
    response_obj = str(response,'utf-8')
    response_data = json.loads(response_obj)
    print(response_data['mal_id'])
    print(response_data['title_english'])
    #print(response_data['title_japanese'])
    print(response_data['score'])
    print(response_data['rating'])
    print(response_data['status'])
    print(response_data['popularity'])
    print(response_data['episodes'])
    print(response_data['rank'])
    print(response_data['title'])
    print(response_data['duration'])
    print(response_data['genre'])





if __name__=="__main__":
    path = input("Enter the path to your animes : ")
    animes = next(os.walk(path))[1]
    for anime in animes:
        AnimeID = find_animeid(anime)
        get_anime_data(AnimeID)
