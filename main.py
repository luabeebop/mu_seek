from tkinter import filedialog
from tkinter import *
import pygame
import os

root = Tk() #TK is from tkinter
root.title("Mu-seek")
root.geometry("350x450")

pygame.mixer.init() #This is to initialize the pygame mixer

menubar = Menu(root) #This is the menu bar
root.config(menu=menubar) #This is to configure the menu bar

songs = []
current_song = ""
pause = False

def load_music():
    global current_song
    root.directory = filedialog.askdirectory() #This is to open the file dialog

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

# Buttons functionality

def play_music():
    pass

def pause_music():
    pass

def next_music():
    pass

def previous_music():
    pass

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
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0) #This is the play button
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0) #This is the pause button
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0) #This is the next button
previous_btn = Button(control_frame, image=previous_btn_image, borderwidth=0) #This is the previous button

play_btn.grid(row=0, column=1) #This is to place the play button in the frame
pause_btn.grid(row=0, column=2) #This is to place the pause button in the frame
next_btn.grid(row=0, column=3) #This is to place the next button in the frame
previous_btn.grid(row=0, column=0) #This is to place the previous button in the frame

root.mainloop() #This is to keep the window open