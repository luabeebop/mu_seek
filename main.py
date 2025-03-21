from tkinter import filedialog #This is to import the file dialog
from tkinter import * #This is to import everything from tkinter
import pygame #This is to import the pygame module
import os #This is to import the os module

root = Tk() #TK is from tkinter
root.title("Mu-seek") #This is to set the title of the window
root.geometry("350x450") #This is to set the size of the window

pygame.mixer.init() #This is to initialize the pygame mixer

menubar = Menu(root) #This is the menu bar
root.config(menu=menubar) #This is to configure the menu bar

songs = [] #This is the list of songs
current_song = "" #This is the current song
pause = False #This is the current state of the music

def load_music(): #This is to load the music
    global current_song #This is to access the current song variable
    root.directory = filedialog.askdirectory() #This is to open the file dialog

    for song in os.listdir(root.directory): #This is to loop through the files in the directory
        name, ext = os.path.splitext(song) #This is to get the name and extension of the file
        if ext == ".mp3": #This is to check if the file is an mp3 file
            songs.append(song) #This is to add the song to the list of songs

    for song in songs: #This is to loop through the songs
        songlist.insert("end", song) #This is to insert the song into the songlist

    songlist.selection_set(0) #This is to select the first song in the list
    current_song = songs[songlist.curselection()[0]] #This is to get the current song

# Buttons functionality

def play_music(): #This is to play the music
    pass #This is to pass the function

def pause_music(): #This is to pause the music
    pass #This is to pass the function

def next_music(): #This is to play the next music
    pass #This is to pass the function

def previous_music(): #This is to play the previous music
    pass #This is to pass the function

organize_menu = Menu(menubar, tearoff=False) #This is the organize menu
menubar.add_cascade(label="Selection", menu=organize_menu) #This is to add the organize menu to the menu bar
organize_menu.add_command(label="Select Folder", command=load_music) #This is to add the select folder option to the organize menu
songlist = Listbox(root, bg="black", fg="white", width=60, height=20) #This is the songlist box where the songs will be displayed
songlist.pack() 

play_btn_image = PhotoImage(file="play.png") #This is to load the play button image
pause_btn_image = PhotoImage(file="pause.png") #This is to load the pause button image
next_btn_image = PhotoImage(file="next.png") #This is to load the next button image
previous_btn_image = PhotoImage(file="previous.png") #This is to load the previous button image

control_frame = Frame(root) #This is the frame for the control buttons
control_frame.pack() #This is to pack the control frame

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0) #This is the play button
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0) #This is the pause button
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0) #This is the next button
previous_btn = Button(control_frame, image=previous_btn_image, borderwidth=0) #This is the previous button

play_btn.grid(row=0, column=1) #This is to place the play button in the frame
pause_btn.grid(row=0, column=2) #This is to place the pause button in the frame
next_btn.grid(row=0, column=3) #This is to place the next button in the frame
previous_btn.grid(row=0, column=0) #This is to place the previous button in the frame

root.mainloop() #This is to keep the window open