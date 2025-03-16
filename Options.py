import os,json
import tkinter as tk
from tkinter import ttk, Toplevel
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox



KEY_MAPPING = {
    "ESCAPE": "esc",
    "RETURN": "enter",
    "SPACE": "space",
    "UP": "up",
    "DOWN": "down",
    "LEFT": "left",
    "RIGHT": "right",
    "A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i",
    "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r",
    "S": "s", "T": "t", "U": "u", "V": "v", "W": "w", "X": "x", "Y": "y", "Z": "z",
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
    "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5",
    "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10",
    "F11": "f11", "F12": "f12",
    "TAB": "tab", "CAPS_LOCK": "caps lock", "SHIFT_L": "shift", "SHIFT_R": "shift",
    "CONTROL_L": "ctrl", "CONTROL_R": "ctrl", "ALT_L": "alt", "ALT_R": "alt",
    "INSERT": "insert", "DELETE": "delete", "HOME": "home", "END": "end",
    "PAGE_UP": "page up", "NEXT": "page down",
    "NUM_LOCK": "num lock", "SCROLL_LOCK": "scroll lock",
    "MULTIPLY": "multiply", "ADD": "add", "SUBTRACT": "subtract", "DECIMAL": "decimal",
}



class KeySelectorApp:
    def __init__(self, master):
        self.master = master
        self.selected_key_name = None
        self.is_window_open = False


        self.temp_data = {}  # Geçici veriler
        self.load_data = {}  # JSON'dan gelen veriler

        self.load_from_json()  # Başlangıçta JSON'dan verileri yükle


    def on_key_press(self, event,title):
            key_name = event.keysym.upper()
            if key_name in KEY_MAPPING:
                selected_key_name = KEY_MAPPING[key_name]
                key_value = f"{key_name})"
                print(f'Selected Key: {selected_key_name}')
                self.select_button['text'] = selected_key_name
                self.new_win.unbind("<KeyPress>")
            else:
                self.select_button['text'] = 'Not Found'


    def start_key_selection(self,title):
        self.select_button['text'] = "Bir tuşa bas"
        if self.new_win.winfo_exists():
            self.new_win.bind("<KeyPress>", lambda event: self.on_key_press(event, title))

    def on_close(self):
        self.is_window_open = False
        try:
            self.number_window.destroy()
            self.new_win.destroy()  # Pencereyi kapat

        except AttributeError:
            self.new_win.destroy()


    def PotionSaveButton(self,title):
        self.hp = self.hpSlider.get()
        self.mp = self.mpSlider.get()
        state = "Aktif" if self.switch_state else "Pasif"
        self.update_temp_data("potSet", {"Hp": self.hp, "Mp": self.mp, "state": state})  # Geçici veri ekleme
        self.save_to_json()
        self.new_win.attributes("-topmost", 0)
        messagebox.showinfo(title='Succes!', message=f"{title}'Ayarları Kaydedildi!")
        self.on_close()

    def RestoreSaveButton(self,title):
        otoLocation = self.otoLocation['text']
        Manuel = self.resManuel['text']
        state = "Aktif" if self.switch_state else "Pasif"
        tus = self.select_button["text"]
        manuel = self.Restorevar.get()

        self.update_temp_data("restoreSet", {"otoLocation": otoLocation, "Manuel": Manuel,"key":tus , "state": state , 'manuel_koordinat':manuel})  # Geçici veri ekleme
        self.save_to_json()
        self.new_win.attributes("-topmost", 0)
        messagebox.showinfo(title='Succes!', message=f"{title}'Ayarları Kaydedildi!")
        self.on_close()

    def slaytSave(self,title):
        tus = self.select_button["text"]
        state = "Aktif" if self.switch_state else "Pasif"

        self.update_temp_data("Slayt",{"key": tus,"state": state})  # Geçici veri ekleme
        self.save_to_json()
        self.new_win.attributes("-topmost", 0)
        messagebox.showinfo(title='Succes!', message=f"{title}'Ayarları Kaydedildi!")
        self.on_close()

    def KalkanSave(self,title):
        tus = self.select_button["text"]
        state = "Aktif" if self.switch_state else "Pasif"
        kalkan = self.kuritek2['text']
        silah = self.kuritek1['text']
        inv = self.Itemvar.get()
        TwoHandle = self.TwohandleVar.get()

        self.update_temp_data("Kalkan",{"key": tus,"state": state,'kalkan':kalkan,'silah':silah,"inv":inv ,'Cift-El':TwoHandle})  # Geçici veri ekleme
        self.save_to_json()
        self.new_win.attributes("-topmost", 0)
        messagebox.showinfo(title='Succes!',message=f"{title}'Ayarları Kaydedildi!")
        self.on_close()




    def start_listening(self,title):
        if title == 'kalkan':
            self.kuritek2['text'] = "CTRL"

        elif title == 'silah':
            self.kuritek1['text'] = "CTRL"

        elif title == 'restore':
            self.resManuel['text'] = "CTRL"

        else:
            pass


        # Butona tıklandığında sadece bir kere tuşu dinlemeye başla
        self.new_win.bind('<Control_L>', lambda event: self.on_control_press(event,title))
        self.new_win.bind('<Control_R>', lambda event: self.on_control_press(event,title))

        # Butona tıklanmasının ardından tuş dinlemeyi durdur
        # self.button.config(state=tk.DISABLED)




    def load_from_json(self, filename="data.json"):
        """JSON dosyasından veriyi yükleyip geçici belleğe aktarır."""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                self.load_data = json.load(file)  # JSON'daki kayıtlı verileri yükle
                self.temp_data = self.load_data.copy()  # Geçici verileri yükle
        else:
            self.load_data = {}  # Dosya yoksa boş sözlük kullan
            self.temp_data = {}



    def save_to_json(self, filename="data.json"):
        """Geçici verileri, kayıtlı verilerle birleştirerek JSON'a kaydeder."""

        # Eğer potSet gibi bir anahtar varsa, onun içine yeni verileri ekleyelim
        for key, value in self.temp_data.items():
            if isinstance(value, dict):  # Eğer değer bir sözlükse (örn: 'potSet' içindeki Hp, Mp)
                if key in self.load_data and isinstance(self.load_data[key], dict):
                    self.load_data[key].update(value)  # Mevcut veriyi yeni değerlerle güncelle
                else:
                    self.load_data[key] = value  # Eğer anahtar yoksa, direkt ekle
            else:
                self.load_data[key] = value  # Eğer sözlük değilse direkt güncelle

        # Güncellenmiş verileri JSON dosyasına yaz
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.load_data, file, indent=4)



    def update_temp_data(self, key, value):
        """Geçici ayarları güncelleyen fonksiyon."""
        self.temp_data[key] = value




    def imagesCreate(self, imgPach):
        if not os.path.exists(imgPach):
            print(f"Hata: {imgPach} bulunamadı!")
            return None  # Geçersiz dosya yoluysa None döndür

        icon = Image.open(imgPach)
        icon = icon.resize((20, 20))  # 📌 Resmi yeniden boyutlandır
        icon = ImageTk.PhotoImage(icon)  # 📌 Tkinter için uygun formata dönüştür
        return icon  # 📌 İkonu geri döndür


    def toggle_switch(self):
        """Switch'in durumunu değiştir ve animasyonu uygula"""


        self.switch_state = not self.switch_state

        if self.switch_state:
            for x in range(2, 22, 3):  # Sağa kaydır
                self.switch_btn.place(x=x)
                self.switch_frame.update()
                self.switch_frame.after(5)
            self.switch_frame.config(style="SwitchOn.TFrame")  # Açık (Yeşil)
        else:
            for x in range(22, 2, -3):  # Sola kaydır
                self.switch_btn.place(x=x)
                self.switch_frame.update()
                self.switch_frame.after(5)
            self.switch_frame.config(style="SwitchOff.TFrame")  # Kapalı (Gri)



    def switchFonksiyonu(self):
        style = ttk.Style()
        style.configure("SwitchOff.TFrame", background="gray", relief="flat")
        style.configure("SwitchOn.TFrame", background="green", relief="flat")
        style.configure("SwitchButton.TLabel", background="white", relief="solid", borderwidth=1)

        # Switch başlangıç durumu
        self.switch_state = False


       # Switch çerçevesi
        self.switch_frame = ttk.Frame(self.top_frame, width=45, height=20, style="SwitchOff.TFrame",cursor='hand2')
        self.switch_frame.pack( side="left",padx=5)

        # Hareket eden düğme
        self.switch_btn = ttk.Label(self.switch_frame, text="", style="SwitchButton.TLabel")
        self.switch_btn.place(relx=0.001,rely=0.001,relwidth=0.5,relheight=0.9)

        # Switch'e tıklama olayı ekle
        self.switch_frame.bind("<Button-1>", lambda e: self.toggle_switch())
        self.switch_btn.bind("<Button-1>", lambda e: self.toggle_switch())


    def update_hp_label(self, value):
        """HP Slider değeri değiştikçe güncellenir"""
        self.value_text.config(text=f"% {int(float(value) * 100)}")

    def update_mp_label(self, value):
        """HP Slider değeri değiştikçe güncellenir"""
        self.value_text2.config(text=f"% {int(float(value) * 100)}")



    def create_window(self, boyut , imgPach , title="Tuş Seçici", content_type=None):
        if self.is_window_open:
            print(f"{title} penceresi zaten açık!")
            return

        if not os.path.exists(imgPach):
            print(f"Hata: {imgPach} bulunamadı!")
            return


        self.is_window_open = True
        self.new_win = Toplevel(self.master)
        self.new_win.title(title)

        self.TitleImg = self.imagesCreate(imgPach)

        self.new_win.attributes("-topmost", 1)
        self.new_win.configure(bg="#2b2b2b")
        self.new_win.overrideredirect(True)

        # 📌 Mevcut pencerenin (self.master) konumunu ve boyutunu al
        self.master.update_idletasks()  # Pencere bilgilerini güncelle
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # 📌 Yeni pencerenin boyutları
        win_width = boyut[0]
        win_height = boyut[1]

        # 📌 Yeni pencerenin konumunu hesapla (Ana pencerenin ortasına getir)
        new_x = master_x + (master_width - win_width) // 2
        new_y = master_y + (master_height - win_height) // 2

        # 📌 Pencereyi belirlenen konumda aç
        self.new_win.geometry(f"{win_width}x{win_height}+{new_x}+{new_y}")


        self.top_frame = tk.Frame(self.new_win, bg="#2b2b2b",bd=2, relief="solid")
        self.top_frame.pack(fill='x')

        # Alt Çerçeve (Geri kalan boşluğu dolduracak)
        self.Bodyframe = tk.Frame(self.new_win, bg="#2b2b2b", bd=2, relief="solid")
        self.Bodyframe.pack(fill="both", expand=True , pady=(2, 2))  # Sayfanın geri kalanını kaplar


        self.switchFonksiyonu()



        exit_button = tk.Button(self.top_frame,width= 3 , text="X", fg="red" ,bg="#2b2b2b", cursor="hand2", command=self.on_close)
        exit_button.pack(side="right",padx=3)

        #new window başlıkları
        titleAndImgt = ttk.Label(self.top_frame,text=content_type,image=self.TitleImg,
                                 compound="left",  # Resmi sol tarafa alır, yazı sağda olur
                                 background="#2b2b2b",foreground='white')

        titleAndImgt.pack(anchor='center',pady=5)



        self.show_content(content_type,imgPach,title)

    def select_number(self,number,title):
        """Kullanıcının seçtiği sayıyı göster"""
        #messagebox.showinfo("Seçilen Değer", f"Seçtiğiniz sayı: {number}")
        print(f"Title :{title}\nSkil_bar :{number}")
        self.update_temp_data("potSet",
                              {title: number})  # Geçici veri ekleme
        self.save_to_json()
        self.number_window.destroy()  # Pencereyi kapat

    def open_number_selector(self,title):
        # 📌 Mevcut pencerenin (self.master) konumunu ve boyutunu al
        self.master.update_idletasks()  # Pencere bilgilerini güncelle
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # 📌 Yeni pencerenin boyutları
        barX = 50
        barY = 420

        # 📌 Yeni pencerenin konumunu hesapla (Ana pencerenin ortasına getir)
        new_x = master_x + (master_width - barX) // 2
        new_y = master_y + (master_height - barY) // 2
        new_x = new_x-150


        """Sayı seçim penceresini aç"""
        self.number_window = tk.Toplevel(self.master)
        self.number_window.geometry(f"{barX}x{barY}+{new_x}+{new_y}")  # Dar ve uzun pencere
        self.number_window.attributes("-topmost", 1)
        self.number_window.configure(bg="#2b2b2b")
        self.number_window.overrideredirect(True)

        for num in range(1, 10):  # 1'den 9'a kadar butonları ekle
            btn = ttk.Button(self.number_window, text=str(num), width=5,cursor="hand2",
                            command=lambda n=num: self.select_number(n,title=title))
            btn.pack(pady=5,padx=10)

        # 0 en son sıraya eklenecek
        btn_zero = ttk.Button(self.number_window, text="0", width=5,cursor="hand2",
                             command=lambda: self.select_number(0,title=title))
        btn_zero.pack(pady=5,padx=10)




    def show_content(self, content_type,pach,title):

        """Pencerenin içeriğini değiştiren fonksiyon."""
        # Önce frame içeriğini temizleyelim
        for widget in self.Bodyframe.winfo_children():
            widget.destroy()

        if content_type == "Item-Change":
            self.ItemState = self.load_data.get('Kalkan', {}).get('state', False)
            self.ItemKey = self.load_data.get('Kalkan', {}).get('key', 'Tuş Seç')

            self.kalkanLocat = self.load_data.get('Kalkan', {}).get('kalkan', 'Seç')
            self.silahLocat = self.load_data.get('Kalkan', {}).get('silah', 'Seç')
            self.Inv = self.load_data.get('Kalkan', {}).get('inv', False)
            self.TwoHandle = self.load_data.get('Kalkan', {}).get('Cift-El', False)


            if self.ItemState == "Aktif":
                self.toggle_switch()



            self.select_button = ttk.Button(self.Bodyframe, text=self.ItemKey,
                                            command=lambda: self.start_key_selection(title=title),
                                            style="Custom.TButton", cursor="hand2")
            self.select_button.pack(side="top",anchor="w", pady=5, padx=5)  # Tuş seçme butonu yerleştir



            TekkoordinatFrame = tk.LabelFrame(self.Bodyframe, text="Options", bg="#2b2b2b", fg='white')
            TekkoordinatFrame.pack(fill="both", expand=True, pady=5, padx=5)




            tk.Label(TekkoordinatFrame, text="Sol-El", bg="#2b2b2b", fg='white').grid(row=0, column=0, padx=2)

            tk.Label(TekkoordinatFrame, text="Kalkan", bg="#2b2b2b", fg='white').grid(row=0, column=2, padx=2)

            self.kuritek1 = ttk.Button(TekkoordinatFrame, text=self.silahLocat, command=lambda :self.start_listening(title='silah'), cursor="hand2",
                                       style="Custom.TButton")
            self.kuritek1.grid(row=1, column=0,padx=3)

            #tk.Label(TekkoordinatFrame, text="<>", bg="#2b2b2b", fg='white').grid(row=1, column=1, padx=2)

            self.kuritek2 = ttk.Button(TekkoordinatFrame, text=self.kalkanLocat, command= lambda :self.start_listening(title='kalkan'), cursor="hand2",
                                       style="Custom.TButton")
            self.kuritek2.grid(row=1, column=2)

            self.Itemvar = tk.BooleanVar(value=self.Inv)
            self.TwohandleVar = tk.BooleanVar(value=self.TwoHandle)

            # TTK Checkbutton oluştur
            check = ttk.Checkbutton(TekkoordinatFrame, text="İnventory Aç/kapa", variable=self.Itemvar, cursor = "hand2",
                                              style="TCheckbutton")
            check.grid(row=2, column=0,padx=3,pady=15)

            checkTwohandle = ttk.Checkbutton(TekkoordinatFrame, text="Çift-El", variable=self.TwohandleVar, cursor="hand2",
                                    style="TCheckbutton")
            checkTwohandle.grid(row=2, column=1, padx=3, pady=3)




            btnFrame = tk.Frame(self.Bodyframe, bg="#2b2b2b")
            btnFrame.pack(fill="both", expand=True, pady=(2, 2))

            self.ItemButton = ttk.Button(btnFrame, text="Kaydet", cursor="hand2", style="Custom.TButton",
                                          command=lambda: self.KalkanSave(title))
            self.ItemButton.pack(side='bottom',anchor="e", padx=5, pady=5)


        elif title == "Slayt":
            self.SlaytState = self.load_data.get('Slayt', {}).get('state', False)
            self.slaytKey = self.load_data.get('Slayt',{}).get('key','Tuş Seç')

            if self.SlaytState == "Aktif":
                self.toggle_switch()

            self.select_button = ttk.Button(self.Bodyframe, text=self.slaytKey, command= lambda :self.start_key_selection(title=title),
                                            style="Custom.TButton", cursor="hand2")
            self.select_button.pack(side="left", pady=5, padx=5)  # Tuş seçme butonu yerleştir


            self.SlaytButton = ttk.Button(self.Bodyframe, text="Kaydet", cursor="hand2", style="Custom.TButton",
                                        command=lambda: self.slaytSave(title))
            self.SlaytButton.pack(side='right', padx=5, pady=5)

        elif title == "restore":
            #self.restoreImg = self.imagesCreate("img/restore.png")
            self.restoreKey = self.load_data.get('restoreSet', {}).get('key', 'Tuş Seç')
            self.restoreManuel = self.load_data.get('restoreSet', {}).get('manuel_koordinat', False)

            self.select_button = ttk.Button(self.Bodyframe, text=self.restoreKey, command= lambda :self.start_key_selection(title=title),
                                            style="Custom.TButton", cursor="hand2")
            self.select_button.pack(side="top",anchor="w",pady=10,padx=10) # Tuş seçme butonu yerleştir

            OtobeginLocation = self.load_data.get('restoreSet', {}).get('otoLocation', 0)
            Location = self.load_data.get('restoreSet', {}).get('Manuel', 'Başlat')

            self.stateRest = self.load_data.get('restoreSet', {}).get('state', 0)


            if self.stateRest == "Aktif":
                self.toggle_switch()





            koordinatFrame = tk.LabelFrame(self.Bodyframe,text="koordinat", bg="#2b2b2b",fg='white')
            koordinatFrame.pack(fill="both", expand=True , padx=6)


            resT = ttk.Button(koordinatFrame, text='Oto',cursor="hand2", style="Custom.TButton",command=self.koordinat_al)
            resT.grid(row=0,column=2,padx=10,pady=10)

            tk.Label(koordinatFrame,text="Oto :", bg="#2b2b2b",fg="white").grid(row=0,column=0,padx=10,pady=10)

            self.otoLocation = ttk.Label(koordinatFrame,text=OtobeginLocation,width=9,relief="sunken")
            self.otoLocation.grid(row=0,column=1,padx=10,pady=10)

            tk.Label(koordinatFrame, text="Manuel :", bg="#2b2b2b", fg="white").grid(row=1, column=0, padx=10,
                                                                                               pady=10)

            self.resManuel = ttk.Button(koordinatFrame, text=Location, cursor="hand2", style="Custom.TButton",command=lambda :self.start_listening(title='restore'))
            self.resManuel.grid(row=1, column=1, padx=5, pady=1)

            self.Restorevar = tk.BooleanVar(value=self.restoreManuel)

            # TTK Checkbutton oluştur
            check = ttk.Checkbutton(koordinatFrame, text="Manuel", variable=self.Restorevar, cursor="hand2",
                                    style="TCheckbutton")
            check.grid(row=1, column=2, padx=3, pady=15)



            btnFrame = tk.Frame(self.Bodyframe, bg="#2b2b2b")
            btnFrame.pack(fill="both", expand=True, pady=(2, 2))

            self.resButton = ttk.Button(btnFrame, text="Kaydet", cursor="hand2",style="Custom.TButton",
                                      command=lambda: self.RestoreSaveButton(title=title))
            self.resButton.pack(side='bottom', anchor='e', padx=5, pady=5)


        elif title == "pot":

            self.hp_icon = self.imagesCreate(pach)
            self.mp_icon = self.imagesCreate("img/mp_pot.png")

            # JSON verisini çek
            pot = self.load_data.get('potSet', {}).get('Hp', 0)
            mana = self.load_data.get('potSet', {}).get('Mp', 0)
            self.statePot = self.load_data.get('potSet', {}).get('state', 0)

            if self.statePot == "Aktif":
                self.toggle_switch()



            self.value_text = tk.Label(self.Bodyframe, text=f'%{int(pot * 100)}', bg="#2b2b2b", fg="white")
            self.value_text.pack(side="top")
            potLabel = ttk.Button(self.Bodyframe, image=self.hp_icon,cursor="hand2", style="Custom.TButton",command=lambda :self.open_number_selector('HP_bar'))
            potLabel.pack(side="top", anchor="w", padx=10, pady=5)
            self.hpSlider = ttk.Scale(self.Bodyframe, from_=0, to=1, orient="horizontal",value=pot, command=self.update_hp_label)
            self.hpSlider.pack(fill="x",padx=10)


            self.value_text2 = tk.Label(self.Bodyframe, text=f'%{int(mana * 100)}', bg="#2b2b2b", fg="white")
            self.value_text2.pack(side="top")
            HP_potLabel = ttk.Button(self.Bodyframe, image=self.mp_icon,cursor="hand2", style="Custom.TButton",command=lambda :self.open_number_selector('MP_bar'))
            HP_potLabel.pack(side="top", anchor="w", padx=10, pady=5)
            self.mpSlider = ttk.Scale(self.Bodyframe, from_=0,value=mana, to=1, orient="horizontal", command=self.update_mp_label)
            self.mpSlider.pack(fill="x",padx=10)

            potionButton = ttk.Button(self.Bodyframe,text="Kaydet",cursor="hand2", style="Custom.TButton",command= lambda :self.PotionSaveButton(title=title))
            potionButton.pack(side='bottom',anchor='e',padx=5,pady=5)




        else:
            tk.Label(self.new_win, text="Bilinmeyen İçerik!", bg="red", fg="white").pack(pady=20)




