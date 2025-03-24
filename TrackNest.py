# Tkinter equivalent for the given PyQt5-based GUI
'''
1. 主選單＿歌曲的子選單第七個選項（這個紅色還沒顯現）[MAC的問題用windows就好，已解決]
2. 左上角的LOGO還沒成功顯現[已解決]
3. 左邊widget的button還是有奇怪的背景[MAC的問題用windows就好，已解決]
4. 還沒研究好怎麼只設定上下其中一邊的距離[pady=(5,30)][已解決]
5. 捲軸 [已解決]
6. 音樂進度條很不乖！！！！！！:(
7. 暫停✅、上一首✅、下一首✅、調高調低音量[menu的還沒辦法]✅、隨機、重複[功能似乎沒辦法開了又關]、詳細資訊、登出登入✅、帳號詳細資訊✅
   從資料庫中刪除✅、加入到資料庫✅、關閉✅、視窗最大化✅、視窗最小化✅、menu1✅、menu2✅、menu3✅、menu4✅、menu5✅、menu6✅
'''
from pygame import mixer
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
import random
from mp3_reg import Login

class MP3Player:
    def __init__(self, root, memberid):
        '''設定主視窗與事前作業'''
        self.root = root
        self.root.title("TrackNest")
        self.root.geometry("1128x783")
        logo = Image.open('logo.png')
        self.root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(logo))
        
        # Database Configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '12345678',
            'database': 'mp3'
        }

        # Initialize
        mixer.init()                            # Initialize the mixer
        self.memberid=memberid                  # Store the memberid
        self.song_data = []                     # Store the song data
        self.current_song_path = None           # Store the path of the current song
        self.song_length = 0                    # Store the length of the current song
        self.is_paused = False                  # Flag to check if the song is paused
        self.current_song_index = -1            # Index of the current song
        self.random_mode = False                # Random mode off by default
        self.repeat_mode = False                # Repeat mode off by default
        self.create_widgets()

    def create_widgets(self):
        '''Initialize Widgets 將主視窗分成三個frame'''
        left_frame = tk.Frame(self.root, bg="#061933", width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0)
        self.content_frame = tk.Frame(self.root, bg="#fefbe7")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.table_frame = tk.Frame(self.content_frame)
        self.table_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        '''設定MenuBar,mac與windows的menu不同,這個是mac的menu'''
        menubar = tk.Menu(self.root)                                          # 建立主選單
        # 建立主選單＿About
        menu_1 = tk.Menu(menubar)                                             # 第一個選單的子選單
        menu_1.add_command(label="TrackNest", command=self.open_TrackNest)    # 子選單第一個選項
        menubar.add_cascade(label='About', menu=menu_1)                       
        # 建立主選單＿歌曲
        menu_2 = tk.Menu(menubar)                                             
        menu_2.add_command(label="加入至Library", command=self.add_library)    
        menu_2.add_command(label="從資料庫中刪除", foreground='red', command=self.delete_library)    
        menu_2.add_separator()                                                # 子選單的分隔線
        menu_2.add_command(label="詳細資訊", command=self.open_songinfo)    
        menubar.add_cascade(label='歌曲', menu=menu_2)                         
        # 建立主選單＿控制      
        menu_3 = tk.Menu(menubar)           
        menu_3.add_command(label="暫停", command=self.pause_song)    
        menu_3.add_command(label="上一首", command=self.play_previous_song)    
        menu_3.add_command(label="下一首", command=self.play_next_song)    
        menu_3.add_separator()            
        menu_3.add_command(label="調高音量", command=self.set_volume)    
        menu_3.add_command(label="調低音量", command=self.set_volume)    
        menu_3.add_separator()             
        menu_3.add_command(label="隨機", command=self.play_random_song)    
        menu_3.add_command(label="重複", command=self.repeat_song)    
        menu_3.add_separator()            
        menu_3.add_command(label="離開", command=self.root.quit)   
        menubar.add_cascade(label='控制', menu=menu_3)                         
        # 建立主選單＿帳號
        menu_4 = tk.Menu(menubar)
        menu_4.add_command(label="帳號資訊", command=self.open_account)
        menu_4.add_command(label="登出", command=self.logout)
        menu_4.add_separator()
        menu_4_more1 = tk.Menu(menu_4)                                        # 建立子選單內的子選單1，有兩個選項
        menu_4_more1.add_command(label="歌曲", command=self.library)           # 子選單的子選單的第一個選項
        menu_4_more1.add_command(label="專輯", command=self.all_album)         # 子選單的子選單的第二個選項
        menu_4_more1.add_command(label="藝人", command=self.all_artist)        # 子選單的子選單的第三個選項
        menu_4.add_cascade(label='我的歌曲庫', menu=menu_4_more1)               # 建立子選單內的子選單1＿我的歌曲庫
        menubar.add_cascade(label='帳號', menu=menu_4)                         
        # 建立主選單＿視窗
        menu_5 = tk.Menu(menubar)
        menu_5.add_command(label="視窗最大化", command= lambda: self.root.state('zoomed'))
        menu_5.add_command(label="視窗最小化", command= lambda: self.root.state('iconic'))
        menubar.add_cascade(label='視窗', menu=menu_5)                         
        # 建立主選單＿Help
        menu_6 = tk.Menu(menubar)
        menu_6.add_command(label="Connect...", command=self.open_connect)
        menubar.add_cascade(label='Help', menu=menu_6)                         
        self.root.config(menu=menubar)                                         # 主視窗加入主選單
        
        '''left_widget的內容物'''
        # Top Section(LOGO)
        top_logo = tk.Frame(left_frame, bg="#061933")
        top_logo.pack(fill=tk.X)
        img_logo = Image.open('logo.jpg')
        img_logo = img_logo.resize((100, 100))
        tk_img = ImageTk.PhotoImage(img_logo)
        label = tk.Label(left_frame, image=tk_img, width=100, height=100, bg="#061933")
        label.image = tk_img  # 保持對圖像的引用
        label.pack(anchor='nw', padx=30, pady=20)
        
        # Buttons and labels
        label_tracknest = tk.Label(left_frame, text="TrackNest", font=("Times New Roman", 15), fg="#e87055", bg="#061933")
        label_tracknest.pack(anchor="w", padx=5)
        ranking_button = tk.Button(left_frame, text="排行榜", bg="#061933", border=None, relief=tk.FLAT, command=self.billboard) #win改, fg='#ffffff'
        ranking_button.pack(fill=tk.X, pady=(5,30))
        
        label_library = tk.Label(left_frame, text="Library", font=("Times New Roman", 15), fg="#e87055", bg="#061933")
        label_library.pack(anchor="w", padx=5)
        songs_button = tk.Button(left_frame, text="歌曲", bg="#061933", border=None, relief=tk.FLAT, command=self.library)#win改, fg='#ffffff'
        songs_button.pack(fill=tk.X, pady=0)
        album_button = tk.Button(left_frame, text="專輯", bg="#061933", border=None, relief=tk.FLAT, command=self.all_album)#win改, fg='#ffffff'
        album_button.pack(fill=tk.X, pady=0)
        singer_button = tk.Button(left_frame, text="藝人", bg="#061933", border=None, relief=tk.FLAT, command=self.all_artist)
        singer_button.pack(fill=tk.X, pady=(0,30))
        
        label_list = tk.Label(left_frame, text="RecommendList", font=("Times New Roman", 15), fg="#e87055", bg="#061933")
        label_list.pack(anchor="w", padx=5)
        button_names = [("蔡昀蓁's", '蔡'),("呂哲瑋's", '呂'),("李哲言's", '李'),("歐芸亘's", '歐')]
        for name, code in button_names:
            playlist_button = tk.Button(left_frame, text=name, bg="#061933", border=None, 
                                        relief=tk.FLAT,command=lambda c=code: self.load_recommendation_songs(c))
            playlist_button.pack(fill=tk.X, pady=0)
        
        label_name = tk.Label(left_frame, text="Made by Yun Jeng Tsai", font=("Times New Roman", 12), fg="lightblue", bg="#061933")
        label_name.pack(side=tk.BOTTOM)

        '''設定右下與右上的widget'''
        # Top Frame in Content Widget
        top_frame = tk.Frame(self.content_frame, bg="#061933")
        top_frame.pack(side=tk.TOP,fill=tk.X)

        # btn_frame in top_frame
        btn_frame = tk.Frame(top_frame, bg="#061933")
        btn_frame.pack(side=tk.LEFT, padx=1, pady=(70,45))
        # Buttons in btn_frame
        self.btn_random = tk.Button(btn_frame, text="⤮", width=1, bg="#061933", command=self.play_random_song)#win改, fg='#ffffff'
        self.btn_random.grid(row=1, column=0)
        btn_previous = tk.Button(btn_frame, text="⏮", width=1, bg="#061933", command=self.play_previous_song)#win改, fg='#ffffff'
        btn_previous.grid(row=1, column=1)
        btn_play = tk.Button(btn_frame, text="▶︎", width=1, bg="#061933", command=self.pause_song)#win改, fg='#ffffff'
        btn_play.grid(row=1, column=2)
        btn_next = tk.Button(btn_frame, text="⏭", width=1, bg="#061933", command=self.play_next_song)#win改, fg='#ffffff'
        btn_next.grid(row=1, column=3)
        self.btn_repeat = tk.Button(btn_frame, text='↺', font=(15), bg="#061933", command=self.repeat_song)#win改, fg='#ffffff'
        self.btn_repeat.grid(row=1, column=4)
        
        # song_frame in top_frame
        song_frame = tk.Frame(top_frame, bg="#061933")
        song_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5), pady=(30,30))
        # Song title in song_frame
        self.song_title = tk.Label(song_frame, text="None", font=("Times New Roman", 18), bg="#061933", fg='#ffffff')
        self.song_title.pack(side=tk.TOP, padx=10)

        # Progress Frame in song_frame
        progress_frame = tk.Frame(song_frame)
        progress_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        # Music progress bar in progress_frame
        self.current_time = tk.Label(progress_frame, text="00:00", bg="#061933", fg='#ffffff')
        self.current_time.pack(side=tk.LEFT)
        self.progress = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.progress.bind("<ButtonRelease-1>", self.set_playback_position)
        self.total_time = tk.Label(progress_frame, text="04:00", bg="#061933", fg='#ffffff')
        self.total_time.pack(side=tk.RIGHT)

        # Volume Frame in top_frame
        volume_frame = tk.Frame(top_frame)
        volume_frame.pack(side=tk.RIGHT, padx=5, pady=(53,45))
        # Volume control in volume_frame
        volume_label = ttk.Label(volume_frame, text="Volume")
        volume_label.pack(side=tk.TOP, padx=10)
        volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        volume_slider.set(50) # 預設音量50
        volume_slider.pack(side=tk.LEFT, padx=5)

    '''Menu功能'''
    def open_TrackNest(self):
        TrackNest = tk.Toplevel()
        TrackNest.title("TrackNest")
        TrackNest.geometry("300x100")
        TrackNest.attributes('-topmost', True)
        TrackNest = tk.Label(TrackNest, text='Welcome to TrackNest, \nthe best music platform ever!\n'
                             'This is the 4th edit version. \n Enjoy your music journey!', font=("Times New Roman", 16))
        TrackNest.pack()

    def add_library(self):
        try:
            # 連接資料庫並且抓取SongID
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            selected_item = self.song_list.selection()[0]
            song_index = self.song_list.index(selected_item)
            songid = self.song_data[song_index].get("SongID")
            # 檢查是否已經加入過
            cursor.execute("SELECT * FROM PlayListSongs WHERE SongID = %s AND MemberID = %s",
            (songid, self.memberid))
            result = cursor.fetchone()
            if result:
                messagebox.showwarning("重複", "這首歌曲已經在您的資料庫中！")
            else:
                cursor.execute(
                    "INSERT INTO PlayListSongs (SongID, MemberID) VALUES (%s, %s)",
                    (songid, self.memberid)
                )
                conn.commit()
                messagebox.showinfo("成功", "歌曲已加入至您的資料庫！")
        finally:
            conn.close()   

    def delete_library(self):
        try:
            # 連接資料庫並且抓取SongID
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            selected_item = self.song_list.selection()[0]
            song_index = self.song_list.index(selected_item)
            songid = self.song_data[song_index].get("SongID")
            cursor.execute(
                "delete from PlayListSongs where SongID=%s and MemberID=%s",(songid, self.memberid,))
            conn.commit()
            messagebox.showwarning("成功", "歌曲已從您的資料庫中刪除！")
            self.library()  # 刷新 Library 顯示
        except Exception as e:
            print(f"Error: {e}")  # Print any error that occurs
        finally:
            conn.close()

    def open_songinfo(self):
        # 創建一個新的 Toplevel 視窗
        Account = tk.Toplevel()
        Account.title("Song_info.")
        Account.geometry("400x200")
        Account.attributes('-topmost', True)

        # 獲取 Treeview 中選中的項目
        try:
            selected_item = self.song_list.selection()[0]
            song_index = self.song_list.index(selected_item)
            songid = self.song_data[song_index].get("SongID")
        except IndexError:
            # 沒有選中歌曲時提示使用者
            tk.Label(Account, text="No song selected.", font=("Times New Roman", 16)).pack(padx=10, pady=10)
            return
        if not songid:
            tk.Label(Account, text="Invalid song ID.", font=("Times New Roman", 16)).pack(padx=10, pady=10)
            return

        # 查詢當前歌曲資訊
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    song.SongID, song.Title, song.Duration, song.ReleaseDate, 
                    Artist.ArtistName, Album.AlbumName, Category.CategoryName, 
                    Composer.ComposerName
                FROM 
                    (((song 
                    INNER JOIN Artist ON song.ArtistID = Artist.ArtistID)
                    INNER JOIN Album ON song.AlbumID = Album.AlbumID)
                    INNER JOIN Category ON song.CategoryID = Category.CategoryID)
                    INNER JOIN Composer ON song.ComposerID = Composer.ComposerID
                WHERE 
                    song.SongID = %s""", (songid,))
            song = cursor.fetchone()
        except mysql.connector.Error as err:
            tk.Label(Account, text=f"Error: {err}", font=("Times New Roman", 16)).pack(padx=10, pady=10)
            return
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
        # 顯示用戶資訊
        if song:
            account_info = (
                f"{song['Title']} by {song['ArtistName']}\n\n"
                f"📍專輯：{song['AlbumName']}\n"
                f"📍歌曲類型： {song['CategoryName']}\n"
                f"📍發行日： {song['ReleaseDate']}\n"
                f"📍歌曲時間： {song['Duration']}\n"
                f"📍作曲人： {song['ComposerName']}\n"
            )
        else:
            account_info = "No account information found."
        # 在視窗中顯示資訊
        label = tk.Label(Account, text=account_info, font=("Times New Roman", 16), justify="left")
        label.pack(padx=10, pady=10)

    def pause_song(self):
        if self.current_song_path:
            if not self.is_paused:
                mixer.music.pause()
                self.is_paused = True
            else:
                mixer.music.unpause()
                self.is_paused = False
                current_song = self.song_data[self.current_song_index]
                for i in self.song_data:
                    if i['SongID'] == self.current_song_index:
                        current_song = i
                        break
                self.song_title.config(text=f"{current_song['Title']} - {current_song['ArtistName']}")
            self.update_progress()

    def play_previous_song(self):
        if self.song_data and self.current_song_index > 0:
            # 找歌曲索引值
            for i in self.song_data:
                if i['SongID'] == self.current_song_index:
                    current_song_in_list = self.song_data.index(i)
                    break
            self.current_song_index = self.song_data[current_song_in_list - 1]['SongID']
            self.play_song_by_index(self.current_song_index)
        self.update_progress()

    def play_next_song(self):
        if self.song_data and self.current_song_index > 0:
            # 找歌曲索引值
            for i in self.song_data:
                if i['SongID'] == self.current_song_index:
                    current_song_in_list = self.song_data.index(i)
                    break
            self.current_song_index = self.song_data[current_song_in_list + 1]['SongID']
            self.play_song_by_index(self.current_song_index)
        self.update_progress()

    def set_volume(self, value):
        mixer.music.set_volume(float(value) / 100)

    def play_random_song(self):
        self.random_mode = not self.random_mode
        if self.song_data:
            random_index = random.randint(0, len(self.song_data) - 1)
            self.play_song_by_index(random_index)
        if self.random_mode:
            self.btn_random.config(text='🔀', width=1)
        else:
            self.btn_random.config(text='⤭', width=1)
        self.update_progress()
    
    def repeat_song(self):
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            self.btn_repeat.config(text='🔁', width=1)
        else:
            self.btn_repeat.config(text='↺', width=1)
        self.update_progress()

    def open_account(self):
        # 創建一個新的 Toplevel 視窗
        Account = tk.Toplevel()
        Account.title("Account")
        Account.geometry("300x200")
        Account.attributes('-topmost', True)
        
        # 查詢當前用戶的帳號資訊
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT memberid, name, email, joindate, membertype FROM member WHERE memberid=%s", 
            (self.memberid,)
        )
        member = cursor.fetchone()
        conn.close()

        # 顯示用戶資訊
        if member:
            account_info = (
                f"Account Information：\n\n"
                f"📍會員ID： {member['memberid']}\n"
                f"📍會員名稱： {member['name']}\n"
                f"📍Mail： {member['email']}\n"
                f"📍加入日期： {member['joindate']}\n"
                f"📍會員類型： {member['membertype']}\n"
            )
        else:
            account_info = "No account information found."

        # 在視窗中顯示資訊
        label = tk.Label(Account, text=account_info, font=("Times New Roman", 16), justify="left")
        label.pack(padx=10, pady=10)

    def logout(self):
        # 顯示確認對話框
        if messagebox.askyesno("Logout", "Are you sure you want to logout and leave?"):
            self.root.destroy()

    def open_connect(self):
        Connect = tk.Toplevel()
        Connect.title("Connect...")
        Connect.geometry("300x200")
        Connect.attributes('-topmost', True)
        Connect = tk.Label(Connect, text='If you have a Questions or Recommend, \nPlease connect: \n\n'
                            'Email:TrackNest@gmail.com\n\n Phone:0912-123456 \n\n Line:@TrackNest\n\n'
                            'Thank you for your support!🧚🏻‍♀️'
                           , font=("Times New Roman", 16))
        Connect.pack()

    '''右鍵功能'''
    def show_menu(self, event):
        print("Right-click detected")
        self.song_list.selection_set(self.song_list.identify_row(event.y))
        self.right_click_menu.post(event.x_root, event.y_root)

    '''選擇並且播放歌曲'''
    def play_song_by_index(self, index):
        try:
            for i in self.song_data:
                if i['SongID'] == index:
                    song = i
                    self.current_song_path = song['FilePath']
                    break
            #song = self.song_data[index]
            self.current_song_index = index

            if not os.path.exists(self.current_song_path):
                self.song_title.config(text=f"File not found: {self.current_song_path}")
                return

            mixer.music.load(self.current_song_path)
            mixer.music.play()
            self.song_title.config(text=f"{song['Title']} - {song['ArtistName']}")

            # Calculate and display total time
            self.song_length = mixer.Sound(self.current_song_path).get_length()
            self.total_time.config(text=self.format_time(self.song_length))
            self.progress.config(to=self.song_length)

            self.is_paused = False  # Reset paused state
            self.update_progress()
        except IndexError:
            self.song_title.config(text="No song selected.")

    def play_selected_song(self, event=None):
        try:
            selected_item = self.song_list.selection()[0]
            song_index = self.song_list.index(selected_item)
            song = self.song_data[song_index]
            self.current_song_index = song['SongID']
            self.current_song_path = song['FilePath']

            if not os.path.exists(self.current_song_path):
                self.song_title.config(text=f"File not found: {self.current_song_path}")
                return

            mixer.music.load(self.current_song_path)
            mixer.music.play()
            self.song_title.config(text=f"{song['Title']} - {song['ArtistName']}")

            # Calculate and display total time
            self.song_length = mixer.Sound(self.current_song_path).get_length()
            self.total_time.config(text=self.format_time(self.song_length))
            self.progress.config(to=self.song_length)

            self.is_paused = False  # Reset paused state
            self.update_progress()
        except IndexError:
            self.song_title.config(text="No song selected.")

    def update_progress(self):
        if mixer.music.get_busy() and not self.is_paused:
            current_pos = mixer.music.get_pos() // 1000  # Get current position in seconds
            self.progress.set(current_pos)
            self.current_time.config(text=self.format_time(current_pos))
            # Continue updating every 1 second
            self.root.after(1000, self.update_progress)
        elif not self.is_paused:
            if self.repeat_mode:
                mixer.music.play()  # Replay the current song
                self.update_progress()
            if self.random_mode:
                random_index = random.randint(0, len(self.song_data) - 1)
                self.play_song_by_index(random_index)
            if self.current_song_index < len(self.song_data) - 1:
                self.play_next_song()
            
    def set_playback_position(self, event):
        if self.current_song_path:
            new_position = int(self.progress.get())
            mixer.music.pause()
            mixer.music.play(start=new_position) # 跳轉到新位置播放
            self.current_time.config(text=self.format_time(new_position)) # 更新當前時間顯示

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    '''左側功能：Billbroad, Library, RecommendList'''
    def library(self):
        if hasattr(self, 'song_list'):
            for row in self.song_list.get_children():
                self.song_list.delete(row)
            self.song_list.destroy()
        if hasattr(self, 'scrollY'):
            self.scrollY.destroy()
        #垂直卷軸
        self.scrollY = tk.Scrollbar(self.table_frame, orient='vertical')  # 垂直捲軸放在 frame 裡
        self.scrollY.pack(side='right', fill='y')                     # 放在下面填滿 x 軸
        columns = ("#1", "#2", "#3", "#4")
        S = ttk.Style()
        S.configure('Treeview', fieldbackground='#fefbe7')
        self.song_list = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.song_list.heading("#1", text="名稱")
        self.song_list.heading("#2", text="時間長度")
        self.song_list.heading("#3", text="藝人")
        self.song_list.heading("#4", text="類型") 
        #self.song_list.pack_forget()
        self.song_list.bind("<Double-1>", self.play_selected_song)

        self.right_click_menu = tk.Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label="詳細資訊", command=self.open_songinfo)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="從資料庫中刪除", foreground='red', command=self.delete_library)
        self.song_list.bind("<Button-2>", self.show_menu)
        self.song_list.pack(fill=tk.BOTH, expand=True)
        
        self.song_list.config(yscrollcommand=self.scrollY.set)    # Canvas 綁定捲軸
        self.scrollY.config(command=self.song_list.yview)                   # 綁定 Canvas x 方向
        
        self.load_songs_from_library_db()

    def load_songs_from_library_db(self, treeview=None):    
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor.execute("""
                SELECT 
                    song.SongID, song.Title, song.Duration, Artist.ArtistName, Category.CategoryName, song.FilePath
                FROM 
                    PlayListSongs
                INNER JOIN 
                    song ON PlayListSongs.SongID = song.SongID
                INNER JOIN 
                    Artist ON song.ArtistID = Artist.ArtistID
                INNER JOIN 
                    Category ON song.CategoryID = Category.CategoryID
                WHERE 
                    PlayListSongs.MemberID = %s
            """, (self.memberid,))
            songs = cursor.fetchall()
            self.song_data = songs  # Store songs for reference
        # Populate the Treeview with songs
            if hasattr(self, 'song_list'):
                for song in songs:
                    self.song_list.insert("", "end", values=(
                    song['Title'], song['Duration'], song['ArtistName'], song['CategoryName']
                    ))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def all_album(self):
        if hasattr(self, 'song_list'):
            for row in self.song_list.get_children():
                self.song_list.delete(row)
            self.song_list.destroy()
        if hasattr(self, 'scrollY'):
            self.scrollY.destroy()
        
        #垂直卷軸
        self.scrollY = tk.Scrollbar(self.table_frame, orient='vertical')  # 垂直捲軸放在 frame 裡
        self.scrollY.pack(side='right', fill='y')                     # 放在下面填滿 x 軸
        columns = ("#1", "#2")
        S = ttk.Style()
        S.configure('Treeview', fieldbackground='#fefbe7')
        self.song_list = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.song_list.heading("#1", text="專輯名稱")
        self.song_list.heading("#2", text="歌曲數量")
        #self.song_list.bind("<Double-1>")
        self.song_list.pack(fill=tk.BOTH, expand=True)
        
        self.song_list.config(yscrollcommand=self.scrollY.set)    # Canvas 綁定捲軸
        self.scrollY.config(command=self.song_list.yview)                   # 綁定 Canvas x 方向
        self.load_songs_from_album_db()

    def load_songs_from_album_db(self, treeview=None):    
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor.execute("""
                SELECT 
                    Album.AlbumName, COUNT(song.SongID) AS SongCount
                FROM 
                    PlayListSongs
                INNER JOIN 
                    song ON PlayListSongs.SongID = song.SongID
                INNER JOIN 
                    Album ON song.AlbumID = Album.AlbumID
                WHERE 
                    PlayListSongs.MemberID = %s
                GROUP BY
                    Album.AlbumName
            """, (self.memberid,))
            albums = cursor.fetchall()
            self.album_data = albums  # Store songs for reference
            # Populate the Treeview with unique album names
            if hasattr(self, 'song_list'):
                for album in albums:
                    self.song_list.insert("", "end", values=(album['AlbumName'], album['SongCount']))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def all_artist(self):
        if hasattr(self, 'song_list'):
            for row in self.song_list.get_children():
                self.song_list.delete(row)
            self.song_list.destroy()
        if hasattr(self, 'scrollY'):
            self.scrollY.destroy()
        #垂直卷軸
        self.scrollY = tk.Scrollbar(self.table_frame, orient='vertical')  # 垂直捲軸放在 frame 裡
        self.scrollY.pack(side='right', fill='y')                     # 放在下面填滿 x 軸
        columns = ("#1", "#2")
        S = ttk.Style()
        S.configure('Treeview', fieldbackground='#fefbe7')
        self.song_list = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.song_list.heading("#1", text="藝人名稱")
        self.song_list.heading("#2", text="歌曲數量")
        #self.song_list.bind("<Double-1>")
        self.song_list.pack(fill=tk.BOTH, expand=True)
        self.song_list.config(yscrollcommand=self.scrollY.set)    # Canvas 綁定捲軸
        self.scrollY.config(command=self.song_list.yview)                   # 綁定 Canvas x 方向
        self.load_songs_from_artist_db() 

    def load_songs_from_artist_db(self, treeview=None):    
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor.execute("""
                SELECT 
                    Artist.ArtistName, COUNT(song.SongID) AS SongCount
                FROM 
                    PlayListSongs
                INNER JOIN 
                    song ON PlayListSongs.SongID = song.SongID
                INNER JOIN 
                    Artist ON song.ArtistID = Artist.ArtistID
                WHERE 
                    PlayListSongs.MemberID = %s
                GROUP BY
                    Artist.ArtistName
            """, (self.memberid,))
            artists = cursor.fetchall()
            self.artist_data = artists  # Store songs for reference
        # Populate the Treeview with songs
            if hasattr(self, 'song_list'):
                for artist in artists:
                    self.song_list.insert("", "end", values=(artist['ArtistName'], artist['SongCount']))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def billboard(self):
        if hasattr(self, 'song_list'):
            for row in self.song_list.get_children():
                self.song_list.delete(row)
            self.song_list.destroy()
        if hasattr(self, 'scrollX'):
            self.scrollX.destroy()
        if hasattr(self, 'scrollY'):
            self.scrollY.destroy()
        # 水平卷軸
        self.scrollX = tk.Scrollbar(self.table_frame, orient='horizontal')  # 水平捲軸放在 frame 裡
        self.scrollX.pack(side='bottom', fill='x')                     # 放在下面填滿 x 軸
        #垂直卷軸
        self.scrollY = tk.Scrollbar(self.table_frame, orient='vertical')  # 垂直捲軸放在 frame 裡
        self.scrollY.pack(side='right', fill='y')                     # 放在下面填滿 x 軸
        columns = ("#1", "#2", "#3", "#4", "#5")
        S = ttk.Style()
        S.configure('Treeview', fieldbackground='#fefbe7')
        self.song_list = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.song_list.heading("#1", text="播放次數")
        self.song_list.heading("#2", text="名稱")
        self.song_list.heading("#3", text="時間長度") # 時間長度（現在先以ReleaseDate）
        self.song_list.heading("#4", text="藝人") 
        self.song_list.heading("#5", text="類型")
        #self.song_list.pack_forget()
        self.song_list.bind("<Double-1>", self.play_selected_song)

        self.right_click_menu = tk.Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label="加入至Library", command=self.add_library)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="詳細資訊", command=self.open_songinfo)
        self.song_list.bind("<Button-2>", self.show_menu)
        self.song_list.pack(fill=tk.BOTH, expand=True)

        self.song_list.config(xscrollcommand=self.scrollX.set, yscrollcommand=self.scrollY.set)    # Canvas 綁定捲軸
        self.scrollX.config(command=self.song_list.xview)                   # 綁定 Canvas x 方向
        self.scrollY.config(command=self.song_list.yview)                   # 綁定 Canvas x 方向
        
        self.load_songs_from_billboard_db() 

    def load_songs_from_billboard_db(self, treeview=None):
        #conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor.execute("select Billboard.Playtimes, song.SongID, song.Title, song.Duration, Artist.ArtistName, Category.CategoryName, song.FilePath "
                           "from ((song inner join Billboard on song.SongID = Billboard.SongID)"
                           "inner join Artist on song.artistID = Artist.ArtistID)"
                           "inner join Category on song.CategoryID = Category.CategoryID  ORDER BY Playtimes DESC")
            songs = cursor.fetchall()
            self.song_data = songs  # Store songs for reference

            # Populate the Treeview with songs
            if hasattr(self, 'song_list'):
                for song in songs:
                    self.song_list.insert("", "end", values=(
                        song['Playtimes'], song['Title'], song['Duration'], song['ArtistName'], song['CategoryName']
                    ))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def load_recommendation_songs(self, code):
        # 清空 treeview
        if hasattr(self, 'song_list'):
            for row in self.song_list.get_children():
                self.song_list.delete(row)
            self.song_list.destroy()
        if hasattr(self, 'scrollY'):
            self.scrollY.destroy()
        #垂直卷軸
        self.scrollY = tk.Scrollbar(self.table_frame, orient='vertical')  # 垂直捲軸放在 frame 裡
        self.scrollY.pack(side='right', fill='y')                     # 放在下面填滿 x 軸

        # 重新設定 treeview
        columns = ("#1", "#2", "#3", "#4")
        S = ttk.Style()
        S.configure('Treeview', fieldbackground='#fefbe7')
        self.song_list = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.song_list.heading("#1", text="名稱")
        self.song_list.heading("#2", text="時間長度")
        self.song_list.heading("#3", text="藝人")
        self.song_list.heading("#4", text="類型")
        self.song_list.pack(fill=tk.BOTH, expand=True)

        # 綁定雙擊事件
        self.song_list.bind("<Double-1>", self.play_selected_song)

        self.right_click_menu = tk.Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label="加入至Library", command=self.add_library)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="詳細資訊", command=self.open_songinfo)
        self.song_list.bind("<Button-2>", self.show_menu)
        self.song_list.pack(fill=tk.BOTH, expand=True)
        self.song_list.config(yscrollcommand=self.scrollY.set)    # Canvas 綁定捲軸
        self.scrollY.config(command=self.song_list.yview)                   # 綁定 Canvas x 方向
        
        # 加載推薦歌曲
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    song.SongID, song.Title, song.Duration, Artist.ArtistName, Category.CategoryName, song.FilePath
                FROM 
                    song
                INNER JOIN 
                    Artist ON song.ArtistID = Artist.ArtistID
                INNER JOIN 
                    Category ON song.CategoryID = Category.CategoryID
                WHERE 
                    song.ourcode = %s
            """
            cursor.execute(query, (code,))
            songs = cursor.fetchall()
            self.song_data = songs  # 存儲歌曲數據

            # 更新 treeview
            for song in songs:
                self.song_list.insert("", "end", values=(
                    song['Title'], song['Duration'], song['ArtistName'], song['CategoryName']
                ))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    def start_main_app(memberid):
        main_window = tk.Tk()
        MP3Player(main_window, memberid)
        main_window.mainloop()

    root = tk.Tk()
    app = Login(root, start_main_app)
    root.mainloop()