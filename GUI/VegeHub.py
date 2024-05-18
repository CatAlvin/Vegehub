from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="nsew") 
        self.master = master
        self.create_widgets()
        self.set_function_frame()
        self.show_lable()

    def create_widgets(self):
        self.columnconfigure(0, weight=0) 
        self.columnconfigure(1, weight=10) 
        
        # create the function frame
        self.rowconfigure(0, weight=1)
        self.functionFrame = Frame(self, background="LightGreen")
        self.functionFrame.grid(row=0, column=0, sticky="nsew")

        # create the show frame
        self.showFrame = Frame(self)
        self.showFrame_title = Frame(self.showFrame, background="LemonChiffon")
        self.showFrame_show = Frame(self.showFrame, background="Lightyellow")
        self.showFrame.grid(row=0, column=1, sticky="nsew")
        
        # set the show frame
        self.showFrame_title.pack(side=TOP, fill=BOTH)
        self.showFrame_show.pack(side=TOP,expand=True, fill=BOTH)
    
    def set_function_frame(self):
        # set the title of the function frame
        titleFont = Font(family=" times new roman ", size="30",weight="bold")
        Ftitle = Label(self.functionFrame, text="VegeHub", bg = "ForestGreen", fg="white", font=titleFont)
        
        # set the functions
        # function 1
        HomeButton = Button(self.functionFrame, text="Home", bg="LightGreen",relief=SUNKEN,command=self.show_home)
        
        # function 2
        VegeButton = Button(self.functionFrame, text="Vegetable Variety", bg="LightGreen",relief=SUNKEN,command=self.show_vege)
        
        # function 3
        PriceButton = Button(self.functionFrame, text="Vegetable Price",bg="LightGreen",relief=SUNKEN,command=self.show_price)
        
        # function 4
        MarketButton = Button(self.functionFrame, text="Vegetable Market",bg="LightGreen",relief=SUNKEN,command=self.show_market)
        
        # function 5
        ShopButton = Button(self.functionFrame, text="My Shop", bg="LightGreen",relief=SUNKEN,command=self.show_shop)
        
        # pack the widgets
        Ftitle.pack(side=TOP, fill=X)
        HomeButton.pack(side=TOP, fill=X)
        VegeButton.pack(side=TOP, fill=X)
        PriceButton.pack(side=TOP, fill=X)
        MarketButton.pack(side=TOP, fill=X)
        ShopButton.pack(side=TOP, fill=X)
        
    def clear_showFrame(self):
        """Clear the showFrame."""
        for widget in self.showFrame_show.winfo_children():
            widget.destroy()
            
        for widget in self.showFrame_title.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_showFrame()
        
        title_lable_home = Label(self.showFrame_title, text="   HOME", bg="LemonChiffon", font=("times new roman",20))
        title_lable_home.pack(side=LEFT)
        
        label = Label(self.showFrame_show, text="1", bg="PaleTurquoise")
        label.pack(expand=True)
        
    def show_vege(self):
        self.clear_showFrame()
        
        title_lable_vege = Label(self.showFrame_title, text="   Vegetable Variety", bg="LemonChiffon", font=("times new roman",20))
        title_lable_vege.pack(side=LEFT)
        
        label = Label(self.showFrame_show, text="2", bg="PaleTurquoise")
        label.pack(expand=True)
        
    def show_price(self):
        self.clear_showFrame()
        
        title_lable_price = Label(self.showFrame_title, text="   Vegetable Price", bg="LemonChiffon", font=("times new roman",20))
        title_lable_price.pack(side=LEFT)
        
        label = Label(self.showFrame_show, text="3", bg="PaleTurquoise")
        label.pack(expand=True)
        
    def show_market(self):
        self.clear_showFrame()
        
        title_lable_market = Label(self.showFrame_title, text="   Vegetable Market", bg="LemonChiffon", font=("times new roman",20))
        title_lable_market.pack(side=LEFT)
        
        label = Label(self.showFrame_show, text="4", bg="PaleTurquoise")
        label.pack(expand=True)
    
    def show_shop(self):
        self.clear_showFrame()
        
        title_lable_shop = Label(self.showFrame_title, text="   My Shop", bg="LemonChiffon", font=("times new roman",20))
        title_lable_shop.pack(side=LEFT)
               
        label = Label(self.showFrame_show, text="5", bg="PaleTurquoise")
        label.pack(expand=True)
    
    def show_lable(self):
        title_label = Label(self.showFrame_title, text="WELECOM TO VEGEHUB", bg="LemonChiffon", font=("times new roman",30))
        
        title_label.pack(side=TOP, fill=X)
    
if __name__ == '__main__':
    root = Tk()
    root.geometry("900x600+300+90")
    root.title("VegeHub")
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    app = Application(master=root)

    root.mainloop()