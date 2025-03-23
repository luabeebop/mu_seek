from tkinter import filedialog
from tkinter import *
import pygame
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Spotify API credentials
SPOTIFY_CLIENT_ID = 'hell naw ofc i wont show it'
SPOTIFY_CLIENT_SECRET = 'hell naw ofc i wont show it'
REDIRECT_URI = 'http://localhost:8888/callback'  
SCOPE = "user-library-read user-read-playback-state user-modify-playback-state playlist-read-private"

root = Tk()
root.title("Mu-seek with Spotify")
root.geometry("500x600")
root.configure(bg="#121212")  # Spotify's dark background color

pygame.mixer.init()

# Initialize Spotify API client
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotifycache"
    ))
    spotify_connected = True
except Exception as e:
    print(f"Spotify connection error: {e}")
    spotify_connected = False

# Global variables
songs = []  # Local songs
spotify_playlists = []  # Spotify playlists
spotify_tracks = []  # Tracks in selected playlist
current_song = ""
paused = False
is_spotify_playing = False  # Flag to know if we're playing Spotify or local music

# Create custom style elements
title_label = Label(root, text="Mu-seek", font=("Helvetica", 24, "bold"), fg="#1DB954", bg="#121212")
title_label.pack(pady=10)

# Create tabs for Local and Spotify music
notebook = Frame(root, bg="#121212")
notebook.pack(pady=10, fill=BOTH, expand=True)

# Tab buttons
tab_frame = Frame(notebook, bg="#121212")
tab_frame.pack(fill=X)

def switch_to_local():
    spotify_frame.pack_forget()
    local_frame.pack(fill=BOTH, expand=True)
    local_btn.config(bg="#1DB954", fg="#121212")
    spotify_btn.config(bg="#333333", fg="white")

def switch_to_spotify():
    if not spotify_connected:
        messagebox.showerror("Connection Error", "Spotify is not connected. Please check your credentials.")
        return
    local_frame.pack_forget()
    spotify_frame.pack(fill=BOTH, expand=True)
    spotify_btn.config(bg="#1DB954", fg="#121212")
    local_btn.config(bg="#333333", fg="white")
    load_spotify_playlists()  # Load playlists when switching to Spotify tab

local_btn = Button(tab_frame, text="Local Music", command=switch_to_local, bg="#1DB954", fg="#121212", padx=10, relief=FLAT)
spotify_btn = Button(tab_frame, text="Spotify", command=switch_to_spotify, bg="#333333", fg="white", padx=10, relief=FLAT)
local_btn.pack(side=LEFT, padx=5, pady=5)
spotify_btn.pack(side=LEFT, padx=5, pady=5)

# Local music frame
local_frame = Frame(notebook, bg="#121212")
local_frame.pack(fill=BOTH, expand=True)

# Spotify frame
spotify_frame = Frame(notebook, bg="#121212")

# Functions for local music
def load_music():
    global current_song
    root.directory = filedialog.askdirectory()

    songs.clear()
    songlist.delete(0, END)

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    if songs:
        songlist.selection_set(0)
        current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused, is_spotify_playing
    
    # Stop Spotify if it's playing
    if is_spotify_playing:
        sp.pause_playback()
        is_spotify_playing = False
    
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False
    
    update_now_playing_info(current_song)

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    
    try:
        songlist.selection_clear(0, "end")
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def previous_music():
    global current_song, paused
    
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

# Spotify functions
def load_spotify_playlists():
    playlist_list.delete(0, END)
    try:
        playlists = sp.current_user_playlists()
        spotify_playlists.clear()
        
        for i, playlist in enumerate(playlists['items']):
            playlist_list.insert(END, playlist['name'])
            spotify_playlists.append({
                'name': playlist['name'],
                'id': playlist['id']
            })
    except Exception as e:
        messagebox.showerror("Spotify Error", f"Error loading playlists: {e}")

