import ctypes
import threading
import time
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import keyboard
from PIL import Image, ImageTk
import os
from Options import KeySelectorApp


class KurianWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)
        self.configure(bg="#1e1e1e")

        self.user32 = ctypes.windll.user32
        self.restoreControl = False
        self.kalkanControl = False
        self.key_pressed = False
        self.key_pressed_kalkan = False
        self.keyPotion = False
        self.is_running = False
        self.tus_durumlari = {}
        self.key_app = None  # KeySelectorApp nesnesi burada tanımlanacak
        self.create_styles()


    def createFrame(self,frame,location):
       self.location = location #2
       self.ButtonsOptions(frame)


    def create_styles(self):
        """Tkinter Stillerini Tanımla"""
        style = ttk.Style()
        style.theme_use("clam")

        # Buton Stili
        style.configure("Custom.TButton",
                        background="#2b2b2b",
                        foreground="white",
                        font=("Arial", 10),
                        padding=(5, 2))

        style.map("Custom.TButton",
                  background=[("active", "#444"), ("pressed", "#666")],
                  foreground=[("active", "white"), ("pressed", "white")])

        # LabelFrame Stili
        style.configure("Custom.TLabelframe", background="#1e1e1e")
        style.configure("Custom.TLabelframe.Label", background="#1e1e1e", foreground="white")

        # Checkbutton ve Slider arka planlarını koyulaştır
        style.configure("TCheckbutton", background="#2b2b2b", foreground="white")
        style.configure("TCheckbutton2", background="#1e1e1e", foreground="white")
        style.map("TCheckbutton",
                  background=[("active", "#444")])
        style.configure("TScale", background="#1e1e1e")

        style.configure("Start.TButton", background="#28a745", foreground="white", font=("Arial", 10, "bold"))
        style.configure("Stop.TButton", background="#dc3545", foreground="white", font=("Arial", 10, "bold"))



    def pencereyi_getir(self):
        """F11'e basılınca pencereyi geri getir"""
        self.master.deiconify()


    def durdur_tus_dinleme(self):
        keyboard.unhook_all()  # Tüm tuş dinleyicilerini durdurur
        keyboard.add_hotkey("F11",self.pencereyi_getir)






    def tus_kontrol(self,key, action):
        if action == "press":
            if not self.tus_durumlari.get(key, False):
                self.tus_durumlari[key] = True
                self.ozel_fonksiyon(key)
        elif action == "release":
            self.tus_durumlari[key] = False
            self.reset_modifier_keys()


    def basilan_tuslari_dinle(self,restoreKey, kalkanKey, slaytKey):
        # Klavye olaylarını arka planda dinle (threading ile donmaları önlüyoruz)
        def klavye_dinleyici():
            keyboard.on_press_key(restoreKey.lower(), lambda _: self.tus_kontrol('restore', "press"))
            keyboard.on_release_key(restoreKey.lower(), lambda _: self.tus_kontrol('restore', "release"))

            keyboard.on_press_key(kalkanKey.lower(), lambda _: self.tus_kontrol('kalkan', "press"))
            keyboard.on_release_key(kalkanKey.lower(), lambda _: self.tus_kontrol('kalkan', "release"))


            keyboard.on_press_key(slaytKey.lower(), lambda _: self.tus_kontrol('slayt', "press"))
            keyboard.on_release_key(slaytKey.lower(), lambda _: self.tus_kontrol('slayt', "release"))

            keyboard.wait()

        thread = threading.Thread(target=klavye_dinleyici, daemon=True)
        thread.start()



    def toggle_start_stop(self):
        if self.is_running:
            self.start_stop_btn.config(text="Başlat", style="Start.TButton")
            self.is_running = False
            self.keyPotion = False

            self.durdur_tus_dinleme()
            print("Attack - Durduruldu!")

        else:
            self.start_stop_btn.config(text="Durdur", style="Stop.TButton")
            self.is_running = True



            print("Attack - Başlatıldı!")



    def create_button(self, frame, text, icon_path, command, row, column):
        """Buton Oluşturma Fonksiyonu"""
        if not os.path.exists(icon_path):
            print(f"Hata: {icon_path} bulunamadı!")
            return

        icon = Image.open(icon_path)
        icon = icon.resize((20, 20))
        icon = ImageTk.PhotoImage(icon)

        btn = ttk.Button(frame, text=text, image=icon, compound="left", command=command,
                         style="Custom.TButton", cursor="hand2")
        btn.image = icon  # Referans kaybetmemek için saklıyoruz
        btn.grid(row=row, column=column, padx=5, pady=5, sticky="ew")  # GENİŞLİK DİNAMİK OLACAK

        # Butonu listeye ekleyin
        if not hasattr(self, 'all_buttons'):
            self.all_buttons = []  # Eğer self.all_buttons yoksa, oluşturulacak
        self.all_buttons.append(btn)

    def ButtonsOptions(self,frame):
        # Opaklık Ayarları
        self.KurianFrame = frame

        def change_opacity(val):
            self.master.attributes("-alpha", float(val))

        def toggle_always_on_top():
            self.master.attributes("-topmost", always_on_top_var.get())


        self.opt = ttk.Frame(self.KurianFrame, style="Custom.TLabelframe", borderwidth=0, relief="flat")
        self.opt.pack(fill="x", pady=(20, 5))


        self.options_frame = ttk.LabelFrame(self.KurianFrame, text="Options", style="Custom.TLabelframe")
        self.options_frame.pack(fill="x", pady=(10, 5))

        self.opt_buttons = ttk.Frame(self.KurianFrame, style="Custom.TLabelframe", borderwidth=0, relief="flat")
        self.opt_buttons.pack(side="bottom", fill="x", padx=10, pady=10)




        buttons_options = [
            (" Restore", "img/restore.png", self.RestoreWin),
            (" Slayt", "img/slayt.png", self.SlaytWin),
            (" Kalkan", "img/kalkan.png", self.ItemWin),
            ("HP-MP", "img/pot.png", self.oto_pot)
        ]


        for idx, (btn_text, icon_path, command) in enumerate(buttons_options):
            row = idx // 4  # 3'erli satır oluştur
            column = idx % 4
            self.create_button(self.options_frame, btn_text, icon_path, command, row, column)

        tk.Label(self.opt, text="Saydamlık:", fg="white", bg="#1e1e1e").pack(side="left")

        opacity_slider = ttk.Scale(self.opt, from_=0.3, to=1.0, orient="horizontal",
                                   command=change_opacity, length=150, style="TScale",cursor = "hand2")
        opacity_slider.set(1.0)
        opacity_slider.pack(side="left", padx=10)

        always_on_top_var = tk.BooleanVar()
        always_on_top_check = tk.Checkbutton(self.opt,
                                              text="Her Zaman Üstte",
                                              variable=always_on_top_var,
                                              command=toggle_always_on_top,
                                              cursor = "hand2",
                                              bg="#1e1e1e",  # Arka plan koyu tema
                                              fg="white",  # Yazı rengi beyaz
                                              selectcolor="gray",  # ✓ işaretinin arka planını gri yap
                                              activeforeground="white")
        always_on_top_check.pack(side="right", padx=10)

        # Başlat/Durdur butonu
        self.start_stop_btn = ttk.Button(self.opt_buttons, text="Başlat",cursor="hand2", style="Start.TButton",
                                         command=self.toggle_start_stop)
        self.start_stop_btn.pack(side="right", padx=1, pady=1)

        # Başlat/Durdur butonu
        self.InfoLabel= tk.Label(self.opt_buttons, text="TEST version...",
                                 bg="#1e1e1e",  # Arka plan koyu tema
                                 fg="pink",  # Yazı rengi beyaz
                                 font="verdana 10 bold"
                                         )
        self.InfoLabel.pack(side="left", padx=1, pady=1)


        # Başlat/Durdur durumu (False = Başlat, True = Durdur)
        self.is_running = False

    def RestoreWin(self):
        self.open_window("restore", boyut=(300, 250), pach="img/restore.png" , content_type= "restore")

    def SlaytWin(self):
        self.open_window("Slayt",boyut=(300,100),pach="img/slayt.png", content_type="Slayt")

    def ItemWin(self):
        self.open_window("Item-Change", boyut=(300, 250), pach="img/change.png", content_type="Item-Change")


    def oto_pot(self):
        self.open_window("pot",boyut=(300,250),pach="img/pot.png",content_type="Oto Potion")

    def open_window(self, name, boyut, pach, content_type):
        if self.key_app is None:
            self.key_app = KeySelectorApp(self.master)
        self.key_app.create_window(title=name, boyut=boyut, imgPach=pach, content_type=content_type)



