import PySimpleGUI as sg

layout = [[sg.Text('Choose the animes folder', size=(35, 1))],
[sg.Text('Anime Folder', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Source'),
 sg.FolderBrowse()],
[sg.Submit(), sg.Cancel(), sg.Button('Customized', button_color=('white', 'green'))]]

event, values  = sg.Window('Anime Data Grabber', auto_size_text=True, default_element_size=(40, 1)).Layout(layout).Read()
sg.Popup("The gui returned",values)