def on_playlist_select(event):
    selection = playlist_list.curselection()
    if not selection:
        return
    
    track_list.delete(0, END)
    spotify_tracks.clear()
    
    playlist_id = spotify_playlists[selection[0]]['id']
    try:
        results = sp.playlist_tracks(playlist_id)
        for i, item in enumerate(results['items']):
            track = item['track']
            artist = track['artists'][0]['name']
            track_name = track['name']
            display_name = f"{artist} - {track_name}"
            
            track_list.insert(END, display_name)
            spotify_tracks.append({
                'name': display_name,
                'uri': track['uri'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
    except Exception as e:
        messagebox.showerror("Spotify Error", f"Error loading tracks: {e}")

def play_spotify_track():
    global is_spotify_playing
    selection = track_list.curselection()
    if not selection:
        return
    
    # Stop local music if it's playing
    pygame.mixer.music.stop()
    
    track_uri = spotify_tracks[selection[0]]['uri']
    track_name = spotify_tracks[selection[0]]['name']
    try:
        sp.start_playback(uris=[track_uri])
        is_spotify_playing = True
        update_now_playing_info(track_name, spotify_tracks[selection[0]]['image_url'])
    except Exception as e:
        messagebox.showerror("Spotify Error", f"Error playing track: {e}")

def pause_spotify():
    global is_spotify_playing
    try:
        sp.pause_playback()
        is_spotify_playing = False
    except Exception as e:
        messagebox.showerror("Spotify Error", f"Error pausing: {e}")

def next_spotify():
    try:
        sp.next_track()
        # Update selection in the list
        update_current_playing_track()
    except Exception as e:
        messagebox.showerror("Spotify Error", f"Error skipping track: {e}")

def previous_spotify():
    try:
        sp.previous_track()
        # Update selection in the list
        update_current_playing_track()
    except Exception as e:
        messagebox.showerror("Spotify Error", f"Error going to previous track: {e}")

def update_current_playing_track():
    # This would ideally update the UI to reflect the currently playing track
    try:
        current = sp.current_playback()
        if current and current['item']:
            track_name = current['item']['name']
            artist = current['item']['artists'][0]['name']
            display_name = f"{artist} - {track_name}"
            
            # Find and select this track in the list
            for i, track in enumerate(spotify_tracks):
                if track['uri'] == current['item']['uri']:
                    track_list.selection_clear(0, END)
                    track_list.selection_set(i)
                    track_list.see(i)
                    update_now_playing_info(display_name, current['item']['album']['images'][0]['url'])
                    break
    except Exception as e:
        print(f"Error updating current track: {e}")

def update_now_playing_info(song_name, image_url=None):
    now_playing_label.config(text=f"Now Playing: {song_name}")
    
    # Update album art if available
    if image_url:
        try:
            response = requests.get(image_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            album_art_label.config(image=photo)
            album_art_label.image = photo  # Keep a reference
        except Exception as e:
            print(f"Error loading album art: {e}")
    else:
        # Reset to default image or clear
        album_art_label.config(image="")

# Local music UI components
songlist_frame = Frame(local_frame, bg="#121212")
songlist_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

songlist = Listbox(songlist_frame, bg="#333333", fg="white", width=50, height=15, selectbackground="#1DB954")
songlist.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(songlist_frame)
scrollbar.pack(side=RIGHT, fill=Y)
songlist.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=songlist.yview)

# Spotify UI components
spotify_main_frame = Frame(spotify_frame, bg="#121212")
spotify_main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

playlist_frame = Frame(spotify_main_frame, bg="#121212")
playlist_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

playlist_label = Label(playlist_frame, text="Your Playlists", bg="#121212", fg="white")
playlist_label.pack()

playlist_list = Listbox(playlist_frame, bg="#333333", fg="white", selectbackground="#1DB954", height=15)
playlist_list.pack(fill=BOTH, expand=True)
playlist_list.bind('<<ListboxSelect>>', on_playlist_select)

playlist_scrollbar = Scrollbar(playlist_frame)
playlist_scrollbar.pack(side=RIGHT, fill=Y)
playlist_list.config(yscrollcommand=playlist_scrollbar.set)
playlist_scrollbar.config(command=playlist_list.yview)

track_frame = Frame(spotify_main_frame, bg="#121212")
track_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

track_label = Label(track_frame, text="Tracks", bg="#121212", fg="white")
track_label.pack()

track_list = Listbox(track_frame, bg="#333333", fg="white", selectbackground="#1DB954", height=15)
track_list.pack(fill=BOTH, expand=True)

track_scrollbar = Scrollbar(track_frame)
track_scrollbar.pack(side=RIGHT, fill=Y)
track_list.config(yscrollcommand=track_scrollbar.set)
track_scrollbar.config(command=track_list.yview)

# Now playing section
now_playing_frame = Frame(root, bg="#121212", height=100)
now_playing_frame.pack(fill=X, padx=10, pady=5)

album_art_label = Label(now_playing_frame, bg="#121212")
album_art_label.pack(side=LEFT, padx=10)

now_playing_label = Label(now_playing_frame, text="Not Playing", bg="#121212", fg="white", font=("Helvetica", 10))
now_playing_label.pack(side=LEFT, padx=10)

# Control buttons
control_frame = Frame(root, bg="#121212")
control_frame.pack(pady=10)

# Try to load button images or use text buttons if images aren't available
try:
    play_btn_image = PhotoImage(file="play.png")
    pause_btn_image = PhotoImage(file="pause.png")
    next_btn_image = PhotoImage(file="next.png")
    previous_btn_image = PhotoImage(file="previous.png")
    
    play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, bg="#121212", 
                      activebackground="#121212", command=lambda: play_music() if not is_spotify_playing else play_spotify_track())
    pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, bg="#121212", 
                      activebackground="#121212", command=lambda: pause_music() if not is_spotify_playing else pause_spotify())
    next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, bg="#121212", 
                      activebackground="#121212", command=lambda: next_music() if not is_spotify_playing else next_spotify())
    previous_btn = Button(control_frame, image=previous_btn_image, borderwidth=0, bg="#121212", 
                      activebackground="#121212", command=lambda: previous_music() if not is_spotify_playing else previous_spotify())
except:
    # Text buttons as fallback
    play_btn = Button(control_frame, text="▶", font=("Helvetica", 16), bg="#333333", fg="white", 
                     command=lambda: play_music() if not is_spotify_playing else play_spotify_track())
    pause_btn = Button(control_frame, text="⏸", font=("Helvetica", 16), bg="#333333", fg="white", 
                     command=lambda: pause_music() if not is_spotify_playing else pause_spotify())
    next_btn = Button(control_frame, text="⏭", font=("Helvetica", 16), bg="#333333", fg="white", 
                     command=lambda: next_music() if not is_spotify_playing else next_spotify())
    previous_btn = Button(control_frame, text="⏮", font=("Helvetica", 16), bg="#333333", fg="white", 
                     command=lambda: previous_music() if not is_spotify_playing else previous_spotify())

previous_btn.grid(row=0, column=0, padx=5)
play_btn.grid(row=0, column=1, padx=5)
pause_btn.grid(row=0, column=2, padx=5)
next_btn.grid(row=0, column=3, padx=5)

# Menu
menubar = Menu(root)
root.config(menu=menubar)

organize_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Selection", menu=organize_menu)
organize_menu.add_command(label="Select Folder", command=load_music)
organize_menu.add_command(label="Refresh Spotify Playlists", command=load_spotify_playlists)

# Start with local music tab active
switch_to_local()

# Start the app
root.mainloop()