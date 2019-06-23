
# MAL-FO
Fetches information about all your anime stored in a folder from [MAL](https://myanimelist.net/) automatically, stores the information in a local DB (sqllite3) and a text file. 

MAL-FO uses PySimpleGui to provide a simple GUI to browse the folders and display the results in a table.  [Jikan API](https://jikan.moe/) is used to fetch the information about anime using their MAL ID. To fetch the MAL ID, [MAL page](https://myanimelist.net/info.php?search=%25%25%25&go=relationids&divname=relationGen1) containing all anime and their ID is parsed using Beautiful Soup. 


## Requirements 

1. Python 3.5.2 +
2. Other requirements in requirements.txt
(```pip install -r requirements.txt```)

## To Do 
 - [x] Database integration
 - [x] Storing results in a file 
 - [x] Displaying results through a GUI 
 - [x] Parsing for Anime ID from live site data 
-  [ ] Improved GUI with better menus
- [ ] Additional features like downloading subs (suggestions needed) 
- [ ]  Faster parsing to find the Anime ID

Any suggestions and improvements are welcome :) 