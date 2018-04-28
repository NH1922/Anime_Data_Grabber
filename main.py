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

def get_anime_data(AnimeID,path):
    base_url = "https://api.jikan.moe/anime/"
    request_url = base_url +  str(AnimeID)
    response = urllib.request.urlopen(request_url).read()
    response_obj = str(response,'utf-8')
    response_data = json.loads(response_obj)
    file_destination = path + "\AnimeData.txt"
    file = open(file_destination,"a")
    file.write("MAL ID:" +str(response_data['mal_id'])  +"\n")
    file.write("TITLE:" +str(response_data['title'])  +"\n")
    file.write("SCORE:" +str(response_data['score'])  +"\n")
    file.write("RATING" +str(response_data['rating'])  +"\n")
    file.write("STATUS:" +str(response_data['status'])  +"\n")
    file.write("POPULARITY:" +str(response_data['popularity'])  +"\n")
    file.write("EPISODES:" +str(response_data['episodes'])  +"\n")
    file.write("RANK:" +str(response_data['rank'])  +"\n")
    file.write("DURATION:" +str(response_data['duration'])  +"\n")
    file.write("GENRE" +str(response_data['genre'])  +"\n")
    file.write("MAL ID:" +str(response_data['mal_id'])  +"\n")
    file.write("\n ----- END OF "+response_data['title']+"-----\n\n\n")

if __name__=="__main__":
    path = input("Enter the path to your animes : ")
    animes = next(os.walk(path))[1]
    for anime in animes:
        print("Adding ",anime)
        AnimeID = find_animeid(anime)
        get_anime_data(AnimeID,path)
    print("SUCCESSFULLY DONE ! AnimeData.txt created in your anime folder")
