from customtkinter import*

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x50")
        self.title("LogiTalk")
        #========= ВІДЖЕТИ ==========
        self.menu_btn = CTkButton(self,width=200,text="menu",corner_radius=0)
        self.menu_btn.place(x=0, y=0)

        self.menu_frame = CTkFrame(self,width=200,height=500,corner_radius=0)
        self.menu_frame.place(x=0, y=0)

        self.chat_frame = CTkScrollableFrame(self)
        self.chat_frame.place(x=0, y=0)

        self.send_frame = CTkFrame(self)
        self.send_frame.place(x=0, y=0)

        self.message_entry = CTkEntry(self.send_frame)
        self.send_frame.place(x=0, y=0)

        #=======  АДАПТИВНІСТЬ ============
        self.adaptive_ui()
    def adaptive_ui(self):
        self.menu_frame.place(x = 0, y = self.menu_btn.winfo_height())
        self.after(50,self.adaptive_ui)
    


    main = MainWindow()
    main.mainloop()