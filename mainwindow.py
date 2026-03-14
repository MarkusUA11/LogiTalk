from customtkinter import *
import threading
import base64
import io
import os
from PIL import Image
from socket import socket, AF_INET, SOCK_STREAM

class MainWindow(CTk):
    def __init__(self,sock, username):
        super().__init__()

        self.sock = sock
        self.username = username
        self.geometry('400x600')
        self.title("Chat Cilent")


        self.geometry('400x600')
        self.title("Chat Client")


        # Меню
        self.label = None
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -20
        self.btn = CTkButton(self, text='▶️', width=30,command =  self.toggle_menu)
        self.btn.place(x=0, y=0)




        # Основне поле чату
        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.place(x=0, y=0)




        # Поле введення та кнопки
        self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', height=40)
        self.message_entry.place(x=0, y=0)
        self.send_button = CTkButton(self, text='>', width=50, height=40)
        self.send_button.place(x=0, y=0)




        self.open_img_button = CTkButton(self, text='📂', width=50, height=40)
        self.open_img_button.place(x=0, y=0)




        self.adaptive_ui()
       


    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width() - 20,
                                    height=self.winfo_height() - 40)
        self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)
        self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_entry.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - 110)
        self.open_img_button.place(x=self.winfo_width()-105, y=self.send_button.winfo_y())




        self.after(50, self.adaptive_ui)



    def toggle_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= 1
            self.btn.configure(text = "▶️")
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= 1
            self.btn.configure(text = "MENU")
            self.show.menu()


            self.label = CTkLabel(self.menu_frame,placeholder_text="Дай нік")
            self.entry.pack()

            self.save.btn = CTkButton(self.menu_frame, text="download", command=self.save_name)
            self.save_btn.pack()

    def show_menu(self):
        self.menu_frame.configure(width = self.menu_frame.winfo() + self.speed_animate_menu)
        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.menu_frame.winfo_width() >= 60 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.label: self.label.destroy()
            if getattr(self, "entry",None): self.entry.destroy()
            if getattr(self, "save_btn",None): self.entry.destroy()

    def add_message(self,message, img=None):
        message_frame = CTkFrame(self.chat_fleld, fg_color="gray")
        message_frame.pack(pady=5, anchor='w')
        
        wrapleng_size = self.winfo_width() - self.menu_frame.winfo_width() - 40

        if not img:
            CTkLabel(message_frame, text=message, wraplength=wrapleng_size, text_color='white'
                    ,justify='left').pack(padx=10,pady=5)
        else:
            CTkLabel(message_frame, text=message, wraplength=wrapleng_size,text_color='white', image=img, compound='top',justify='left').pack(padx=10,pady=5)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message(f"(self.username): {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
            self.message_entry.delete(0, END)
    
    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode(errors='ignore')

                while "\n" in buffer:
                    line, buffer = buffer.split('\n',1)
                    self.handle_line(line.strip())
            except:
                break
            self.sock.close()

    def handle_line(self,line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]

        if msg_type == "TEXT":
            if len(parts) == 3:
               author = parts[1]
               message = parts[2]
               self.add_message(f"{author}:{message}")
            elif msg_type == "IMAGE":
                if len(parts) >= 4:
                    author = parts[1]
                    filename = parts[2]
                    b64_img = parts[3]
                    try:
                        img_data = base64.b64decode(b64_img)
                        pil_img = Image.open(io).BytesIO((img_data))
                        ctk_img  = CTkImage(pil_img, size=(300,300))
                        self.add_message(f"{author} надіслав(ла) зображення: {filename}",img=ctk_img)
                    except Exception as e:
                        self.add_message(f"Помилка відображення зображення: {e}")
            else:
                 self.add_message(line)

        def open_image(self):
            file_name = filedialog.askopenfilename()
            if not file_name:
                return
            try:
                with open(file_name, "rb") as f:
                    raw = f.read
                b64_data = base64.b64encode(raw).decode()
                short_name = os.path.basename(file_name)
                data = f"IMAGE@{self.username}@{short_name}@{b64_data}\n"
                self.sock.sendall(data.encode())
                self.add_message("", CTkImage(light_image=Image.open(file_name),size=(300,300)))
            except Exception as e:
                self.add_message(f"Не вдалось надіслати зображення: {e}") 



main = MainWindow()
main.mainloop()