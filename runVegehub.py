from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from GUI.VegeHub import Application
if __name__ == '__main__':
    root = Tk()
    root.geometry("900x600+300+90")
    root.title("VegeHub")
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    app = Application(master=root)

    root.mainloop()