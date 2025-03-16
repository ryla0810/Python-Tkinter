import subprocess
import threading
import time
import os
import datetime
import sys
import tkinter as tk
import keyboard
from PIL import Image, ImageTk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width = 535
        self.height = 230
        self.title("anaSayfa")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        self.overrideredirect(True)  # üst pencere görünümü kaldır
        self.center_window(self.width, self.height)
        self.UstMenu()
        self.ComeBackMinimize()
        self.running = True

        # test_frame'i tanımla, içeriği dinamik olarak genişleyebilir
        self.test_frame = tk.Frame(self, bg="#1e1e1e")
        self.test_frame.pack(fill="both",padx=10, expand=True)  # Genişlemeye izin ver


        #---------------------------------- Karşılama yazısı Değişen renkler -----------------------------------------------------
        self.wellcome_label = tk.Label(self.test_frame, text='Hoş Geldiniz!',
                                       fg="white", bg="#1e1e1e",
                                       font="Algerian 20 bold")
        self.wellcome_label.pack(expand=True)  # Ortalamak için

        self.color_index = 0
        self.colors = ["red", "cyan", "yellow", "green", "magenta", "orange"]
        self.iconbitmap('img/newIcon.ico')

        #------------------------------------------------------------------------------------------------------------------------
        threading.Thread(target=self.menu_click,daemon=True).start()
        self.change_color()

    def change_color(self):
        """Yazının rengini değiştirir, eğer çalışma aktifse ve label hala varsa."""
        if self.running:
            try:
                if self.wellcome_label.winfo_exists():  # Label silinmiş mi?
                    self.wellcome_label.config(fg=self.colors[self.color_index])
                    self.color_index = (self.color_index + 1) % len(self.colors)
                    self.after(500, self.change_color)  # 500ms sonra tekrar çalıştır
            except:
                self.running = False  # Eğer label yoksa döngüyü durdur

    def menu_click(self):
        from Menu import KurianWindow

        time.sleep(1)
        location = (self.winfo_x(), self.winfo_y())
        for widget in self.test_frame.winfo_children():
            widget.destroy()


        self.kurian_page = KurianWindow(self)
        self.kurian_page.createFrame(self.test_frame,location)
        self.kurian_page.pack(fill="both", expand=True)
        # Yükleme animasyonunu durdur

    

    def start_move(self,event):
        self.x = event.x
        self.y = event.y

    def stop_move(self,event):
        self.x = None
        self.y = None

    def on_move(self,event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def center_window(self, width=300, height=150):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def ComeBackMinimize(self):
        """F11 tuşunu sürekli dinleyen fonksiyon"""
        keyboard.add_hotkey("F11", self.deiconify)  # F11'e her basıldığında çağır

    def UstMenu(self):
        self.menu_frame = tk.Frame(self, bg="#2b2b2b", height=40)
        self.menu_frame.pack(fill="x")
        self.menu_frame.bind("<ButtonPress-1>", self.start_move)
        self.menu_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.menu_frame.bind("<B1-Motion>", self.on_move)

        icon = Image.open('img/newIcon.ico')
        icon = icon.resize((70, 30))
        icon = ImageTk.PhotoImage(icon)



        exit_button = tk.Button(self.menu_frame, text="X", cursor="hand2", fg="red", bg="#2b2b2b",
                                font=("Arial", 10, "bold"), bd=0,
                                command=self.quit)
        exit_button.pack(side="right", padx=10, pady=5)

        minimize_button = tk.Button(self.menu_frame, text="_", cursor="hand2", fg="white", bg="#2b2b2b",
                                    font=("Arial", 10, "bold"), bd=0,
                                    command=lambda: self.withdraw())
        minimize_button.pack(side="right", padx=10, pady=5)

        iconMenu = tk.Label(self.menu_frame,image=icon , cursor="hand2",bg="#2b2b2b")
        iconMenu.image = icon
        iconMenu.pack(side="left", padx=1, pady=1)


    def location(self):
        self.locations = (self.winfo_x(),self.winfo_y())



if __name__ == "__main__":
    root = MainWindow()

    root.mainloop()

