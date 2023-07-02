import vlc
import time
import random
import os
import threading
import tkinter as tk
import urllib.parse
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from tkinter import messagebox
from mutagen.mp3 import MP3
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import yt_dlp
from moviepy.editor import *


class MusicPlayer:
    def __init__(self, music_folder, categories):
        self.music_folder = music_folder
        self.categories = categories
        self.files = {}
        self.queue = []

        self.player = vlc.MediaListPlayer()

        self._load_files()

        self.initUI()

    def initUI(self):
        self.root = tk.Tk()
        self.root.geometry("1050x600")
        self.root.title("MediaOpen 🎵")
        self.root.configure(bg="lightgrey")

        category_frame = tk.Frame(self.root, bg="lightgrey")
        category_frame.pack(side="top", fill="x")

        self.category_label = tk.Label(
            category_frame,
            text="Type of musician:",
            font=("Ink Draft", 30),
            bg="lightgrey",
        )
        self.category_label.pack(side="top", padx=5)

        for category in self.categories:
            button = tk.Button(category_frame, text=category, bg="lightgreen")
            button.pack(side="left", padx=5)
            button.bind("<Button-1>", lambda event, cat=category: self.show_songs(cat))

        button_frame = tk.Frame(self.root, bg="lightgrey")
        button_frame.pack(side="top")

        self.play_button = tk.Button(
            button_frame,
            text="Play▶",
            command=self.play_music,
            width=8,
            height=2,
            bg="lightgreen",
        )
        self.play_button.pack(side="left", padx=8, pady=100)
        self.pause_button = tk.Button(
            button_frame,
            text="Pause⏸",
            command=self.pause_music,
            width=8,
            height=2,
            bg="lightgreen",
        )
        self.pause_button.pack(side="left", padx=8)
        self.pause_button = tk.Button(
            button_frame,
            text="Resume⏯",
            command=self.unpause_music,
            width=8,
            height=2,
            bg="lightgreen",
        )
        self.pause_button.pack(side="left", padx=8)
        self.stop_button = tk.Button(
            button_frame,
            text="End✖️",
            command=self.stop_music,
            width=8,
            height=2,
            bg="lightgreen",
        )
        self.stop_button.pack(side="left", padx=8)

        queue_buttons_frame = tk.Frame(self.root, bg="lightgrey")
        queue_buttons_frame.pack(side="top", pady=10)

        self.play_queue_button = tk.Button(
            queue_buttons_frame,
            text="Play queue",
            command=self.play_queue,
            width=12,
            height=2,
            bg="lightgreen",
        )
        self.play_queue_button.pack(side="left", padx=8)

        self.remove_songs_button = tk.Button(
            queue_buttons_frame,
            text="Remove songs from the queue",
            command=self.remove_songs_from_queue,
            width=25,
            height=2,
            bg="red",
        )
        self.remove_songs_button.pack(side="left", padx=8)

        self.clear_queue_button = tk.Button(
            queue_buttons_frame,
            text="Clear queue",
            command=self.clear_queue,
            width=12,
            height=2,
            bg="red",
        )
        self.clear_queue_button.pack(side="left", padx=8)

        self.ytmp3_button = tk.Button(
            text="YT MP3 DOWNLOAD", command=lambda: self.program2(), bg="lightgreen"
        )
        self.ytmp3_button.pack(side="bottom")
        self.category_label = tk.Label(text="Created by ITisws.pl", bg="lightgrey")
        self.category_label.configure(font=("Ink Draft", 12))
        self.category_label.pack(side="bottom")

        self.current_label = tk.Label(self.root, text="", bg="lightgrey")
        self.current_label.pack(side="bottom", pady=10)

        nav_button_frame = tk.Frame(self.root, bg="lightgrey")
        nav_button_frame.pack(side="bottom", fill="x")

        self.previous_button = tk.Button(
            nav_button_frame,
            text="⏮Previous",
            command=self.previous_music,
            width=10,
            height=2,
            bg="lightgreen",
        )
        self.previous_button.pack(side="left")
        self.next_button = tk.Button(
            nav_button_frame,
            text="Next⏭",
            command=self.next_music,
            width=10,
            height=2,
            bg="lightgreen",
        )
        self.next_button.pack(side="right")
        rewind_button = tk.Button(
            nav_button_frame,
            text="↩   -10s",
            command=self.rewind,
            font=20,
            bg="lightgreen",
        )
        rewind_button.pack(side="left", padx=100)

        fast_forward_button = tk.Button(
            nav_button_frame,
            text="+10s   ↪",
            command=self.fast_forward,
            font=20,
            bg="lightgreen",
        )
        fast_forward_button.pack(side="right", padx=100)

        button_frame.pack(anchor="center")
        category_frame.pack(anchor="center")
        nav_button_frame.pack(anchor="center")

        self.root.mainloop()

    def select_song_from_category(self, category):
        if category in self.files:
            song_list_window = tk.Toplevel(self.root)
            song_list_window.title(f"{category}")
            song_list_window.geometry("300x300")

            song_listbox = tk.Listbox(song_list_window)
            for song in self.files[category]:
                song_listbox.insert(tk.END, song)
            song_listbox.pack(fill="both", expand=True)

            song_listbox.bind(
                "<Double-1>", lambda event, cat=category: self.play_(cat, song_listbox)
            )

            self.play_all_songs_randomly(category)

        else:
            messagebox.showinfo(f"{category}", "There are no songs in this category.")

    def show_songs(self, category):
        if category in self.files:
            song_list_window = tk.Toplevel(self.root)
            song_list_window.title(f"{category}")
            song_list_window.geometry("430x600")
            song_list_window.transient(self.root)
            song_list_window.grab_set()

            song_listbox = tk.Listbox(song_list_window)
            for song in self.files[category]:
                song_listbox.insert(tk.END, song)
            song_listbox.pack(fill="both", expand=True)

            song_listbox.bind(
                "<Double-1>",
                lambda event, cat=category: self.play_selected_song(cat, song_listbox),
            )

            play_abc_button = tk.Button(
                song_list_window,
                text="ABC",
                command=lambda: self.play_abc(category),
            )
            play_abc_button.pack(side="left", pady=10)

            play_all_randomly_button = tk.Button(
                song_list_window,
                text="Randomly",
                command=lambda: self.play_all_songs_randomly(category),
            )
            play_all_randomly_button.pack(side="left", pady=10, padx=100)
            add_to_queue_button = tk.Button(
                song_list_window,
                text="Add to queue",
                command=lambda: self.add_to_queue(category, song_listbox),
            )
            add_to_queue_button.pack(side="right", pady=15)

        else:
            messagebox.showinfo(f"{category}", "There are no songs in this category.")

    def add_to_queue(self, category, song_listbox):
        selected_song = song_listbox.get(song_listbox.curselection())
        self.queue.append(os.path.join(self.music_folder, category, selected_song))

        if self.player.get_state() == vlc.State.Playing:
            self.play_queue()

    def play_queue(self):
        if not self.queue:
            messagebox.showerror("Error", "There are no tracks in the queue.")
            return

        media_list = vlc.MediaList(self.queue)

        if self.player.get_state() == vlc.State.Playing:
            current_media = self.player.get_media_player().get_media()
            current_index = media_list.index_of_item(current_media)
            media_list.remove_index(current_index)
            self.player.set_media_list(media_list)
        else:
            self.player.stop()
            self.player.set_media_list(media_list)
            self.player.play()

        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def clear_queue(self):
        self.queue.clear()
        messagebox.showinfo("Success", "The queue has been cleared!")

        self.player.stop()
        media_list = vlc.MediaList(self.queue)
        self.player.set_media_list(media_list)
        self.player.play()
        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def remove_songs_from_queue(self):
        if not self.queue:
            messagebox.showerror("Error", "There are no tracks in the queue.")
            return

        remove_songs_window = tk.Toplevel(self.root)
        remove_songs_window.title("Remove songs from the queue")
        remove_songs_window.geometry("350x350")
        remove_songs_window.transient(self.root)
        remove_songs_window.grab_set()

        queue_listbox = tk.Listbox(remove_songs_window)
        for song in self.queue:
            song_name = os.path.basename(song)
            queue_listbox.insert(tk.END, song_name)
        queue_listbox.pack(fill="both", expand=True)

        queue_listbox.bind(
            "<Double-1>", lambda event: self.remove_selected_song(queue_listbox)
        )

        remove_songs_window.mainloop()

    def remove_selected_song(self, queue_listbox):
        media_player = self.player.get_media_player()
        current_media = media_player.get_media()

        selected_index = queue_listbox.curselection()
        self.queue.pop(selected_index[0])
        queue_listbox.delete(selected_index)

        media_list = vlc.MediaList(self.queue)
        self.player.set_media_list(media_list)

        if current_media.get_mrl() in [song.get_mrl() for song in media_list]:
            current_index = media_list.index_of_item(current_media)
            if selected_index[0] <= current_index:
                current_index -= 1
            self.player.play_item_at_index(current_index)
        else:
            self.player.play_item_at_index(0)

        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def play_all_songs_randomly(self, category):
        self.player.stop()
        media_list = vlc.MediaList(
            [
                os.path.join(self.music_folder, category, f)
                for f in random.sample(self.files[category], len(self.files[category]))
            ]
        )

        self.player.set_media_list(media_list)
        self.player.play()

        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def play_abc(self, category):
        self.player.stop()
        sorted_files = sorted(self.files[category])
        media_list = vlc.MediaList(
            [os.path.join(self.music_folder, category, f) for f in sorted_files]
        )

        self.player.set_media_list(media_list)
        self.player.play()

        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def play_selected_song(self, category, song_listbox):
        self.player.stop()

        selected_song = song_listbox.get(song_listbox.curselection())
        media = vlc.Media(os.path.join(self.music_folder, category, selected_song))
        media_list = vlc.MediaList([media])
        self.player.set_media_list(media_list)
        self.player.play()
        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def _load_files(self):
        for category in self.categories:
            category_folder = os.path.join(self.music_folder, category)
            if os.path.exists(category_folder):
                self.files[category] = [
                    f for f in os.listdir(category_folder) if f.endswith(".mp3")
                ]

    def play_music(self):
        category = self.category_var.get()
        if category not in self.files or len(self.files[category]) == 0:
            print(f"There are no files in the category: {category}")
            return

        media_list = vlc.MediaList(
            [
                os.path.join(self.music_folder, category, f)
                for f in random.sample(self.files[category], len(self.files[category]))
            ]
        )

        self.player.set_media_list(media_list)
        self.player.play()

        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def update_current_label(self):
        media_player = self.player.get_media_player()
        media = media_player.get_media()

        if media is not None:
            current_song = media.get_mrl().split("/")[-1]
            current_song = urllib.parse.unquote(current_song)

            media_length = media.get_duration() / 1000
            current_time = media_player.get_time() / 1000
            time_string = f"{int(current_time//60)}:{int(current_time%60):02d} / {int(media_length//60)}:{int(media_length%60):02d}"
            self.current_label.config(text=f"{current_song} ({time_string})")
        else:
            self.current_label.config(text="")

        self.update_label_timer = self.root.after(1000, self.update_current_label)

    def _play_music_thread(self):
        while True:
            if not self.player.is_playing():
                self.root.event_generate("<<EndOfMedia>>", when="tail")
                time.sleep(1)
            else:
                media_player = self.player.get_media_player()
                media = media_player.get_media()
                current_song = media.get_mrl().split("/")[-1]
                current_song = urllib.parse.unquote(current_song)
                self.current_label.config(text=current_song)
                time.sleep(1)

    def fast_forward(self):
        media_player = self.player.get_media_player()
        current_time = media_player.get_time()
        new_time = current_time + 10000
        media_player.set_time(new_time)

    def rewind(self):
        media_player = self.player.get_media_player()
        current_time = media_player.get_time()
        new_time = current_time - 10000
        media_player.set_time(new_time)

    def stop_music(self):
        self.player.stop()
        self.root.after_cancel(self.update_label_timer)
        self.stopped = True
        self.current_label.config(text="")
        self.update_current_label()

    def pause_music(self):
        self.player.pause()

    def next_music(self):
        self.player.next()

    def previous_music(self):
        self.player.previous()

    def unpause_music(self):
        self.player.play()

    def program2(self):
        app = tk.Toplevel(self.root)
        app.title("YouTube MP3 Downloader")
        app.geometry("450x150")
        app.transient(self.root)
        app.grab_set()

        def download_video(url, output_path):
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_path + "/" + "%(title)s.%(ext)s",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        def browse_button():
            folder_selected = filedialog.askdirectory()
            folder_path.set(folder_selected)
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder_selected)

        def start_download():
            url = url_entry.get()
            output_path = folder_path.get()
            if not url or not output_path:
                messagebox.showerror(
                    "Error", "Please enter a URL and select a destination folder"
                )
                return

            try:
                download_video(url, output_path)

                messagebox.showinfo(
                    "Success", "The MP3 file has been successfully downloaded"
                )
                self._load_files()
            except Exception as e:
                messagebox.showerror("Error", f"File download failed: {e}")

        url_label = tk.Label(app, text="URL YouTube:")
        url_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="w")

        url_entry = tk.Entry(app, width=50)
        url_entry.grid(row=0, column=1, padx=(10, 10), pady=(10, 5))

        folder_label = tk.Label(app, text="URL path:")
        folder_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 5), sticky="w")

        folder_path = tk.StringVar()
        folder_entry = tk.Entry(app, textvariable=folder_path, width=40)
        folder_entry.grid(row=1, column=1, padx=(10, 10), pady=(10, 5), sticky="w")

        browse_button = tk.Button(app, text="Select", command=browse_button)
        browse_button.grid(row=1, column=1, padx=(10, 10), pady=(10, 5), sticky="e")

        download_button = tk.Button(app, text="Download MP3", command=start_download)
        download_button.grid(row=2, column=1, pady=(10, 5), sticky="e")

        app.mainloop()


if __name__ == "__main__":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    music_folder = os.path.join(desktop_path, "muzyczka")
    categories = [
        "biesiady",
        "disco polo",
        "hard",
        "inne",
        "lata 80-90",
        "mix",
        "nowoczesna",
        "polski rap",
        "polskie",
        "polskie techno",
        "taneczne",
        "wolne",
        "wolne",
        "zagraniczne techno",
        "zagraniczny rap",
    ]

    player = MusicPlayer(music_folder, categories)
    player.root.mainloop()
