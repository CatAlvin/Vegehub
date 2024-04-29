import tkinter as tk
from tkinter import ttk
from database import models as db_models
from database import utils as db_utils
import hashlib
from typing import Optional
import sv_ttk

import logging
from logger import logging_setup


class LoggingPage(tk.Tk):
    def __init__(self,
                 session: db_models.session,
                 theme: str = "light",
                 title: str = "Vegehub Admin Login"
                 ) -> None:
        
        super().__init__()
        
        # set session
        self.session = session
        
        # hashlib obj
        self.md5 = hashlib.md5()
        
        # logger
        self.logger = logging.getLogger(__name__)
        
        # set window size
        self.WIN_WIDTH = 400
        self.WIN_HEIGHT = 200
        self.resizable(0, 0)
        self.title(title)
        
        # set window position to center
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw-self.WIN_WIDTH) / 2
        y = (sh-self.WIN_HEIGHT) / 2
        self.geometry("%dx%d+%d+%d" %
                              (self.WIN_WIDTH, self.WIN_HEIGHT, x, y-70))
        
        sv_ttk.set_theme(theme)
        self.accountName = tk.StringVar()
        self.password = tk.StringVar()
        self.accountName_label = ttk.Label(self, text="Username:")
        self.accountName_hint_label = ttk.Label(self)
        self.password_label = ttk.Label(self, text="Password:")
        self.password_hint_label = ttk.Label(self)
        self.hint_label = ttk.Label(self)
        self.accountName_entry = ttk.Entry(self,
                                            textvariable=self.accountName)
        self.password_entry = ttk.Entry(self, show="*",
                                         textvariable=self.password)
        self.signIn_button = ttk.Button(self, text="login", width=5)

    def is_account_exist(self, account_name: str) -> bool:
        res = self.session.query(db_models.Admin).filter_by(username=account_name).first()
        return res is not None

    def is_password_correct(self, account_name: str, password: str) -> bool:
        hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        res = self.session.query(db_models.Admin).filter(db_models.Admin.username == account_name).first()
        return res.password == hash_password
    
    def authorize(self, account_name: str, password: str) -> None:
        if self.is_account_exist(account_name):
            self.accountName_entry.state(["!invalid"])
            self.accountName_hint_label.config(text="√", foreground="green")
        else:
            self.accountName_entry.state(["invalid"])
            self.accountName_hint_label.config(text="X", foreground="red")
            self.hint_label.config(text="Account Not Exist!", foreground="red")
            return

        if self.is_password_correct(account_name, password):
            self.password_entry.state(["!invalid"])
            self.password_hint_label.config(text="√", foreground="green")
            self.hint_label.config(text="")
            
            self.logger.info(f"Admin '{account_name}' login successfully!")
            self.enter()
        else:
            self.password_entry.state(["invalid"])
            self.password_hint_label.config(text="X", foreground="red")
            self.hint_label.config(text="Password Incorrect!", foreground="red")
            self.password.set("")

    def place_components(self) -> None:
        # place components
        # account input
        self.accountName_label.place(x=self.WIN_WIDTH/2-130, y=37)
        self.accountName_hint_label.place(x=self.WIN_WIDTH/2+130, y=37)
        self.accountName_entry.place(x=self.WIN_WIDTH/2-60, y=30)
        
        # password input
        self.password_label.place(x=self.WIN_WIDTH/2-130, y=77)
        self.password_hint_label.place(x=self.WIN_WIDTH/2+130, y=77)
        self.password_entry.place(x=self.WIN_WIDTH/2-60, y=70)
        
        # hint
        self.hint_label.place(x=self.WIN_WIDTH/2+20, y=165)
        
        # sign in button
        self.signIn_button.place(x=self.WIN_WIDTH/2+60, y=120)

    def bind_them(self) -> None:
        self.signIn_button.config(command=lambda: self.authorize(
            self.accountName.get(), self.password.get()))

    def enter(self) -> None:
        # self.cursor.close()
        # self.mysql_conn.close()
        # self.destroy()
        # 进入主界面
        print("进入主界面")

    def exit(self) -> None:
        self.destroy()

    def run(self) -> None:
        self.place_components()
        self.bind_them()
        self.protocol("WM_DELETE", self.exit)
        self.mainloop()