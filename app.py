import PySimpleGUI as sg
import sqlite3
import os
import requests
import re
import json
import urllib.request
import sqlite3
from bs4 import BeautifulSoup


def prepare_soup():
    print("Fetching the pre requisites")
    anime_list_path = "https://myanimelist.net/info.php?search=%25%25%25&go=relationids&divname=relationGen1"
    anime_page = urllib.request.urlopen(anime_list_path)
    print("Preparing the soup. This may take a while")
    soup = BeautifulSoup(anime_page,"lxml")
    print("All done")
    return soup


def find_animeid(AnimeName,soup):
    animeid = soup.find("td",text = re.compile("^"+AnimeName+"$",re.I)).find_previous_sibling("td").text
    return animeid


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
    return anime_data

def CreateTables():
    db.execute(''' CREATE TABLE IF NOT EXISTS ANIMES (ID INTEGER PRIMARY KEY,TITLE text,SCORE FLOAT,RATING text,STATUS text,
 POPULARITY integer,EPISODES integer,RANK integer,DURATION text)''')



if __name__=="__main__":
    soup = prepare_soup()
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
    CreateTables()
    animes = next(os.walk(path))[1]
    data = []
    for anime in animes:
        print("Adding ", anime)
        AnimeID = find_animeid(anime,soup)
        data.append(get_anime_data(AnimeID, path))
    print(data)
    header_list = ["MAL ID","TITLE","SCORE","RATING","STATUS","POPULARITY","EPISODES","RANK","DURATION"]
    sg.SetOptions(element_padding=(0, 0))

    layout = [[sg.Table(values=data,
                            headings=header_list,
                            max_col_width=25,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='center',
                            alternating_row_color='lightblue',
                            pad=25,
                            num_rows=min(len(data), 20))]]


    window = sg.Window('Table', grab_anywhere=False).Layout(layout)
    event, values = window.Read()

    sg.Popup("SUCCESSFULLY DONE ! AnimeData.txt created in your anime folder")