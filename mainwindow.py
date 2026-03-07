from customtkinter import *


class MainWindow(CTk):
    def __init__(self):
        super().__init__()


        self.geometry('400x600')
        self.title("Chat Client")


        # Меню
        self.label = None
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -20
        self.btn = CTkButton(self, text='▶️', width=30)
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

main = MainWindow()
main.mainloop()

    