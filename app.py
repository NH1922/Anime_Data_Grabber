import PySimpleGUI as sg
import sqlite3
import os
import requests
import re
import bs4
import json
import urllib.request
import sqlite3
import csv 



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
    anime_data = []
    file_destination = path + "\AnimeData.txt"
    file = open(file_destination,"a")
    file.write("MAL ID:" +str(response_data['mal_id'])  +"\n")
    anime_data.append(str(response_data['mal_id']))
    file.write("TITLE:" +str(response_data['title'])  +"\n")
    anime_data.append(str(response_data['title']))
    file.write("SCORE:" +str(response_data['score'])  +"\n")
    anime_data.append(str(response_data['score']))
    file.write("RATING" +str(response_data['rating'])  +"\n")
    anime_data.append(str(response_data['rating']))
    file.write("STATUS:" +str(response_data['status'])  +"\n")
    anime_data.append(str(response_data['status']))
    file.write("POPULARITY:" +str(response_data['popularity'])  +"\n")
    anime_data.append(str(response_data['popularity']))
    file.write("EPISODES:" +str(response_data['episodes'])  +"\n")
    anime_data.append(str(response_data['episodes']))
    file.write("RANK:" +str(response_data['rank'])  +"\n")
    anime_data.append(str(response_data['rank']))
    file.write("DURATION:" +str(response_data['duration'])  +"\n")
    anime_data.append(str(response_data['duration']))
    file.write("GENRE" +str(response_data['genre'])  +"\n")
    file.write("\n ----- END OF "+response_data['title']+"-----\n\n\n")
    response_data = list(response_data.values())
    print(anime_data)
    db.execute('''INSERT INTO ANIMES VALUES(?,?,?,?,?,?,?,?,?)''',tuple(anime_data))
    db.commit()

def create_table():
    db.execute(''' CREATE TABLE IF NOT EXISTS ANIMES (ID INTEGER PRIMARY KEY,TITLE text,SCORE FLOAT,RATING text,STATUS text,
 POPULARITY integer,EPISODES integer,RANK integer,DURATION text)''')

def create_csv(AnimeID,path):
    base_url = "https://api.jikan.moe/anime/"
    request_url = base_url +  str(AnimeID)
    response = urllib.request.urlopen(request_url).read()
    response_obj = str(response,'utf-8')
    response_data = json.loads(response_obj)
    anime_data = []
    file_destination = path + "\AnimeData.csv"
    try:
        csv_file = open(file_destination,"r")
        print("in try block")
    except FileNotFoundError:
        print("In exception block")
        csv_file = open(file_destination,"a")
        headings = ["MAL ID","TITLE","SCORE","RATING","STATUS","POPULARITY","EPISODES","RANK","DURATION"]
        writer = csv.writer(csv_file)
        writer.writerow(headings)
        csv_file.close()
    finally:
        anime_data.append(str(response_data['mal_id']))
        anime_data.append(str(response_data['title']))
        anime_data.append(str(response_data['score']))
        anime_data.append(str(response_data['rating']))
        anime_data.append(str(response_data['status']))
        anime_data.append(str(response_data['popularity']))
        anime_data.append(str(response_data['episodes']))
        anime_data.append(str(response_data['rank']))
        anime_data.append(str(response_data['duration']))
        print(anime_data)
        csv_file = open(file_destination,"a")
        writer = csv.writer(csv_file)
        writer.writerow(anime_data)
        csv_file.close()



if __name__=="__main__":
    db = sqlite3.connect('data/reports')
    layout = [[sg.Text('Choose the animes folder', size=(35, 1))],
              [sg.Text('Anime Folder', size=(15, 1), auto_size_text=False, justification='right'),
               sg.InputText('Source'),
               sg.FolderBrowse()],
              [sg.Submit(), sg.Cancel(), sg.Button('Customized', button_color=('white', 'green'))]]

    event, values = sg.Window('Anime Data Grabber', auto_size_text=True, default_element_size=(40, 1)).Layout(
        layout).Read()
    sg.Text("This is a text",size=(35, 1))
    sg.Popup("The gui returned", values)
    path = values[0]
    create_table()
    animes = next(os.walk(path))[1]
    '''for anime in animes:
        print("Adding ", anime)
        AnimeID = find_animeid(anime)
        get_anime_data(AnimeID, path)'''

    for anime in animes:
        print("Adding ", anime)
        AnimeID = find_animeid(anime)
        create_csv(AnimeID,path)  
    sg.Popup("SUCCESSFULLY DONE ! AnimeData.txt created in your anime folder")