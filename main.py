# Modules Imported
import _thread
import os
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import ttk

from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from pygame import mixer

# Pygame Initiated
mixer.init()

# Global Variables
playing = False
paused = False
mute = False
cur_playing = ''
to_break = False
current_time = 0


# Main Class
class MyApp:
    songs = []

    # COUNT AND INCREMENT CURRENT PLAYING TIME
    def start_count(self, t):
        global current_time
        while current_time <= t and mixer.music.get_busy():
            global paused
            global dur_start
            global progress_bar
            global total_length
            global to_break

            if paused:
                continue
            elif to_break:

                break
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                dur_start['text'] = timeformat
                time.sleep(1)
                current_time += 1
                progress_bar['value'] = current_time
                progress_bar.update()

    # FETCH SONG DETAILS
    def show_details(self, play_song):
        global dur_end
        global progress_bar
        global total_length
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()

        progress_bar['maximum'] = total_length
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        dur_end['text'] = timeformat

        _thread.start_new_thread(self.start_count, (total_length,))

    # FETCH SONG ID3 TAGS
    def get_song_info(self, f):
        audio = ID3(f)  # path: path to file

        title = audio['TIT2'].text[0]
        # album = audio["TALB"].text[0]
        artist = audio['TPE1'].text[0]

        songTitle['text'] = title
        music_note.place(x=50, y=705)
        songArtist['text'] = artist
        artist_ico.place(x=50, y=740)
        # songAlbum['text'] = album

    # ADD SONG FOLDER TO PLAYLIST
    def set_playlist(self):
        try:
            music_ex = ['mp3', 'wav', 'mpeg', 'm4a', 'wma', 'ogg']
            dir_ = filedialog.askdirectory(initialdir='D:\\', title='Select Directory')
            os.chdir(dir_)
            status_bar['text'] = 'Playlist Updated.'
            dir_files = os.listdir(dir_)
            for file in dir_files:
                exten = file.split('.')[-1]
                for ex in music_ex:
                    if exten == ex:
                        play_list.insert(END, file)
                        self.songs.append(file)
        except OSError:
            dir_ = ''

    # ADD SINGLE SONG TO PLAYLIST
    def open_file(self):
        try:
            dir_ = filedialog.askopenfilename(initialdir='D:/', title='Select File')
            cng_dir = dir_.split('/')[0:-1]
            cng_dir = ''.join(cng_dir)
            os.chdir(cng_dir)
            self.songs.append(dir_)
            filename = os.path.basename(dir_)
            play_list.insert(END, filename)
            global playing
            playing = False

        except OSError:
            cng_dir = ''

    # NEXT MUSIC CHOOSER
    def play_next(self, song):
        global playing
        global cur_playing
        global file
        file = song
        cur_playing = file
        mixer.music.load(file)
        mixer.music.play()
        status_bar['text'] = 'Playing - ' + file
        play_button['image'] = pause_img
        playing = True
        self.show_details(file)
        self.get_song_info(file)

    # PLAY MUSIC FUNCTION
    def play_music(self):
        global playing
        global cur_playing
        global file
        try:
            if playing == False:
                file = play_list.get(ACTIVE)
                cur_playing = file
                mixer.music.load(file)
                mixer.music.play()
                status_bar['text'] = 'Playing - ' + file
                play_button['image'] = pause_img
                playing = True
                self.show_details(file)
                self.get_song_info(file)
            else:
                global paused
                if paused == True:
                    mixer.music.unpause()
                    paused = False
                    status_bar['text'] = 'Playing - ' + file
                    play_button['image'] = pause_img
                else:
                    mixer.music.pause()
                    paused = True
                    play_button['image'] = play_img
                    status_bar['text'] = 'Music Paused'
        except:
            mb.showerror('Error', 'No file found to play.')

    # PLAY MUSIC ON DOUBLE CLICK IN PLAYLIST
    def onDoubleClick(self, event):
        global playing
        global cur_playing
        global file
        global current_time
        global progress_bar

        current_time = 0
        dur_start['text'] = '00:00'
        dur_end['text'] = '--:--'
        progress_bar['value'] = 0.0
        progress_bar.update()

        widget = event.widget
        selection = widget.curselection()
        file = widget.get(selection[0])
        cur_playing = file
        mixer.music.load(file)
        mixer.music.play()
        status_bar['text'] = 'Playing - ' + file
        play_button['image'] = pause_img
        playing = True
        self.show_details(file)
        self.get_song_info(file)

    # STOP MUSIC FUNCTION
    def stop_music(self):
        mixer.music.stop()
        global playing
        global paused
        global dur_start
        global progress_bar
        global cur_playing
        global current_time
        current_time = 0
        cur_playing = ''
        playing = False
        paused = False
        dur_start['text'] = '--:--'
        dur_end['text'] = '--:--'
        progress_bar['value'] = 0.0
        progress_bar.update()

        play_button['image'] = play_img
        status_bar['text'] = 'Music Stopped'

        return None

    # NEXT AND PREVIOUS SONG FUNCTION
    def next_prev(self, num):
        global file
        global playing
        global to_break
        global dur_start
        to_break = True
        dur_start['text'] = '00:00'
        try:
            if num == 1:
                index = self.songs.index(file) - 1
                file = self.songs[index]
                mixer.music.load(file)
                mixer.music.play()
                status_bar['text'] = 'Playing - ' + file
                play_button['image'] = pause_img
                playing = True
                self.show_details(file)
                self.get_song_info(file)
            else:
                index = self.songs.index(file) + 1
                file = self.songs[index]
                mixer.music.load(file)
                mixer.music.play()
                status_bar['text'] = 'Playing - ' + file
                play_button['image'] = pause_img
                playing = True
                self.show_details(file)
                self.get_song_info(file)
        except IndexError:
            self.play_music()
            self.get_song_info()
        except ValueError:
            global paused
            playing = False
            paused = False
            self.play_music()
            self.get_song_info()

    # VOLUME FUNCTION
    def speaker_func(self):
        global mute
        global status_bar
        if mute == False:
            speaker['image'] = mute_img
            mixer.music.set_volume(0.0)
            mute = True
        else:
            speaker['image'] = speaker_img
            num = scale.get()
            mixer.music.set_volume(float(num) / 100)
            mute = False

    def set_vol(self, num):
        global mute
        global status_bar
        if num == float(0):
            speaker['image'] = mute_img
            mixer.music.set_volume(0.0)
            mute = True
        elif mute == True:
            speaker['image'] = speaker_img
            num = scale.get()
            mixer.music.set_volume(float(num) / 100)
            mute = False
        else:
            volume = float(num) / 100
            mixer.music.set_volume(volume)

    # EXIT WINDOW FUNCTION
    def exit(self):
        self.stop_music()
        win.destroy()
        sys.exit()

    # ABOUT FUNCTION
    def about(self):
        mb.showinfo('About', 'Project Name : Nix Music Player \n'
                             '\n Developers: '
                             '\n        Nikhil Kumar - 1800267 '
                             '\n        Niladri Mandal -1800268'
                             '\n        Nazpreet - 1800264 \n'
                             '\n Thanks for using our Application.')

    # CONSTRUCTOR METHOD -  MAIN METHOD FOR GUI.
    def __init__(self):

        # Making Tkinter Window.
        global win
        win = Tk()
        width = 1280
        height = 840
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        win.geometry("%dx%d+%d+%d" % (width, height, x, y))
        win.resizable(0, 0)
        win.title('Nix Music Player')
        win.wm_attributes('-alpha', 0.95)
        win.iconbitmap('icons/icon.ico')
        win.config(bg="#753a88")

        # MENU BAR
        main_menu = Menu(win, tearoff=0, bg='#753a88')
        win.configure(menu=main_menu)

        file = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='Media', menu=file)

        file.add_command(label='Open', command=self.open_file)
        file.add_command(label='Open Folder', command=self.set_playlist)
        file.add_separator()
        file.add_command(label='Exit', command=self.exit)

        about = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='About', menu=about)

        about.add_command(label='About Us', command=self.about)

        # PLAYLIST FRAME
        topFrame = Frame(win, bg='#753a88', width=width)
        topFrame.pack(fill=X)

        global play_list
        play_list = Listbox(topFrame, height=20, font='Calibri 16', bg='#753a88', fg='#fff', relief_='flat',
                            bd=0, width=width)
        play_list.pack(ipadx=30, fill=X)
        play_list.bind("<Double-Button-1>", self.onDoubleClick)

        global addSong_button
        add_playlist = PhotoImage(file='icons/add_playlist.png')
        addSong_button = Button(win, image=add_playlist, command=self.set_playlist, bg='#753a88', relief_='flat')
        addSong_button.place(x=1190, y=5)

        # BUTTON CONTROL FRAME
        def on_enter_prev(event):
            prev_des.place(x=400, y=550)

        def on_leave_prev(event):
            prev_des.place(x=1000, y=1000)

        prev_img = PhotoImage(file='icons/prev.png')
        prev_des = Label(win, text='Previous Track', relief='groove')
        prev_button = Button(win, image=prev_img, bd=0, command=lambda: self.next_prev(1), bg='#753a88')
        prev_button.place(x=480, y=560)
        prev_button.bind('<Enter>', on_enter_prev)
        prev_button.bind('<Leave>', on_leave_prev)

        global play_img
        global pause_img
        pause_img = PhotoImage(file='icons/pause.png')
        play_img = PhotoImage(file='icons/play.png')

        def on_enter_play(event):
            play_des.place(x=570, y=540)

        def on_leave_play(event):
            play_des.place(x=1000, y=1000)

        global play_button
        play_des = Label(win, text='Play/Pause', relief='groove')
        play_button = Button(win, image=play_img, bd=0, command=self.play_music, bg='#753a88')
        play_button.place(x=560, y=560)
        play_button.bind('<Enter>', on_enter_play)
        play_button.bind('<Leave>', on_leave_play)

        def on_enter_next(event):
            next_des.place(x=700, y=540)

        def on_leave_next(event):
            next_des.place(x=1000, y=1000)

        next_img = PhotoImage(file='icons/next.png')
        next_des = Label(win, text='Next Track', relief='groove')
        next_button = Button(win, image=next_img, bd=0, command=lambda: self.next_prev(2), bg='#753a88')
        next_button.place(x=640, y=560)
        next_button.bind('<Enter>', on_enter_next)
        next_button.bind('<Leave>', on_leave_next)

        def on_enter_stop(event):
            stop_des.place(x=800, y=540)

        def on_leave_stop(event):
            stop_des.place(x=1000, y=1000)

        stop_img = PhotoImage(file='icons/stop.png')
        stop_des = Label(win, text='Stop Music', relief='groove')
        stop_button = Button(win, image=stop_img, bd=0, command=self.stop_music, bg='#753a88')
        stop_button.place(x=750, y=560)
        stop_button.bind('<Enter>', on_enter_stop)
        stop_button.bind('<Leave>', on_leave_stop)

        # VOLUME FRAME
        global speaker_img
        speaker_img = PhotoImage(file='icons/vol.png')

        global mute_img
        mute_img = PhotoImage(file='icons/mute.png')

        def on_enter_vol(event):
            vol_des.place(x=940, y=540)

        def on_leave_vol(event):
            vol_des.place(x=1000, y=1000)

        global speaker
        vol_des = Label(win, text='Adjust Volume', relief='groove')
        speaker = Button(win, image=speaker_img, bd=0, command=self.speaker_func, bg='#753a88')
        speaker.place(x=980, y=564)
        speaker.bind('<Enter>', on_enter_vol)
        speaker.bind('<Leave>', on_leave_vol)

        global scale
        scale = ttk.Scale(win, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol, length=200)
        scale.set(40)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.4)
        scale.place(x=1050, y=590)

        # TIME DURATIONS
        global dur_start, dur_end
        dur_start = Label(win, text='--:--', font=('Calibri', 12, 'bold'), bg='#753a88', fg='#fff')
        dur_start.place(x=340, y=660)
        dur_end = Label(win, text='--:--', font=('Calibri', 12, 'bold'), bg='#753a88', fg='#fff')
        dur_end.place(x=920, y=660)

        # PROGRESS BAR
        global progress_bar
        progress_bar = ttk.Progressbar(win, orient='horizontal', length=500)
        progress_bar.place(x=400, y=660)

        # DISPLAY SONG ID3 TAGS
        global songTitle
        global music_note
        music_img = PhotoImage(file='icons/musicnote.png')
        music_note = Label(win, image=music_img, bg='#753a88')
        songTitle = Label(win, text='', bg='#753a88', fg='#fff', font='Calibri 20')
        music_note.place(x=1000, y=1000)
        songTitle.place(x=84, y=700)

        global songArtist
        global artist_ico
        artist_img = PhotoImage(file='icons/album.png')
        artist_ico = Label(win, image=artist_img, bg='#753a88')
        songArtist = Label(win, text='', bg='#753a88', fg='#fff', font='Calibri 14')
        artist_ico.place(x=1000, y=1000)
        songArtist.place(x=84, y=740)

        # STATUS BAR
        global status_bar
        status_bar = Label(win, text='Welcome to NiX Music Player', relief_='ridge', anchor=W, bg='#fff', fg='#753a88',
                           font='Arial 10 bold')
        status_bar.pack(side=BOTTOM, fill=X)

        win.protocol("WM_DELETE_WINDOW", self.exit)
        win.mainloop()


music_player = MyApp()
