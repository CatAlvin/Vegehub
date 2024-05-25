from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import database.api as db_api
import tkinter.ttk
import time
import datetime
from tkinter import font
import turtle as T
import random
import time


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="nsew")
        self.master = master
        self.create_widgets()
        self.set_function_frame()
        self.show_home()

    # *创建组件
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
        self.showFrame_show = Frame(self.showFrame, background="lightyellow")
        self.showFrame.grid(row=0, column=1, sticky="nsew")

        # set the show frame
        self.showFrame_title.pack(side=TOP, fill=X)
        self.showFrame_show.pack(side=TOP, expand=True, fill=BOTH)
        """
        # create the notebook
        self.vege_notebook = tkinter.ttk.Notebook(self.master)  # 将小部件添加到窗口的主框架上
        self.vege_information_frame = Frame(self.vege_notebook, bg="lightyellow")
        self.vege_notebook.add(self.vege_information_frame, text="Vegetable Information")
        self.vege_Modification_frame = Frame(self.vege_notebook, bg="lightyellow")
        self.vege_notebook.add(self.vege_Modification_frame, text="Vegetable Modification")
        
        self.vege_information_frame.pack(expand=True, fill=BOTH)
        self.vege_Modification_frame.pack(expand=True, fill=BOTH)
        """

    # *设置功能框架
    def set_function_frame(self):
        # set the title of the function frame
        titleFont = Font(family=" times new roman ", size="30", weight="bold")
        Ftitle = Label(
            self.functionFrame,
            text="VegeHub",
            bg="ForestGreen",
            fg="white",
            font=titleFont,
        )

        # set the functions
        # function home
        HomeButton = Button(
            self.functionFrame,
            text="Home",
            bg="LightGreen",
            relief=SUNKEN,
            command=self.show_home,
        )

        # function vegetable information
        InformationButton = Button(
            self.functionFrame,
            text="Vegetable Information",
            bg="LightGreen",
            relief=SUNKEN,
            command=self.show_information,
        )

        # function vegetable market
        MarketButton = Button(
            self.functionFrame,
            text="Vegetable Market",
            bg="LightGreen",
            relief=SUNKEN,
            command=self.show_market,
        )

        # function my shop
        ShopButton = Button(
            self.functionFrame,
            text="My Shop",
            bg="LightGreen",
            relief=SUNKEN,
            command=self.show_shop,
        )

        # pack the widgets
        Ftitle.pack(side=TOP, fill=X)
        HomeButton.pack(side=TOP, fill=X)
        InformationButton.pack(side=TOP, fill=X)
        MarketButton.pack(side=TOP, fill=X)
        ShopButton.pack(side=TOP, fill=X)

    # *清空showFrame
    def clear_showFrame(self):
        """Clear the showFrame."""
        for widget in self.showFrame_show.winfo_children():
            widget.destroy()

        for widget in self.showFrame_title.winfo_children():
            widget.destroy()

    def clear_showFrame_show(self):
        """Clear the showFrame."""
        for widget in self.showFrame_show.winfo_children():
            widget.destroy()

    # *更新评价信息
    def update_comment(self, df):
        # 清空当前内容
        for item in self.comment.get_children():
            self.comment.delete(item)

        # 插入新的数据
        for index, row in df.iterrows():
            self.comment.insert(
                "",
                "end",
                values=(row["review_text"], row["review_date"], row["compound"]),
            )

    # *展示主页管理页面
    def show_home(self):
        # clear the showFrame
        self.clear_showFrame()
        admin = "admin"  # 需要修改
        # set the hit title of the showFrame
        title_label_home = Label(
            self.showFrame_title,
            text="WELCOME TO VEGEHUB " + admin,
            bg="LemonChiffon",
            fg="ForestGreen",
            font=("times new roman", 30),
        )
        title_label_home.pack(side=TOP, fill=X)

        # *展示主页
        timeFrame = Frame(self.showFrame_show, bg="lightyellow")
        clockFrame = Frame(timeFrame, bg="Azure")

        # *展示用户数量
        # 获取用户
        self.customer_df = db_api.getCustomerDataFrame()
        # 计算用户数量
        customer_count = self.customer_df["name"].count()
        # 设置展示frame
        show_customer_frame = Frame(timeFrame, bg="cornsilk")
        show_customer_frame.pack(side=LEFT, fill=X)

        # 设置展示label
        customer_label = Label(
            show_customer_frame,
            bd=5,
            text="Customer Count: " + str(customer_count),
            bg="lightyellow",
            fg="goldenrod",
            font=("times new roman", 30),
            relief=SUNKEN,
        )
        customer_label.pack(side=TOP, fill=X, expand=True, padx=5)

        # define the function to update the time and date
        def update_time():
            current_time = time.strftime("%H:%M:%S")
            time_label.config(text=current_time)
            self.after_id_time = time_label.after(1000, update_time)

        # define the function to update the date
        def update_date():
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            date_label.config(text=current_date)
            self.after_id_date = date_label.after(
                86400000, update_date
            )  # 24 hours in milliseconds

        # set the font of the clock
        time_font = font.Font(family="Helvetica", size=48, weight="bold")
        date_font = font.Font(family="Helvetica", size=16)

        # create the widgets of the clock
        time_label = Label(clockFrame, font=time_font, bg="Azure", fg="orange")
        date_label = Label(clockFrame, font=date_font, bg="Azure", fg="orange")

        # pack the widgets of the clock
        time_label.pack(side=TOP)
        date_label.pack(side=TOP)

        # pack the widgets
        clockFrame.pack(side=RIGHT)
        timeFrame.pack(side=TOP, fill=X)

        # update the time and date
        update_time()
        update_date()

        # *展示用户评价
        # 获取评价
        self.reviews = db_api.getCustomerReviewsDataFrame()

        # create the review frame
        reviewFrame = Frame(self.showFrame_show, bg="white")
        commentFrame = Frame(reviewFrame, bg="Azure")

        # create the table to show the comments
        columns = ("#1", "#2", "#3")
        self.comment = tkinter.ttk.Treeview(
            commentFrame, columns=columns, show="headings"
        )

        # define the columns
        self.comment.heading("#1", text="Commends")
        self.comment.heading("#2", text="Date")
        self.comment.heading("#3", text="Value")

        # define the width of the columns
        self.comment.column("#1", anchor=W, stretch=NO, width=550)
        self.comment.column("#2", anchor=CENTER, stretch=NO, width=120)
        self.comment.column("#3", anchor=CENTER, stretch=NO, width=70)

        # insert the data into the table
        self.update_comment(self.reviews)

        # create the scrollbar
        self.comment.pack(side=LEFT, fill=Y, expand=1)
        comment_scrollbar = tkinter.ttk.Scrollbar(
            commentFrame, orient="vertical", command=self.comment.yview
        )
        self.comment.configure(yscrollcommand=comment_scrollbar.set)
        comment_scrollbar.pack(side=RIGHT, fill=Y)

        # set the style of the table
        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="Cornsilk")
        self.comment.configure(style="Custom.Treeview")

        # create the widgets of the review
        commentFrame.pack(side=LEFT, fill=BOTH)
        reviewFrame.pack(side=TOP, fill=BOTH, expand=True)

    # *展示蔬菜管理页面
    def show_information(self):

        # clear the showFrame
        self.clear_showFrame()

        # set the hit title of the showFrame
        title_lable_vege = Label(
            self.showFrame_title,
            text="   Vegetable Information",
            bg="LemonChiffon",
            fg="ForestGreen",
            font=("times new roman", 30),
        )
        title_lable_vege.pack(side=LEFT)

        # Show the vegetable information
        # self.show_vegetable_information()

        # Show the notebook
        self.show_information_notebook()

    """
    # 展示蔬菜信息
    def show_vegetable_information(self, parent):
        # 展示蔬菜
        # 获取蔬菜信息
        df = db_api.getVegetableDataFrame()
        vegs = df['vegetable_name'].unique().tolist()
        
        #搜索蔬菜
        search_lable = Label(parent, text="搜 索 蔬 菜:")
        search_lable.pack(side=TOP, pady=5)
        
        entry = Entry(parent, width=30)
        entry.pack(side=TOP, pady=5)
        
        search_button = Button(parent, text="查 找")
        search_button.pack(side=TOP, pady=5)
        
        # 展示蔬菜
        for veg in vegs:
            label = Label(self.showFrame_show, text=veg, bg="PaleTurquoise")
            label.pack(side=TOP)
    """

    # *更新蔬菜信息
    def update_vege(self, df):
        # 清空当前内容
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 插入新的数据
        for index, row in df.iterrows():
            self.tree.insert(
                "",
                "end",
                values=(
                    row["vegetable_name"],
                    row["purchase_quantity"],
                    row["purchase_price"],
                    row["supplier_id"],
                    row["selling_price"],
                    row["vip_price"],
                ),
            )

    # *搜索蔬菜
    def search_vegetable(self):
        search_value = self.var_vege_name.get()
        seach_result = self.vegetable_df[
            self.vegetable_df["vegetable_name"].str.contains(search_value, case=False)
        ]
        self.update_vege(seach_result)

    # *清空搜索框
    def clear_search(self):
        self.var_vege_name.set("")
        self.update_vege(self.vegetable_df)

    # *蔬菜信息管理
    def show_information_notebook(self):
        notebook = tkinter.ttk.Notebook(self.showFrame_show)

        # *展示蔬菜信息
        tab1 = Frame(notebook, bg="lightyellow")
        notebook.add(tab1, text="Vegetable List")
        search_frame = Frame(tab1, bg="lightyellow")
        search_frame.pack(side=TOP, pady=5)

        # 获取数据
        self.vegetable_df = db_api.getVegetableDataFrame()
        vegs = self.vegetable_df["vegetable_name"].unique().tolist()

        # 蔬菜搜索
        self.var_vege_name = StringVar()
        entry = Entry(search_frame, width=30, textvariable=self.var_vege_name)
        entry.grid(row=0, column=0, padx=5)
        search_button = Button(
            search_frame, text="Search", command=self.search_vegetable
        )
        search_button.grid(row=0, column=1, padx=5)
        show_all_button = Button(
            search_frame, text="Show All", command=self.clear_search
        )
        show_all_button.grid(row=0, column=2, padx=5)

        # 展示蔬菜
        columns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.tree = tkinter.ttk.Treeview(tab1, columns=columns, show="headings")

        # 定义每一列
        self.tree.heading("#1", text="Vegetable Name")
        self.tree.heading("#2", text="Qurchase Quantity")
        self.tree.heading("#3", text="Purchase Price")
        self.tree.heading("#4", text="Supplier Id")
        self.tree.heading("#5", text="Selling Price")
        self.tree.heading("#6", text="VIP Price")

        self.tree.column("#1", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("#2", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("#3", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("#4", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("#5", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("#6", anchor=CENTER, stretch=NO, width=120)

        # 插入数据到Treeview
        self.update_vege(self.vegetable_df)

        scrollbar = tkinter.ttk.Scrollbar(
            tab1, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 将Treeview放置在tab1中并扩展以填满空间
        self.tree.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="FloralWhite")
        self.tree.configure(style="Custom.Treeview")

        """
        # 设置行的权重,以确保Treeview可扩展 
        tab1.grid_rowconfigure(1, weight=5)
        # 设置列的权重，以确保可扩展性 
        tab1.grid_columnconfigure(1, weight=500)
        """

        """
        # 使得tree能够在resize时调整大小
        tab1.grid_rowconfigure(4, weight=1)
        tab1.grid_columnconfigure(0, weight=1)
        tab1.grid_columnconfigure(1, weight=1)

        
        # 获取蔬菜信息
        vegetable_df = db_api.getVegetableDataFrame()
        vegs = vegetable_df['vegetable_name'].unique().tolist()
        """

        # *管理蔬菜信息
        tab2 = Frame(notebook, bg="lightyellow")
        notebook.add(tab2, text="Modification")

        # 选择添加或删除蔬菜或修改蔬菜信息
        choose_frame = Frame(tab2, bg="lightyellow")
        choose_frame.pack(side=TOP, pady=5)

        # 添加蔬菜按钮
        add_button = Button(
            choose_frame,
            text="Add Vegetable",
            bg="LightGreen",
            command=self.add_vegetable,
            font=("times new roman", 20),
        )
        add_button.pack(side=LEFT, padx=20, pady=50)

        # 删除蔬菜按钮
        delete_button = Button(
            choose_frame,
            text="Delete Vegetable",
            bg="LightGreen",
            command=self.delete_vegetable,
            font=("times new roman", 20),
        )
        delete_button.pack(side=LEFT, padx=20, pady=50)

        # 修改蔬菜按钮
        modify_button = Button(
            choose_frame,
            text="Modify Vegetable",
            bg="LightGreen",
            command=self.modify_vegetable,
            font=("times new roman", 20),
        )
        modify_button.pack(side=LEFT, padx=20, pady=50)

        # set the notebook
        notebook.pack(expand=True, fill=BOTH)

        # 添加蔬菜

    def add_vegetable(self):
        self.clear_showFrame_show()

        addFrame_show = Frame(self.showFrame_show, bg="lightyellow")
        addFrame_show.pack(side=TOP, pady=10)
        add_vege_frame = Frame(addFrame_show, bg="lightyellow")
        add_vege_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vege_name_label = Label(
            add_vege_frame,
            text="vegetable_name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vege_name_label.grid(row=0, column=0, padx=10)
        vege_name_entry = Entry(add_vege_frame, width=30)
        vege_name_entry.grid(row=0, column=1, padx=10)

        # 蔬菜量
        purchase_quantity_label = Label(
            add_vege_frame,
            text="purchase quantity:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        purchase_quantity_label.grid(row=1, column=0, padx=10)
        purchase_quantity_entry = Entry(add_vege_frame, width=30)
        purchase_quantity_entry.grid(row=1, column=1, padx=10)

        # 蔬菜进价
        purchase_price_label = Label(
            add_vege_frame,
            text="purchase price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        purchase_price_label.grid(row=2, column=0, padx=10)
        purchase_price_entry = Entry(add_vege_frame, width=30)
        purchase_price_entry.grid(row=2, column=1, padx=10)

        # 供应商
        supplier_label = Label(
            add_vege_frame,
            text="supplier id:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        supplier_label.grid(row=3, column=0, padx=10)
        supplier_entry = Entry(add_vege_frame, width=30)
        supplier_entry.grid(row=3, column=1, padx=10)

        # 蔬菜售价
        selling_price_label = Label(
            add_vege_frame,
            text="selling price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        selling_price_label.grid(row=4, column=0, padx=10)
        selling_price_entry = Entry(add_vege_frame, width=30)
        selling_price_entry.grid(row=4, column=1, padx=10)

        # VIP价格
        vip_price_label = Label(
            add_vege_frame,
            text="vip price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vip_price_label.grid(row=5, column=0, padx=10)
        vip_price_entry = Entry(add_vege_frame, width=30)
        vip_price_entry.grid(row=5, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            add_vege_frame, text="Submit", bg="LightGreen", font=("times new roman", 20)
        )
        submit_button.grid(row=6, column=0, columnspan=5, pady=20)

        # 返回
        return_button = Button(
            add_vege_frame,
            text="Return",
            bg="LightGreen",
            command=self.back_vege_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=6, column=1, columnspan=5, pady=20)

        """
        for i in range(1, 6):
            lbl = Label(tab2, text=f"Detail {i}", bg="LightGreen")
            lbl.pack(fill='x')
        """

    # *删除蔬菜
    def delete_vegetable(self):
        self.clear_showFrame_show()

        # Create the main frame for modification
        delete_frame = Frame(self.showFrame_show, bg="lightyellow")
        delete_frame.pack(side=TOP, pady=10)

        # Frame for selecting vegetable to modify
        delete_vege_frame = Frame(delete_frame, bg="lightyellow")
        delete_vege_frame.pack(side=TOP, pady=10)

        # 蔬菜名称输入部分
        select_label = Label(
            delete_vege_frame,
            text="Enter Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        select_label.grid(row=0, column=0, padx=10)

        self.var_search_vege = StringVar()
        search_entry = Entry(
            delete_vege_frame, textvariable=self.var_search_vege, width=30
        )
        search_entry.grid(row=0, column=1, padx=10)
        search_entry.bind("<KeyRelease>", self.update_vege_menu)

        self.var_selected_vege = StringVar()
        self.vege_menu = OptionMenu(delete_vege_frame, self.var_selected_vege, "")
        self.vege_menu.grid(row=0, column=2, padx=10)

        delete_button = Button(
            delete_vege_frame,
            text="Delete",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_deleted_vegetable,
        )
        delete_button.grid(row=2, column=0, columnspan=2, pady=5, padx=20)

        return_button = Button(
            delete_vege_frame,
            text="Return",
            bg="LightGreen",
            command=self.back_vege_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=2, column=1, columnspan=2, pady=5, padx=20)

        self.update_vege_menu()

    def update_vege_menu(self, event=None):
        search_text = self.var_search_vege.get().lower()
        filtered_vegs = [
            vege
            for vege in self.vegetable_df["vegetable_name"]
            if search_text in vege.lower()
        ]

        menu = self.vege_menu["menu"]
        menu.delete(0, "end")

        if filtered_vegs:
            self.var_selected_vege.set(filtered_vegs[0])
            for vege in filtered_vegs:
                menu.add_command(
                    label=vege, command=lambda v=vege: self.var_selected_vege.set(v)
                )
        else:
            self.var_selected_vege.set("")

    def save_deleted_vegetable(self):
        selected_vege = self.var_selected_vege.get()
        if selected_vege == "":
            messagebox.showwarning("Warning", "No vegetable selected!")
            return

        # 删除 DataFrame 中的数据
        self.vegetable_df = self.vegetable_df[
            self.vegetable_df["vegetable_name"] != selected_vege
        ]

        # 同步数据库
        # db_api.updateVegetableDataFrame(self.vegetable_df)

        # 提示用户
        messagebox.showinfo("Info", "Vegetable deleted successfully!")

        # 返回蔬菜信息 Notebook
        self.back_vege_information()

    # *修改蔬菜
    def modify_vegetable(self):
        # Clear the current frame
        self.clear_showFrame_show()

        # Create the main frame for modification
        modify_frame = Frame(self.showFrame_show, bg="lightyellow")
        modify_frame.pack(side=TOP, pady=10)

        # Frame for selecting vegetable to modify
        select_vege_frame = Frame(modify_frame, bg="lightyellow")
        select_vege_frame.pack(side=TOP, pady=10)

        select_label = Label(
            select_vege_frame,
            text="Enter Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        select_label.grid(row=0, column=0, padx=10)

        self.var_search_vege = StringVar()
        search_entry = Entry(
            select_vege_frame, textvariable=self.var_search_vege, width=30
        )
        search_entry.grid(row=0, column=1, padx=10)
        search_entry.bind("<KeyRelease>", self.update_vege_menu)

        self.var_selected_vege = StringVar()
        self.vege_menu = OptionMenu(select_vege_frame, self.var_selected_vege, "")
        self.vege_menu.grid(row=0, column=2, padx=10)

        show_button = Button(
            select_vege_frame,
            text="Show Details",
            bg="LightGreen",
            font=("times new roman", 15),
            command=self._display_modify_form,
        )
        show_button.grid(row=0, column=3, padx=5)

        self.update_vege_menu()

    def update_vege_menu(self, event=None):
        search_text = self.var_search_vege.get().lower()
        filtered_vegs = [
            vege
            for vege in self.vegetable_df["vegetable_name"]
            if search_text in vege.lower()
        ]

        menu = self.vege_menu["menu"]
        menu.delete(0, "end")

        if filtered_vegs:
            self.var_selected_vege.set(filtered_vegs[0])
            for vege in filtered_vegs:
                menu.add_command(
                    label=vege, command=lambda v=vege: self.var_selected_vege.set(v)
                )
        else:
            self.var_selected_vege.set("")

    def _display_modify_form(self):
        selected_vege = self.var_selected_vege.get()
        if selected_vege == "":
            messagebox.showwarning("Warning", "No vegetable selected!")
            return

        vege_info = self.vegetable_df.loc[
            self.vegetable_df["vegetable_name"] == selected_vege
        ].iloc[0]
        form_frame = Frame(self.showFrame_show, bg="lightyellow")
        form_frame.pack(side=TOP, pady=20)

        # vegetable form fields
        labels = [
            "vegetable_name",
            "purchase_quantity",
            "purchase_price",
            "supplier_id",
            "selling_price",
            "vip_price",
        ]
        entries = {}

        for i, label in enumerate(labels, start=1):
            lbl = Label(
                form_frame,
                text=f"{label.replace('_', ' ').capitalize()}:",
                bg="lightyellow",
                font=("times new roman", 20),
            )
            lbl.grid(row=i, column=0, padx=10)
            ent = Entry(form_frame, width=30)
            ent.grid(row=i, column=1, padx=10)
            ent.insert(0, vege_info[label])
            entries[label] = ent

        # Save button
        save_button = Button(
            form_frame,
            text="Save",
            bg="LightGreen",
            font=("times new roman", 20),
            command=lambda: self.save_modified_vegetable(entries),
            width=10,
        )
        save_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

        # Return button
        return_button = Button(
            form_frame,
            text="Return",
            bg="LightGreen",
            command=self.back_vege_information,
            font=("times new roman", 20),
            width=10,
        )
        return_button.grid(
            row=len(labels) + 2, column=0, columnspan=2, pady=10, padx=20
        )

        # 刷新页面
        re_choose_button = Button(
            form_frame,
            text="Re-choose",
            bg="Limegreen",
            command=self.modify_vegetable,
            font=("times new roman", 15),
            width=10,
        )
        re_choose_button.grid(row=len(labels) + 3, column=0, columnspan=5, pady=5)

    def save_modified_vegetable(self, entries):
        selected_vege = self.var_selected_vege.get()

        # 获取每个 Entry 的值
        updated_info = {label: entry.get().strip() for label, entry in entries.items()}

        # 更新 DataFrame 中的数据
        self.vegetable_df.loc[
            self.vegetable_df["vegetable_name"] == selected_vege, updated_info.keys()
        ] = updated_info.values()

        # 同步数据库
        db_api.updateVegetableDataFrame(self.vegetable_df)

        # 提示用户
        messagebox.showinfo("Info", "Vegetable information updated successfully!")

        # 返回蔬菜信息 Notebook
        self.back_vege_information()

    # *返回管理蔬菜信息页面
    def back_vege_information(self):
        # clear the showFrame
        self.clear_showFrame_show()

        # back to the vege showFrame
        self.show_information_notebook()

    def show_market(self):
        self.clear_showFrame()
        title_label_market = Label(
            self.showFrame_title,
            text="Vegetable Market",
            bg="LemonChiffon",
            fg="ForestGreen",
            font=("times new roman", 30),
        )
        title_label_market.pack(side=LEFT)

        self.show_market_notebook()

    def apply_sorting(self, df, column, sort_order):
        return df.sort_values(by=column, ascending=(sort_order == "Ascending"))

    def filter_and_update_market_vege(self):
        search_value = self.market_vege_name.get()
        selected_season = self.season_var.get()

        if selected_season == "All":
            filtered_df = self.market_vegetable_df[
                self.market_vegetable_df["vegetable_name"].str.contains(
                    search_value, case=False
                )
            ]
        else:
            filtered_df = self.market_vegetable_df[
                (
                    self.market_vegetable_df["vegetable_name"].str.contains(
                        search_value, case=False
                    )
                )
                & (self.market_vegetable_df["season"] == selected_season)
            ]

        sorted_df = self.apply_sorting(
            filtered_df, column="date", sort_order=self.date_sort_var.get()
        )
        self.update_market_vege(sorted_df)

    def update_market_vege(self, df):
        for item in self.tree_market_vege.get_children():
            self.tree_market_vege.delete(item)

        for index, row in df.iterrows():
            self.tree_market_vege.insert(
                "",
                "end",
                values=(
                    row["vegetable_name"],
                    row["price"],
                    row["sale_volume"],
                    row["season"],
                    row["date"],
                ),
            )

    def clear_market_search(self):
        self.market_vege_name.set("")
        self.season_var.set("All")
        sorted_df = self.apply_sorting(
            self.market_vegetable_df, column="date", sort_order=self.date_sort_var.get()
        )
        self.update_market_vege(sorted_df)

    def sort_by_date(self, *args):
        self.filter_and_update_market_vege()

    def filter_and_update_market_information(self):
        search_vegetable = self.market_information.get()
        search_region = self.region_var.get()

        filtered_df = self.market_information_df[
            (
                self.market_information_df["vegetable_name"].str.contains(
                    search_vegetable, case=False
                )
            )
            & (
                self.market_information_df["region"].str.contains(
                    search_region, case=False
                )
            )
        ]

        sorted_df = self.apply_sorting(
            filtered_df,
            column=self.market_info_sort_column,
            sort_order=self.market_info_sort_order,
        )
        self.update_market_information(sorted_df)

    def update_market_information(self, df):
        for item in self.tree_market_info.get_children():
            self.tree_market_info.delete(item)

        for index, row in df.iterrows():
            self.tree_market_info.insert(
                "",
                "end",
                values=(
                    row["vegetable_name"],
                    row["market_name"],
                    row["region"],
                    row["lowest_price"],
                    row["highest_price"],
                    row["average_price"],
                    row["publish_date"],
                ),
            )

    def clear_market_information(self):
        self.market_information.set("")
        self.region_var.set("")
        sorted_df = self.apply_sorting(
            self.market_information_df,
            column=self.market_info_sort_column,
            sort_order=self.market_info_sort_order,
        )
        self.update_market_information(sorted_df)

    def sort_by_column(self, column):
        if self.market_info_sort_column == column:
            self.market_info_sort_order = (
                "Descending"
                if self.market_info_sort_order == "Ascending"
                else "Ascending"
            )
        else:
            self.market_info_sort_order = "Ascending"
        self.market_info_sort_column = column
        self.filter_and_update_market_information()

    def show_market_notebook(self):
        show_market_notebook = tkinter.ttk.Notebook(self.showFrame_show)

        # Market Price Tab
        market_tab1 = Frame(show_market_notebook, bg="lightyellow")
        show_market_notebook.add(market_tab1, text="Market Price")
        search_frame = Frame(market_tab1, bg="lightyellow")
        search_frame.pack(side=TOP, pady=5)

        self.market_vegetable_df = db_api.getMarketPriceDataFrame()

        self.market_vege_name = StringVar()
        entry = Entry(search_frame, width=30, textvariable=self.market_vege_name)
        entry.grid(row=0, column=0, padx=5)

        season_label = Label(search_frame, text="Season:")
        season_label.grid(row=0, column=3, padx=5)

        self.season_var = StringVar()
        self.season_var.set("All")
        season_choices = ["All", "spring", "summer", "autumn", "winter"]
        season_menu = OptionMenu(
            search_frame,
            self.season_var,
            *season_choices,
            command=lambda _: self.filter_and_update_market_vege(),
        )
        season_menu.grid(row=0, column=4, padx=5)

        search_button = Button(
            search_frame, text="Search", command=self.filter_and_update_market_vege
        )
        search_button.grid(row=0, column=1, padx=5)

        show_all_button = Button(
            search_frame, text="Show All", command=self.clear_market_search
        )
        show_all_button.grid(row=0, column=2, padx=5)

        date_sort_label = Label(search_frame, text="Sort by Date:")
        date_sort_label.grid(row=0, column=5, padx=5)

        self.date_sort_var = StringVar()
        self.date_sort_var.set("Ascending")
        date_sort_choices = ["Ascending", "Descending"]
        date_sort_menu = OptionMenu(
            search_frame,
            self.date_sort_var,
            *date_sort_choices,
            command=self.sort_by_date,
        )
        date_sort_menu.grid(row=0, column=6, padx=5)

        columns = ("#1", "#2", "#3", "#4", "#5")
        self.tree_market_vege = tkinter.ttk.Treeview(
            market_tab1, columns=columns, show="headings"
        )

        self.tree_market_vege.heading("#1", text="Vegetable Name")
        self.tree_market_vege.heading("#2", text="Price")
        self.tree_market_vege.heading("#3", text="Sale Volume")
        self.tree_market_vege.heading("#4", text="Season")
        self.tree_market_vege.heading("#5", text="Date")

        self.tree_market_vege.column("#1", anchor=CENTER, stretch=NO, width=160)
        self.tree_market_vege.column("#2", anchor=CENTER, stretch=NO, width=140)
        self.tree_market_vege.column("#3", anchor=CENTER, stretch=NO, width=140)
        self.tree_market_vege.column("#4", anchor=CENTER, stretch=NO, width=140)
        self.tree_market_vege.column("#5", anchor=CENTER, stretch=NO, width=150)

        sorted_df = self.apply_sorting(
            self.market_vegetable_df, column="date", sort_order=self.date_sort_var.get()
        )
        self.update_market_vege(sorted_df)

        scrollbar = tkinter.ttk.Scrollbar(
            market_tab1, orient="vertical", command=self.tree_market_vege.yview
        )
        self.tree_market_vege.configure(yscrollcommand=scrollbar.set)
        self.tree_market_vege.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="FloralWhite")
        style.configure("Treeview.Heading", font=("Arial", 8))
        self.tree_market_vege.configure(style="Custom.Treeview")

        # Market Information Tab
        market_tab2 = Frame(show_market_notebook, bg="lightyellow")
        show_market_notebook.add(market_tab2, text="Market Information")

        search_frame = Frame(market_tab2, bg="lightyellow")
        search_frame.pack(side=TOP, pady=5)

        self.market_information_df = db_api.getMarketDataFrame()

        self.market_information = StringVar()
        entry = Entry(search_frame, width=30, textvariable=self.market_information)
        entry.grid(row=0, column=0, padx=5)

        region_label = Label(search_frame, text="Region:")
        region_label.grid(row=0, column=3, padx=5)

        self.region_var = StringVar()
        self.region_var.set("")
        region_entry = Entry(search_frame, width=30, textvariable=self.region_var)
        region_entry.grid(row=0, column=4, padx=5)

        search_button = Button(
            search_frame,
            text="Search",
            command=self.filter_and_update_market_information,
        )
        search_button.grid(row=0, column=1, padx=5)

        show_all_button = Button(
            search_frame, text="Show All", command=self.clear_market_information
        )
        show_all_button.grid(row=0, column=2, padx=5)

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.tree_market_info = tkinter.ttk.Treeview(
            market_tab2, columns=columns, show="headings"
        )

        self.tree_market_info.heading("#1", text="Vegetable Name")
        self.tree_market_info.heading("#2", text="Market Name")
        self.tree_market_info.heading("#3", text="Market Region")
        self.tree_market_info.heading(
            "#4",
            text="Lowest Price",
            command=lambda: self.sort_by_column("lowest_price"),
        )
        self.tree_market_info.heading(
            "#5",
            text="Highest Price",
            command=lambda: self.sort_by_column("highest_price"),
        )
        self.tree_market_info.heading(
            "#6",
            text="Average Price",
            command=lambda: self.sort_by_column("average_price"),
        )
        self.tree_market_info.heading("#7", text="Publish Date")

        self.market_info_sort_column = "publish_date"
        self.market_info_sort_order = "Ascending"

        self.tree_market_info.column("#1", anchor=CENTER, stretch=NO, width=95)
        self.tree_market_info.column("#2", anchor=CENTER, stretch=NO, width=200)
        self.tree_market_info.column("#3", anchor=CENTER, stretch=NO, width=80)
        self.tree_market_info.column("#4", anchor=CENTER, stretch=NO, width=80)
        self.tree_market_info.column("#5", anchor=CENTER, stretch=NO, width=80)
        self.tree_market_info.column("#6", anchor=CENTER, stretch=NO, width=80)
        self.tree_market_info.column("#7", anchor=CENTER, stretch=NO, width=110)

        sorted_market_information_df = self.apply_sorting(
            self.market_information_df,
            column=self.market_info_sort_column,
            sort_order=self.market_info_sort_order,
        )
        self.update_market_information(sorted_market_information_df)

        scrollbar = tkinter.ttk.Scrollbar(
            market_tab2, orient="vertical", command=self.tree_market_info.yview
        )
        self.tree_market_info.configure(yscrollcommand=scrollbar.set)
        self.tree_market_info.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="FloralWhite")
        self.tree_market_info.configure(style="Custom.Treeview")

        market_tab3 = Frame(show_market_notebook, bg="lightyellow")
        show_market_notebook.add(market_tab3, text="Supplier Information")

        search_frame = Frame(market_tab3, bg="lightyellow")
        search_frame.pack(side=TOP, pady=5)

        self.supplier_df = db_api.getSupplierDataFrame()

        self.supplier_region = StringVar()
        entry_region = Entry(search_frame, width=10, textvariable=self.supplier_region)
        entry_region.grid(row=0, column=0, padx=5)

        supplier_name_label = Label(search_frame, text="Supplier:")
        supplier_name_label.grid(row=0, column=3, padx=5)

        self.supplier_name_var = StringVar()
        entry_name = Entry(search_frame, width=15, textvariable=self.supplier_name_var)
        entry_name.grid(row=0, column=4, padx=5)

        rating_label = Label(search_frame, text="Rating:")
        rating_label.grid(row=0, column=5, padx=5)

        self.rating_var = StringVar()
        entry_rating = Entry(search_frame, width=10, textvariable=self.rating_var)
        entry_rating.grid(row=0, column=6, padx=5)

        availability_label = Label(search_frame, text="Availability:")
        availability_label.grid(row=0, column=7, padx=5)

        self.availability_var = StringVar()
        availability_choices = ["All", "available", "not available"]
        availability_menu = OptionMenu(
            search_frame, self.availability_var, *availability_choices
        )
        availability_menu.grid(row=0, column=8, padx=5)

        search_button = Button(
            search_frame, text="Search", command=self.filter_and_update_supplier
        )
        search_button.grid(row=0, column=1, padx=5)

        show_all_button = Button(
            search_frame, text="Show All", command=self.clear_supplier_search
        )
        show_all_button.grid(row=0, column=2, padx=5)

        columns = ("#1", "#2", "#3", "#4", "#5")
        self.tree_supplier = tkinter.ttk.Treeview(
            market_tab3, columns=columns, show="headings"
        )

        self.tree_supplier.heading("#1", text="Supplier Name")
        self.tree_supplier.heading("#2", text="Region")
        self.tree_supplier.heading("#3", text="Contact Info")
        self.tree_supplier.heading("#4", text="Rating")
        self.tree_supplier.heading("#5", text="Availability")

        self.tree_supplier.column("#1", anchor=CENTER, stretch=NO, width=200)
        self.tree_supplier.column("#2", anchor=CENTER, stretch=NO, width=160)
        self.tree_supplier.column("#3", anchor=CENTER, stretch=NO, width=120)
        self.tree_supplier.column("#4", anchor=CENTER, stretch=NO, width=120)
        self.tree_supplier.column("#5", anchor=CENTER, stretch=NO, width=120)

        self.update_supplier(self.supplier_df)

        scrollbar = tkinter.ttk.Scrollbar(
            market_tab3, orient="vertical", command=self.tree_supplier.yview
        )
        self.tree_supplier.configure(yscrollcommand=scrollbar.set)
        self.tree_supplier.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure style
        style = tkinter.ttk.Style()
        style.configure("Custom.Treeview", background="FloralWhite")
        self.tree_supplier.configure(style="Custom.Treeview")

        # Management Tab
        market_tab4 = Frame(show_market_notebook, bg="lightyellow")
        show_market_notebook.add(market_tab4, text="Management")
        management_frame = Frame(market_tab4, bg="lightyellow")
        management_frame.pack(side=TOP, pady=5)

        """
        self.management_choice = StringVar()
        choices = ["Add", "Delete", "Update"]
        self.management_choice.set(choices[0])
        choice_menu = OptionMenu(management_frame, self.management_choice, *choices)
        choice_menu.grid(row=0, column=0, padx=5)

        self.table_choice = StringVar()
        tables = ["Market Price", "Market Information", "Supplier Information"]
        self.table_choice.set(tables[0])
        table_menu = OptionMenu(management_frame, self.table_choice, *tables)
        table_menu.grid(row=0, column=1, padx=5)

        action_button = Button(
            management_frame, text="Execute", command=self.execute_management_action
        )
        action_button.grid(row=0, column=2, padx=5)

        self.management_message = Label(management_frame, text="", bg="lightyellow")
        self.management_message.grid(row=1, column=0, columnspan=3, pady=5)
        """
        # 选择dataframe
        # 选择MarketPriceDataFrame
        MarketPrice_button = Button(
            management_frame,
            text="Market Price",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.func_market_price,
        )
        MarketPrice_button.pack(side=LEFT, padx=20, pady=50)

        market_information_button = Button(
            management_frame,
            text="Market Information",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.func_market_information,
        )
        market_information_button.pack(side=LEFT, padx=20, pady=50)

        supplier_information_button = Button(
            management_frame,
            text="Supplier Information",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.func_supplier_information,
        )
        supplier_information_button.pack(side=LEFT, padx=20, pady=50)

        show_market_notebook.pack(expand=True, fill=BOTH)

    def update_supplier(self, df):
        # 清除当前所有行
        for row in self.tree_supplier.get_children():
            self.tree_supplier.delete(row)

        # 遍历DataFrame并插入到Treeview中
        for _, row in df.iterrows():
            self.tree_supplier.insert(
                "",
                "end",
                values=(
                    row["supplier_name"],
                    row["region"],
                    row["contact_info"],
                    row["rating"],
                    row["availability"],
                ),
            )

    def filter_and_update_supplier(self):
        # 获取搜索框的值
        region = self.supplier_region.get()
        name = self.supplier_name_var.get()
        rating = self.rating_var.get()
        availability = self.availability_var.get()

        # 应用过滤条件
        filtered_df = self.supplier_df.copy()

        if region:
            filtered_df = filtered_df[
                filtered_df["region"].str.contains(region, case=False, na=False)
            ]
        if name:
            filtered_df = filtered_df[
                filtered_df["supplier_name"].str.contains(name, case=False, na=False)
            ]
        if rating:
            filtered_df = filtered_df[
                filtered_df["rating"]
                .astype(str)
                .str.contains(rating, case=False, na=False)
            ]
        if availability != "All":
            filtered_df = filtered_df[
                filtered_df["availability"].str.contains(
                    availability, case=False, na=False
                )
            ]

        # 更新Treeview
        self.update_supplier(filtered_df)

    def clear_supplier_search(self):
        # 清空搜索框
        self.supplier_region.set("")
        self.supplier_name_var.set("")
        self.rating_var.set("")
        self.availability_var.set("All")

        # 显示所有数据
        self.update_supplier(self.supplier_df)

    def execute_management_action(self):
        action = self.management_choice.get()
        table = self.table_choice.get()

        if action == "Add":
            # 添加逻辑 implementation
            self.management_message.config(text=f"Successfully added to {table}.")
        elif action == "Delete":
            # 删除逻辑 implementation
            self.management_message.config(text=f"Successfully deleted from {table}.")
        elif action == "Update":
            # 更新逻辑 implementation
            self.management_message.config(text=f"Successfully updated in {table}.")

    # *操作market_information
    def func_market_information(self):
        self.clear_showFrame_show()
        # Create the main frame for func_market_information
        market_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        market_information_frame.pack(side=TOP, pady=10)

        # 选择具体的操作方法（add，delete，modify）
        add_market_information_button = Button(
            market_information_frame,
            text="Add",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.add_market_information,
        )

        delete_market_information_button = Button(
            market_information_frame,
            text="Delete",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.delete_market_information,
        )

        modify_market_information_button = Button(
            market_information_frame,
            text="Modify",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.modify_market_information,
        )

        return_market_information_button = Button(
            market_information_frame,
            text="Return",
            bg="LightGreen",
            command=self.show_market,
            font=("times new roman", 30),
        )

        add_market_information_button.pack(side=LEFT, padx=20, pady=100)
        delete_market_information_button.pack(side=LEFT, padx=20, pady=100)
        modify_market_information_button.pack(side=LEFT, padx=20, pady=100)
        return_market_information_button.pack(side=LEFT, padx=20, pady=100)

    def func_market_price(self):
        self.clear_showFrame_show()
        # Create the main frame for func_market_price
        market_price_frame = Frame(self.showFrame_show, bg="lightyellow")
        market_price_frame.pack(side=TOP, pady=10)

        # 选择具体的操作方法（add，delete，modify）
        add_market_price_button = Button(
            market_price_frame,
            text="Add",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.add_market_price,
        )

        delete_market_price_button = Button(
            market_price_frame,
            text="Delete",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.delete_market_price,
        )

        modify_market_price_button = Button(
            market_price_frame,
            text="Modify",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.modify_market_price,
        )

        return_market_price_button = Button(
            market_price_frame,
            text="Return",
            bg="LightGreen",
            command=self.show_market,
            font=("times new roman", 30),
        )

        add_market_price_button.pack(side=LEFT, padx=20, pady=100)
        delete_market_price_button.pack(side=LEFT, padx=20, pady=100)
        modify_market_price_button.pack(side=LEFT, padx=20, pady=100)
        return_market_price_button.pack(side=LEFT, padx=20, pady=100)

    def func_supplier_information(self):
        self.clear_showFrame_show()
        # Create the main frame for func_supplier_information
        supplier_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        supplier_information_frame.pack(side=TOP, pady=10)

        # 选择具体的操作方法（add，delete，modify）
        add_supplier_information_button = Button(
            supplier_information_frame,
            text="Add",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.add_supplier_information,
        )

        delete_supplier_information_button = Button(
            supplier_information_frame,
            text="Delete",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.delete_supplier_information,
        )

        modify_supplier_information_button = Button(
            supplier_information_frame,
            text="Modify",
            bg="LightGreen",
            font=("times new roman", 30),
            command=self.modify_supplier_information,
        )

        return_supplier_information_button = Button(
            supplier_information_frame,
            text="Return",
            bg="LightGreen",
            command=self.show_market,
            font=("times new roman", 30),
        )

        add_supplier_information_button.pack(side=LEFT, padx=20, pady=100)
        delete_supplier_information_button.pack(side=LEFT, padx=20, pady=100)
        modify_supplier_information_button.pack(side=LEFT, padx=20, pady=100)
        return_supplier_information_button.pack(side=LEFT, padx=20, pady=100)

    def add_market_information(self):
        self.clear_showFrame_show()
        # Create the main frame for add_market_information
        add_market_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        add_market_information_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vegetable_name_label = Label(
            add_market_information_frame,
            text="Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vegetable_name_label.grid(row=0, column=0, padx=10)
        vegetable_name_entry = Entry(add_market_information_frame, width=30)
        vegetable_name_entry.grid(row=0, column=1, padx=10)

        # 市场名称
        market_name_label = Label(
            add_market_information_frame,
            text="Market Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        market_name_label.grid(row=1, column=0, padx=10)
        market_name_entry = Entry(add_market_information_frame, width=30)
        market_name_entry.grid(row=1, column=1, padx=10)

        # 地区
        region_label = Label(
            add_market_information_frame,
            text="Region:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        region_label.grid(row=2, column=0, padx=10)
        region_entry = Entry(add_market_information_frame, width=30)
        region_entry.grid(row=2, column=1, padx=10)

        # 最低价格
        lowest_price_label = Label(
            add_market_information_frame,
            text="Lowest Price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        lowest_price_label.grid(row=3, column=0, padx=10)
        lowest_price_entry = Entry(add_market_information_frame, width=30)
        lowest_price_entry.grid(row=3, column=1, padx=10)

        # 最高价格
        highest_price_label = Label(
            add_market_information_frame,
            text="Highest Price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        highest_price_label.grid(row=4, column=0, padx=10)
        highest_price_entry = Entry(add_market_information_frame, width=30)
        highest_price_entry.grid(row=4, column=1, padx=10)

        # 平均价格
        average_price_label = Label(
            add_market_information_frame,
            text="Average Price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        average_price_label.grid(row=5, column=0, padx=10)
        average_price_entry = Entry(add_market_information_frame, width=30)
        average_price_entry.grid(row=5, column=1, padx=10)

        # 发布日期
        publish_date_label = Label(
            add_market_information_frame,
            text="Publish Date:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        publish_date_label.grid(row=6, column=0, padx=10)
        publish_date_entry = Entry(add_market_information_frame, width=30)
        publish_date_entry.grid(row=6, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            add_market_information_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_added_market_information,
        )
        submit_button.grid(row=7, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            add_market_information_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_market_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=8, column=0, columnspan=2, pady=5, padx=20)

    def save_added_market_information(self):
        # 提示用户
        messagebox.showinfo("Info", "Market information added successfully!")
        # 返回market_information
        self.func_market_information()

    """
    def save_added_market_information(self):
        # 获取输入框的值
        vegetable_name = vegetable_name_entry.get()
        market_name = market_name_entry.get()
        region = region_entry.get()
        lowest_price = lowest_price_entry.get()
        highest_price = highest_price_entry.get()
        average_price = average_price_entry.get()
        publish_date = publish_date_entry.get()
        
        # 将数据添加到DataFrame中
        new_row = {
            "vegetable_name": vegetable_name,
            "market_name": market_name,
            "region": region,
            "lowest_price": lowest_price,
            "highest_price": highest_price,
            "average_price": average_price,
            "publish_date": publish_date,
        }
        self.market_information_df = self.market_information_df.append(new_row, ignore_index=True)
        
        # 同步数据库
        db_api.updateMarketDataFrame(self.market_information_df)
        
        # 提示用户
        messagebox.showinfo("Info", "Market information added successfully!")
        
        # 返回market_information
        self.func_market_information()    
        """

    def delete_market_information(self):
        self.clear_showFrame_show()
        # Create the main frame for delete_market_information
        delete_market_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        delete_market_information_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vegetable_name_label = Label(
            delete_market_information_frame,
            text="Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vegetable_name_label.grid(row=0, column=0, padx=10)
        vegetable_name_entry = Entry(delete_market_information_frame, width=30)
        vegetable_name_entry.grid(row=0, column=1, padx=10)

        # 市场名称
        market_name_label = Label(
            delete_market_information_frame,
            text="Market Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        market_name_label.grid(row=1, column=0, padx=10)
        market_name_entry = Entry(delete_market_information_frame, width=30)
        market_name_entry.grid(row=1, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            delete_market_information_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_deleted_market_information,
        )
        submit_button.grid(row=2, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            delete_market_information_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_market_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=3, column=0, columnspan=2, pady=5, padx=20)

    def save_deleted_market_information(self):
        # 提示用户
        messagebox.showinfo("Info", "Market information deleted successfully!")
        # 返回market_information
        self.func_market_information()

    def modify_market_information(self):
        self.clear_showFrame_show()
        # Create the main frame for modify_market_information
        modify_market_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        modify_market_information_frame.pack(side=TOP, pady=10)

        # Frame for choosing the vegetable to modify
        choose_vege_frame = Frame(modify_market_information_frame, bg="lightyellow")
        choose_vege_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vegetable_name_label = Label(
            choose_vege_frame,
            text="Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vegetable_name_label.grid(row=0, column=0, padx=10)
        vegetable_name_entry = Entry(choose_vege_frame, width=30)
        vegetable_name_entry.grid(row=0, column=1, padx=10)

        # 市场名称
        market_name_label = Label(
            choose_vege_frame,
            text="Market Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        market_name_label.grid(row=1, column=0, padx=10)
        market_name_entry = Entry(choose_vege_frame, width=30)
        market_name_entry.grid(row=1, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            choose_vege_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.show_modified_market_information,
        )
        submit_button.grid(row=2, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            choose_vege_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_market_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=3, column=0, columnspan=2, pady=5, padx=20)

    def show_modified_market_information(self):
        messagebox.showinfo("Info", "Market information modified successfully!")
        self.func_market_information()

    def add_market_price(self):
        self.clear_showFrame_show()
        # Create the main frame for add_market_price
        add_market_price_frame = Frame(self.showFrame_show, bg="lightyellow")
        add_market_price_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vegetable_name_label = Label(
            add_market_price_frame,
            text="Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vegetable_name_label.grid(row=0, column=0, padx=10)
        vegetable_name_entry = Entry(add_market_price_frame, width=30)
        vegetable_name_entry.grid(row=0, column=1, padx=10)

        # 价格
        price_label = Label(
            add_market_price_frame,
            text="Price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        price_label.grid(row=1, column=0, padx=10)
        price_entry = Entry(add_market_price_frame, width=30)
        price_entry.grid(row=1, column=1, padx=10)

        # 销量
        sale_volume_label = Label(
            add_market_price_frame,
            text="Sale Volume:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        sale_volume_label.grid(row=2, column=0, padx=10)
        sale_volume_entry = Entry(add_market_price_frame, width=30)
        sale_volume_entry.grid(row=2, column=1, padx=10)

        # 季节
        season_label = Label(
            add_market_price_frame,
            text="Season:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        season_label.grid(row=3, column=0, padx=10)
        season_entry = Entry(add_market_price_frame, width=30)
        season_entry.grid(row=3, column=1, padx=10)

        # 日期
        date_label = Label(
            add_market_price_frame,
            text="Date:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        date_label.grid(row=4, column=0, padx=10)
        date_entry = Entry(add_market_price_frame, width=30)
        date_entry.grid(row=4, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            add_market_price_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_added_market_price,
        )
        submit_button.grid(row=5, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            add_market_price_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_market_price,
            font=("times new roman", 20),
        )
        return_button.grid(row=6, column=0, columnspan=2, pady=5, padx=20)

    def save_added_market_price(self):
        # 提示用户
        messagebox.showinfo("Info", "Market price added successfully!")
        # 返回market_price
        self.func_market_price()

    def delete_market_price(self):
        self.clear_showFrame_show()
        # Create the main frame for delete_market_price
        delete_market_price_frame = Frame(self.showFrame_show, bg="lightyellow")
        delete_market_price_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vegetable_name_label = Label(
            delete_market_price_frame,
            text="Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vegetable_name_label.grid(row=0, column=0, padx=10)
        vegetable_name_entry = Entry(delete_market_price_frame, width=30)
        vegetable_name_entry.grid(row=0, column=1, padx=10)

        # 季节
        season_label = Label(
            delete_market_price_frame,
            text="Season:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        season_label.grid(row=1, column=0, padx=10)
        season_entry = Entry(delete_market_price_frame, width=30)
        season_entry.grid(row=1, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            delete_market_price_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_deleted_market_price,
        )
        submit_button.grid(row=2, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            delete_market_price_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_market_price,
            font=("times new roman", 20),
        )
        return_button.grid(row=3, column=0, columnspan=2, pady=5, padx=20)

    def save_deleted_market_price(self):
        # 提示用户
        messagebox.showinfo("Info", "Market price deleted successfully!")
        # 返回market_price
        self.func_market_price()

    def modify_market_price(self):
        self.clear_showFrame_show()
        # Create the main frame for modify_market_price
        modify_market_price_frame = Frame(self.showFrame_show, bg="lightyellow")
        modify_market_price_frame.pack(side=TOP, pady=10)

        # Frame for choosing the vegetable to modify
        choose_vege_frame = Frame(modify_market_price_frame, bg="lightyellow")
        choose_vege_frame.pack(side=TOP, pady=10)

        # 蔬菜名称
        vegetable_name_label = Label(
            choose_vege_frame,
            text="Vegetable Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        vegetable_name_label.grid(row=0, column=0, padx=10)
        vegetable_name_entry = Entry(choose_vege_frame, width=30)
        vegetable_name_entry.grid(row=0, column=1, padx=10)

        # 价格
        price_label = Label(
            choose_vege_frame,
            text="Price:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        price_label.grid(row=1, column=0, padx=10)
        price_entry = Entry(choose_vege_frame, width=30)
        price_entry.grid(row=1, column=1, padx=10)

        # 销量
        sale_volume_label = Label(
            choose_vege_frame,
            text="Sale Volume:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        sale_volume_label.grid(row=2, column=0, padx=10)
        sale_volume_entry = Entry(choose_vege_frame, width=30)
        sale_volume_entry.grid(row=2, column=1, padx=10)

        # 季节
        season_label = Label(
            choose_vege_frame,
            text="Season:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        season_label.grid(row=3, column=0, padx=10)
        season_entry = Entry(choose_vege_frame, width=30)
        season_entry.grid(row=3, column=1, padx=10)

        # 日期
        date_label = Label(
            choose_vege_frame,
            text="Date:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        date_label.grid(row=4, column=0, padx=10)
        date_entry = Entry(choose_vege_frame, width=30)
        date_entry.grid(row=4, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            choose_vege_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.show_modified_market_price,
        )
        submit_button.grid(row=5, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            choose_vege_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_market_price,
            font=("times new roman", 20),
        )
        return_button.grid(row=6, column=0, columnspan=2, pady=5, padx=20)

    def show_modified_market_price(self):
        messagebox.showinfo("Info", "Market price modified successfully!")
        self.func_market_price()

    def add_supplier_information(self):
        self.clear_showFrame_show()
        # Create the main frame for add_supplier_information
        add_supplier_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        add_supplier_information_frame.pack(side=TOP, pady=10)

        # 供应商名称
        supplier_name_label = Label(
            add_supplier_information_frame,
            text="Supplier Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        supplier_name_label.grid(row=0, column=0, padx=10)
        supplier_name_entry = Entry(add_supplier_information_frame, width=30)
        supplier_name_entry.grid(row=0, column=1, padx=10)

        # 地区
        region_label = Label(
            add_supplier_information_frame,
            text="Region:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        region_label.grid(row=1, column=0, padx=10)
        region_entry = Entry(add_supplier_information_frame, width=30)
        region_entry.grid(row=1, column=1, padx=10)

        # 联系方式
        contact_info_label = Label(
            add_supplier_information_frame,
            text="Contact Info:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        contact_info_label.grid(row=2, column=0, padx=10)
        contact_info_entry = Entry(add_supplier_information_frame, width=30)
        contact_info_entry.grid(row=2, column=1, padx=10)

        # 评分
        rating_label = Label(
            add_supplier_information_frame,
            text="Rating:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        rating_label.grid(row=3, column=0, padx=10)
        rating_entry = Entry(add_supplier_information_frame, width=30)
        rating_entry.grid(row=3, column=1, padx=10)

        # 可用性
        availability_label = Label(
            add_supplier_information_frame,
            text="Availability:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        availability_label.grid(row=4, column=0, padx=10)
        availability_entry = tkinter.ttk.Combobox(
            add_supplier_information_frame, width=30
        )
        availability_entry["values"] = ["available", "not available"]
        availability_entry.grid(row=4, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            add_supplier_information_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_added_supplier_information,
        )
        submit_button.grid(row=5, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            add_supplier_information_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_supplier_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=6, column=0, columnspan=2, pady=5, padx=20)

    def save_added_supplier_information(self):
        # 提示用户
        messagebox.showinfo("Info", "Supplier information added successfully!")
        # 返回supplier_information
        self.func_supplier_information()

    def delete_supplier_information(self):
        self.clear_showFrame_show()
        # Create the main frame for delete_supplier_information
        delete_supplier_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        delete_supplier_information_frame.pack(side=TOP, pady=10)

        # 供应商名称
        supplier_name_label = Label(
            delete_supplier_information_frame,
            text="Supplier Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        supplier_name_label.grid(row=0, column=0, padx=10)
        supplier_name_entry = Entry(delete_supplier_information_frame, width=30)
        supplier_name_entry.grid(row=0, column=1, padx=10)

        # 地区
        region_label = Label(
            delete_supplier_information_frame,
            text="Region:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        region_label.grid(row=1, column=0, padx=10)
        region_entry = Entry(delete_supplier_information_frame, width=30)
        region_entry.grid(row=1, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            delete_supplier_information_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.save_deleted_supplier_information,
        )
        submit_button.grid(row=2, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            delete_supplier_information_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_supplier_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=3, column=0, columnspan=2, pady=5, padx=20)

    def save_deleted_supplier_information(self):
        # 提示用户
        messagebox.showinfo("Info", "Supplier information deleted successfully!")
        # 返回supplier_information
        self.func_supplier_information()

    def modify_supplier_information(self):
        self.clear_showFrame_show()
        # Create the main frame for modify_supplier_information
        modify_supplier_information_frame = Frame(self.showFrame_show, bg="lightyellow")
        modify_supplier_information_frame.pack(side=TOP, pady=10)

        # Frame for choosing the supplier to modify
        choose_supplier_frame = Frame(
            modify_supplier_information_frame, bg="lightyellow"
        )
        choose_supplier_frame.pack(side=TOP, pady=10)

        # 供应商名称
        supplier_name_label = Label(
            choose_supplier_frame,
            text="Supplier Name:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        supplier_name_label.grid(row=0, column=0, padx=10)
        supplier_name_entry = Entry(choose_supplier_frame, width=30)
        supplier_name_entry.grid(row=0, column=1, padx=10)

        # 地区
        region_label = Label(
            choose_supplier_frame,
            text="Region:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        region_label.grid(row=1, column=0, padx=10)
        region_entry = Entry(choose_supplier_frame, width=30)
        region_entry.grid(row=1, column=1, padx=10)

        # 联系方式
        contact_info_label = Label(
            choose_supplier_frame,
            text="Contact Info:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        contact_info_label.grid(row=2, column=0, padx=10)
        contact_info_entry = Entry(choose_supplier_frame, width=30)
        contact_info_entry.grid(row=2, column=1, padx=10)

        # 评分
        rating_label = Label(
            choose_supplier_frame,
            text="Rating:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        rating_label.grid(row=3, column=0, padx=10)
        rating_entry = Entry(choose_supplier_frame, width=30)
        rating_entry.grid(row=3, column=1, padx=10)

        # 可用性
        availability_label = Label(
            choose_supplier_frame,
            text="Availability:",
            bg="lightyellow",
            font=("times new roman", 20),
        )
        availability_label.grid(row=4, column=0, padx=10)
        availability_entry = tkinter.ttk.Combobox(choose_supplier_frame, width=30)
        availability_entry["values"] = ["available", "not available"]
        availability_entry.grid(row=4, column=1, padx=10)

        # 完成提交
        submit_button = Button(
            choose_supplier_frame,
            text="Submit",
            bg="LightGreen",
            font=("times new roman", 20),
            command=self.show_modified_supplier_information,
        )
        submit_button.grid(row=5, column=0, columnspan=2, pady=5, padx=20)

        # 返回
        return_button = Button(
            choose_supplier_frame,
            text="Return",
            bg="LightGreen",
            command=self.func_supplier_information,
            font=("times new roman", 20),
        )
        return_button.grid(row=6, column=0, columnspan=2, pady=5, padx=20)

    def show_modified_supplier_information(self):
        messagebox.showinfo("Info", "Supplier information modified successfully!")
        self.func_supplier_information()

    def management_message(self):
        pass

    def show_shop(self):
        # clear the showFrame
        self.clear_showFrame()

        # set the hit title of the showFrame
        title_label_shop = Label(
            self.showFrame_title,
            text="   My Shop",
            bg="LemonChiffon",
            fg="ForestGreen",
            font=("times new roman", 30),
        )
        title_label_shop.pack(side=LEFT)

        self.show_shop_notebook()

    def show_shop_notebook(self):
        show_shop_notebook = tkinter.ttk.Notebook(self.showFrame_show)

        # show the customer information tab
        shop_tab1 = Frame(show_shop_notebook, bg="lightyellow")
        show_shop_notebook.add(shop_tab1, text="Shop")
        search_frame = Frame(shop_tab1, bg="lightyellow")
        search_frame.pack(side=TOP, pady=10)

        # 添加搜索框和搜索按钮
        self.name_entry = Entry(search_frame)
        self.name_entry.pack(side=LEFT, padx=5)
        name_search_button = Button(
            search_frame, text="Search Name", command=self.search_by_name
        )
        name_search_button.pack(side=LEFT, padx=5)

        self.age_entry = Entry(search_frame)
        self.age_entry.pack(side=LEFT, padx=5)
        age_search_button = Button(
            search_frame, text="Search Age", command=self.search_by_age
        )
        age_search_button.pack(side=LEFT, padx=5)

        self.gender_entry = Entry(search_frame)
        self.gender_entry.pack(side=LEFT, padx=5)
        gender_search_button = Button(
            search_frame, text="Search Gender", command=self.search_by_gender
        )
        gender_search_button.pack(side=LEFT, padx=5)

        # Mocking db_api.getCustomerDataFrame() for the sake of example
        self.customer_df = db_api.getCustomerDataFrame()

        # 客户信息表格
        columns = ("#1", "#2", "#3", "#4", "#5")
        self.tree_customer = tkinter.ttk.Treeview(
            shop_tab1, columns=columns, show="headings"
        )

        self.tree_customer.heading("#1", text="Customer Name")
        self.tree_customer.heading("#2", text="Age")
        self.tree_customer.heading("#3", text="Gender")
        self.tree_customer.heading("#4", text="Phone Number")
        self.tree_customer.heading("#5", text="VIP")

        self.tree_customer.column("#1", width=140, anchor="center")
        self.tree_customer.column("#2", width=140, anchor="center")
        self.tree_customer.column("#3", width=140, anchor="center")
        self.tree_customer.column("#4", width=140, anchor="center")
        self.tree_customer.column("#5", width=140, anchor="center")

        self.update_customer(self.customer_df)

        scrollbar = tkinter.ttk.Scrollbar(
            shop_tab1, orient="vertical", command=self.tree_customer.yview
        )
        self.tree_customer.configure(yscrollcommand=scrollbar.set)
        self.tree_customer.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="FloralWhite")
        self.tree_customer.configure(style="Custom.Treeview")

        # 展示管理员信息
        shop_tab2 = Frame(show_shop_notebook, bg="lightyellow")
        show_shop_notebook.add(shop_tab2, text="Admin")
        admin_frame = Frame(shop_tab2, bg="lightyellow")
        admin_frame.pack(side=TOP, pady=10)

        # 获取管理员信息
        self.admin_df = db_api.getAdminDataFrame()

        # 管理员信息表格
        columns = ("#1", "#2", "#3")
        self.tree_admin = tkinter.ttk.Treeview(
            shop_tab2, columns=columns, show="headings"
        )
        self.tree_admin.heading("#1", text="Admin Name")
        self.tree_admin.heading("#2", text="Password")
        self.tree_admin.heading("#3", text="Create Time")

        self.tree_admin.column("#1", width=200, anchor="center")
        self.tree_admin.column("#2", width=200, anchor="center")
        self.tree_admin.column("#3", width=200, anchor="center")

        self.update_admin(self.admin_df)

        scrollbar = tkinter.ttk.Scrollbar(
            shop_tab1, orient="vertical", command=self.tree_admin.yview
        )
        self.tree_admin.configure(yscrollcommand=scrollbar.set)
        self.tree_admin.pack(side=TOP, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        style = tkinter.ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="FloralWhite")
        self.tree_admin.configure(style="Custom.Treeview")

        show_shop_notebook.pack(side=TOP, fill=BOTH, expand=1)

    def update_customer(self, customer_df):
        # Clear the treeview
        for item in self.tree_customer.get_children():
            self.tree_customer.delete(item)
        # Insert new data
        for _, row in customer_df.iterrows():
            self.tree_customer.insert("", "end", values=row.tolist())

    def update_admin(self, admin_df):
        # Clear the treeview
        for item in self.tree_admin.get_children():
            self.tree_admin.delete(item)
        # Insert new data
        for _, row in admin_df.iterrows():
            self.tree_admin.insert("", "end", values=row.tolist())
            
    def search_by_name(self):
        search_text = self.name_entry.get().lower()
        if not search_text:
            self.update_customer(self.customer_df)
            return
        filtered_df = self.customer_df[
            self.customer_df["name"].str.lower().str.contains(search_text)
        ]
        self.update_customer(filtered_df)

    def search_by_age(self):
        search_text = self.age_entry.get().lower()
        if not search_text:
            self.update_customer(self.customer_df)
            return
        filtered_df = self.customer_df[
            self.customer_df["age"].astype(str).str.contains(search_text)
        ]
        self.update_customer(filtered_df)

    def search_by_gender(self):
        search_text = self.gender_entry.get().lower()
        if not search_text:
            self.update_customer(self.customer_df)
            return
        filtered_df = self.customer_df[
            self.customer_df["gender"].str.lower().str.contains(search_text)
        ]
        self.update_customer(filtered_df)

    def search_by_vip(self):
        search_text = self.vip_entry.get().lower()
        if not search_text:
            self.update_customer(self.customer_df)
            return
        filtered_df = self.customer_df[
            self.customer_df["is_vip"].str.lower().str.contains(search_text)
        ]
        self.update_customer(filtered_df)


if __name__ == "__main__":
    root = Tk()
    root.geometry("900x600+300+90")
    root.title("VegeHub")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    app = Application(master=root)

    root.mainloop()
