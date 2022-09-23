from dbase import Database
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
from tkinter import ttk
from works import *
import pandas as pd
import sqlite3
import os
import time
from ml import ml_model
from output_to_price_sheet import pricesheet
from speech_engine import speech_text

db = Database('Database/building_db.db')
pricesheet = pricesheet()


class background(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open("img/background.jpg")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

class main_gui(tk.Tk):
   def __init__(self):
        super().__init__()
        path = os.getcwd()
        print(path)
        self.speech = speech_text()
        self.title("Building Tool")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.state("zoomed")
        #self.geometry("600x600")

        style = ttk.Style(self)
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.configure("Custom.Treeview.Heading",
                        background="gray", foreground="black", relief="groove", font=(None, 8))

        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])

        style_button = ttk.Style(self)
        style_button.configure('W.TButton', font=('calibri', 10, 'bold'),foreground='black')
        self.Txtvar = StringVar()
        self.Txtvar_storey = IntVar()
        self.Txtvar_storeyheight = DoubleVar()
        self.Txtvar_width = DoubleVar()
        self.Txtvar_length = DoubleVar()
        self.selected = IntVar()
        self.n = StringVar()
        self.found_beam = StringVar()
        self.found_wall = StringVar()
        self.ins = StringVar()
        self.floor = StringVar()
        self.room_type = StringVar()
        self.thk = IntVar()
        self.room_area = DoubleVar()
        self.room_qty = IntVar()
        self.room_place = StringVar()
        self.around_rooms = StringVar()
        self.mat = StringVar()
        self.structural_type = StringVar()
        self.steel_type = StringVar()
        self.basement_boolean = StringVar()
        self.seperated_boolean= StringVar()
        self.middle_floor_boolean = StringVar()
        self.rc_cladding = StringVar()
        self.project_name = StringVar()

        self.lbl = Label(self, text="BUILDING NAME:", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl2 = Label(self, text="STOREY(W/O BASEMENT):", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl3 = Label(self, text="STRUCTURAL TYPE:", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl5 = Label(self, text="BASEMENT(YES/NO):", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl4 = Label(self, text="FOUNDATION TYPE:", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_width = Label(self, text="WIDTH(m):", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_length = Label(self, text="LENGTH(m):", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_insulation = Label(self, text="INSULATION", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_thickness = Label(self, text="CLADDING THICKNESS:", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_material = Label(self, text="INSULATION MATERIAL:", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_buildings = Label(self, text="BUILDING LIST", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_floor = Label(self, text="FLOOR NO", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_room = Label(self, text="ROOM TYPE", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_room_area = Label(self, text="ROOM AREA", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_room_qty = Label(self, text="ROOM QTY", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_room_place = Label(self, text="ROOM PLACE", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_around_rooms = Label(self, text="AROUND ROOMS", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_room_list = Label(self, text="ROOM LIST", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl_middle_floor = Label(self, text="MIDDLE FLOOR", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_floor_covering = Label(self, text="FLOOR COVERING", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_seperated_room = Label(self, text="SEPERATED ROOM", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_project_name = Label(self, text="PROJECT NAME:", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.txt = ttk.Entry(self, width=5, textvariable=self.Txtvar)
        #self.spin1 = Spinbox(self, from_=1, to=10, relief="flat", borderwidth=4)
        self.spin1 = ttk.Combobox(self, width=27, textvariable=self.Txtvar_storey, state='readonly')
        self.spin1.bind('<<ComboboxSelected>>', self.comboFloorValues)
        self.txt_storeyheight = ttk.Entry(self, width=5, textvariable=self.Txtvar_storeyheight)
        self.txt_project_name = ttk.Entry(self, width=5, textvariable=self.project_name)
        self.combo_structural_type = ttk.Combobox(self, width=27, textvariable=self.structural_type, state='readonly')
        self.combo_structural_type.bind("<<ComboboxSelected>>", self.steel_selection)
        self.combo_steeltype = ttk.Combobox(self, width=27, textvariable=self.steel_type, state='readonly')
        self.combo_steeltype.bind("<<ComboboxSelected>>", self.steel_selection)
        self.combo_soil = ttk.Combobox(self, width=27, textvariable=self.n, state='readonly')
        self.combo_soil.bind("<<ComboboxSelected>>", self.foundation_selection)
        self.lbl_found_beam = Label(self, text="TIE BEAM", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.combo_found_beam = ttk.Combobox(self, width=27, textvariable=self.found_beam, state='readonly')
        self.combo_found_beam.bind("<<ComboboxSelected>>", self.foundation_selection)
        self.lbl_found_wall = Label(self, text="GROUND WALL", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_cable_channel = Label(self, text="CABLE CHANNEL", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.combo_found_wall = ttk.Combobox(self, width=27, textvariable=self.found_wall, state='readonly')
        self.combo_found_wall.bind("<<ComboboxSelected>>", self.foundation_selection)
        self.combo_cable_channel = ttk.Combobox(self, width=27, textvariable=self.found_wall, state='readonly')
        self.combo_cable_channel.bind("<<ComboboxSelected>>", self.foundation_selection)
        self.combo_seperated_room = ttk.Combobox(self, width=27, textvariable=self.seperated_boolean, state='readonly')
        self.combo_seperated_room.bind("<<ComboboxSelected>>", self.seperated_room_selection)
        self.combo_basement = ttk.Combobox(self, width=27, textvariable=self.basement_boolean, state='readonly')
        self.combo_basement.bind('<<ComboboxSelected>>', self.comboFloorValues)
        self.txt_width = ttk.Entry(self, width=5, textvariable=self.Txtvar_width)
        self.txt_length = ttk.Entry(self, width=5, textvariable=self.Txtvar_length)
        self.combo_insulation = ttk.Combobox(self, width=27, textvariable=self.ins, state='readonly')
        self.combo_thickness = ttk.Combobox(self, width=27, textvariable=self.thk, state='readonly')
        self.combo_material = ttk.Combobox(self, width=27, textvariable=self.mat, state='readonly')
        self.combo_floor = ttk.Combobox(self, width=27, textvariable=self.floor, state='readonly')
        self.combo_room_type = ttk.Combobox(self, width=27, textvariable=self.room_type, state='readonly')
        self.combo_room_place = ttk.Combobox(self, width=27, textvariable=self.room_place, state='readonly')
        self.combo_around_rooms = ttk.Combobox(self, width=27, textvariable=self.around_rooms, state='readonly')
        self.txt_room_area = ttk.Entry(self, width=5, textvariable=self.room_area)
        self.txt_room_qty = ttk.Entry(self, width=5, textvariable=self.room_qty)
        self.mf_spin = ttk.Combobox(self, width=17, textvariable=self.middle_floor_boolean, state='readonly')

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13", "#14", "#15")

        self.tvStudent = ttk.Treeview(self,show="headings", height="5", columns=columns, style="Custom.Treeview")
        self.tvStudent.bind("<<TreeviewSelect>>", self.select_item)
        self.tvStudent.heading('#1', text='Index', anchor='center')
        self.tvStudent.column('#1', width=40, anchor='center', stretch=False)
        self.tvStudent.heading('#2', text='Name', anchor='center')
        self.tvStudent.column('#2', width=60, anchor='center', stretch=False)
        self.tvStudent.heading('#3', text='StoreyNo', anchor='center')
        self.tvStudent.column('#3', width=52, anchor='center', stretch=False)
        self.tvStudent.heading('#4', text='StoreyHeight', anchor='center')
        self.tvStudent.column('#4', width=72, anchor='center', stretch=False)
        self.tvStudent.heading('#5', text='StructuralType', anchor='center')
        self.tvStudent.column('#5', width=79, anchor='center', stretch=False)
        self.tvStudent.heading('#6', text='SteelType', anchor='center')
        self.tvStudent.column('#6', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#7', text='Cladding', anchor='center')
        self.tvStudent.column('#7', width=80, anchor='center', stretch=False)
        self.tvStudent.heading('#8', text='SeperatedRoom', anchor='center')
        self.tvStudent.column('#8', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#9', text='MiddleFloor', anchor='center')
        self.tvStudent.column('#9', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#10', text='FoundationType', anchor='center')
        self.tvStudent.column('#10', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#11', text='Beam Connection', anchor='center')
        self.tvStudent.column('#11', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#12', text='Ground Wall', anchor='center')
        self.tvStudent.column('#12', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#13', text='Basement', anchor='center')
        self.tvStudent.column('#13', width=60, anchor='center', stretch=False)
        self.tvStudent.heading('#14', text='Width', anchor='center')
        self.tvStudent.column('#14', width=50, anchor='center', stretch=False)
        self.tvStudent.heading('#15', text='Length', anchor='center')
        self.tvStudent.column('#15', width=50, anchor='center', stretch=False)



        #self.room_list = Listbox(self, height=4, width=25, border=2, relief='sunken', borderwidth=5,font=("Allegro", 8, "bold"))
        #self.room_list.bind('<<ListboxSelect>>', self.select_room)

        columns_rooms = ("#1", "#2", "#3", "#4","#5","#6","#7","#8")
        self.room_list = ttk.Treeview(self,show="headings", height="5", columns=columns_rooms, style="Custom.Treeview")
        self.room_list.bind("<<TreeviewSelect>>", self.select_room)
        self.room_list.heading('#1', text='Index', anchor='center')
        self.room_list.column('#1', width=40, anchor='center', stretch=False)
        self.room_list.heading('#2', text='Room Type', anchor='center')
        self.room_list.column('#2', width=40, anchor='center', stretch=True)
        self.room_list.heading('#3', text='Floor No', anchor='center')
        self.room_list.column('#3', width=45, anchor='center', stretch=False)
        self.room_list.heading('#4', text='Room Area', anchor='center')
        self.room_list.column('#4', width=47, anchor='center', stretch=False)
        self.room_list.heading('#5', text='Room Quantity', anchor='center')
        self.room_list.column('#5', width=40, anchor='center', stretch=True)
        self.room_list.heading('#6', text='Room Place', anchor='center')
        self.room_list.column('#6', width=40, anchor='center', stretch=True)
        self.room_list.heading('#7', text='Around Rooms', anchor='center')
        self.room_list.column('#7', width=40, anchor='center', stretch=True)
        self.room_list.heading('#8', text='Building Name', anchor='center')
        self.room_list.column('#8', width=40, anchor='center', stretch=True)


        self.scrollbar = Scrollbar(self)
        self.scrollbar_room = Scrollbar(self)

        self.tvStudent.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.tvStudent.yview)
        self.room_list.configure(yscrollcommand=self.scrollbar_room.set)
        self.scrollbar_room.configure(command=self.room_list.yview)

        self.add_button_image = tk.PhotoImage(file='img/add.png').subsample(3, 3)
        self.run_btn = ttk.Button(self, text="ADD", command=self.add_item,cursor="hand2",style = 'W.TButton', image=self.add_button_image,compound = LEFT)
        self.show_button_image = tk.PhotoImage(file='img/list.png').subsample(3, 3)
        self.show_btn = ttk.Button(self, text="SHOW LIST", command=self.show_item, cursor="hand2",style = 'W.TButton', image=self.show_button_image,compound = LEFT)
        self.run_button_image = tk.PhotoImage(file='img/run.png').subsample(3, 3)
        self.btn_execute = ttk.Button(self, text="RUN", command=self.Execute, cursor="hand2",style = 'W.TButton', image=self.run_button_image,compound = LEFT)
        self.delete_button_image = tk.PhotoImage(file='img/delete.png').subsample(3, 3)
        self.btn_delete = ttk.Button(self, text="REMOVE", command=self.remove_item, cursor="hand2",style = 'W.TButton', image=self.delete_button_image,compound = LEFT)
        self.update_button_image = tk.PhotoImage(file='img/update.png').subsample(3, 3)
        self.btn_update = ttk.Button(self, text="UPDATE", command=self.update_item, cursor="hand2",style = 'W.TButton', image=self.update_button_image,compound = LEFT)
        self.clear_button_image = tk.PhotoImage(file='img/clear.png').subsample(3, 3)
        self.btn_clear = ttk.Button(self, text="CLEAR INPUT", command=self.clear_text, cursor="hand2",style = 'W.TButton', image=self.clear_button_image,compound = LEFT)
        self.quit_button_image = tk.PhotoImage(file='img/quit.png').subsample(3, 3)
        self.btn2 = ttk.Button(self, text="QUIT", command=self.on_closing, cursor="hand2",style = 'W.TButton', image=self.quit_button_image,compound = LEFT)
        self.room_btn = ttk.Button(self, text="ADD", command=self.add_room, cursor="hand2",style = 'W.TButton', image=self.add_button_image,compound = LEFT)
        self.room_btn2 = ttk.Button(self, text="UPDATE", command=self.update_room, cursor="hand2",style = 'W.TButton', image=self.update_button_image,compound = LEFT)
        self.room_btn3 = ttk.Button(self, text="REMOVE", command=self.remove_room, cursor="hand2",style = 'W.TButton', image=self.delete_button_image,compound = LEFT)
        self.room_btn4 = ttk.Button(self, text="SHOW ALL", command=self.show_room, cursor="hand2",style = 'W.TButton', image=self.show_button_image,compound = LEFT)

        self.lbl_storeyheight= Label(self,text="STOREY HEIGHT(m):",relief="groove",borderwidth=2,font=("Allegro",8,"bold"))
        self.lbl_storeyheight.place(relx=0.2204,rely=0.15,relwidth=0.25,relheight=0.05)

        self.combo_structural_type['values'] = ("STEEL", "RC")
        self.combo_structural_type.current()
        self.combo_steeltype['values'] = ("LIGHT_DUTY", "HEAVY_DUTY")
        self.combo_steeltype.current()
        self.combo_soil['values'] = ('MAT', 'STRIP', 'SINGLE_FOOTING','SINGLE_FOOTING(ONLY EDGE)')
        self.combo_soil.current()
        self.combo_found_beam['values'] = ('ONE_WAY', 'TWO_WAY', 'NO_BEAM','STRAP_BEAM')
        self.combo_soil.current()
        self.combo_found_wall['values'] = ('YES', 'NO')
        self.combo_soil.current()
        self.combo_basement['values'] = ('YES', 'NO')
        self.combo_basement.current()
        self.combo_insulation['values'] = ('CLADDING', 'SHEET')
        self.combo_insulation.current()
        self.combo_seperated_room['values'] = ('YES', ' NO')
        self.combo_seperated_room.current()
        self.mf_spin['values'] = ('YES', ' NO')
        self.mf_spin.current()
        self.combo_thickness['values'] = (6, 8, 10)
        self.combo_thickness.current()
        self.combo_material['values'] = ("ROCKWOOL", "PUR")
        self.combo_material.current()
        self.combo_floor['values'] = ('BASEMENT', '1', '2','3')
        self.spin1['values'] = ('1', '2', '3','4','5')
        self.spin1.current()
        self.combo_room_type['values'] = ("OFFICE", "SPECIAL_OFFICE", "ELECTRICAL_ROOM", "CONTROL_ROOM", "STORE", "WORKSHOP", "BATTERY_ROOM", "BEDROOM","ENTRANCE", "KITCHEN", "WC", "HALL","CANTEEN","MEETING ROOM","CONFERENCE ROOM","INDUCTION ROOM","STAIRHALL")
        self.combo_room_type.current()
        self.combo_room_place['values'] = ('EDGE', 'MIDDLE')
        self.combo_room_place.current()
        self.combo_around_rooms['values'] = ('ONE SIDE', 'BOTH SIDE', 'NONE')
        self.combo_around_rooms.current()
        self.Widget_List=[self.txt,self.spin1,self.combo_structural_type,self.combo_soil,self.combo_basement,self.run_btn,self.show_btn,self.btn2,self.lbl,self.lbl2,self.lbl3,self.lbl4,self.lbl5,self.lbl_storeyheight,self.txt_storeyheight,self.lbl_width,self.lbl_length,self.txt_width,self.txt_length,self.btn_update,self.btn_delete,self.btn_clear,self.btn_execute]
        self.Place_Coordinates=np.array([[0.1304,0.1304,0.1304,0.1304,0.1304,0.608,0.52,0.95,0.01,0.01,0.01,0.01,0.01,0.1904,0.304,0.01,0.01,0.1304,0.1304,0.67,0.73,0.79,0.1],#0.01
                                    [0.075,0.15,0.225,0.3,0.375,0.88,0.88,0.03,0.075,0.15,0.225,0.3,0.375,0.15,0.15,0.45,0.525,0.45,0.525,0.88,0.88,0.88,0.88],#0.075
                                    [0.13,0.05,0.05,0.12,0.05,0.05,0.07,0.04,0.113,0.113,0.113,0.113,0.113,0.1035,0.02,0.113,0.113,0.03,0.03,0.05,0.05,0.07,0.05],#0.113
                                    [0.03,0.04,0.03,0.03,0.03,0.05,0.05,0.04,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.05,0.05,0.05,0.05]])#0.03

        for i in range(0, len(self.Widget_List)):
            self.Widget_List[i].place_forget()

   # Creating the username & password entry boxes
        self.username_text = Label(self, text="Username:", bg='light goldenrod', relief='groove',font=("Pickwick", 10, "bold"))
        self.username_guess = Entry(self, relief='sunken', bd=4)
        self.username_guess.focus()
        self.username_guess.focus()
        self.password_text = Label(self, text="Password:", bg='light goldenrod', relief='groove',font=("Pickwick", 10, "bold"))
        self.password_guess = Entry(self, show="*", relief='sunken', bd=4)

        self.attempt_login = ttk.Button(text="Login", command=self.try_login,style = 'W.TButton')

        self.username_text.place(relx=0.45, rely=0.1455, relwidth=0.15, relheight=0.035)
        self.username_guess.place(relx=0.45, rely=0.1855, relwidth=0.15, relheight=0.035)
        self.password_text.place(relx=0.45, rely=0.2255, relwidth=0.15, relheight=0.035)
        self.password_guess.place(relx=0.45, rely=0.2655, relwidth=0.15, relheight=0.035)
        self.attempt_login.place(relx=0.45, rely=0.3055, relwidth=0.15, relheight=0.035)
        for i in range(0, len(self.Widget_List)):
            self.Widget_List[i].place(relx=self.Place_Coordinates[0, i], rely=self.Place_Coordinates[1, i],relwidth=self.Place_Coordinates[2, i], relheight=self.Place_Coordinates[3, i])
            self.tvStudent.place(relx=0.01, rely=0.58, relwidth=0.98, relheight=0.295)
            #tvStudent.place(x=40, y=310, height=h / 5, width=w / 1.1)
            self.scrollbar.place(relx=0.99, rely=0.58, relwidth=0.01, relheight=0.295)
            self.lbl_buildings.place(relx=0.45, rely=0.53, relwidth=0.08, relheight=0.03)
            self.lbl_project_name.place(relx=0.304, rely=0.075, relwidth=0.113, relheight=0.03)
            self.txt_project_name.place(relx=0.420, rely=0.075, relwidth=0.113, relheight=0.03)
        self.username_text.place_forget()
        self.username_guess.place_forget()
        self.password_text.place_forget()
        self.password_guess.place_forget()
        self.attempt_login.place_forget()
        self.txt.focus()
        self.add_menu()


        self.protocol("WM_DELETE_WINDOW", self.on_closing)

   def add_menu(self):
       self.menubar = tk.Menu(self)
       self.config(menu=self.menubar)

       self.filemenu = Menu(self.menubar, tearoff=0)
       self.submenu = Menu(self.filemenu, tearoff=0)
       self.submenu_type_rc = Menu(self.submenu, tearoff=0)
       self.submenu_type_steel = Menu(self.submenu, tearoff=0)

       self.filemenu.add_cascade(label="Preferences", menu=self.submenu, underline=0)
       self.submenu.add_cascade(label="RC", menu=self.submenu_type_rc, underline=0)
       self.submenu.add_cascade(label="STEEL", menu=self.submenu_type_steel, underline=0)
       self.filemenu.add_separator()
       self.filemenu.add_command(label="Reset Project", command=self.reset_project)
       self.filemenu.add_separator()
       self.filemenu.add_command(label="Exit", command=self.on_closing)
       self.menubar.add_cascade(label="Options", menu=self.filemenu)

   def try_login(self):
        print("Trying to login...")
        #if self.password_guess.get() == password and self.username_guess.get()==username:
            #messagebox.showinfo("-- COMPLETE --", "You Are Now Logging In.", icon="info")
            #self.attributes("-fullscreen", True)
        for i in range(0, len(self.Widget_List)):
            self.Widget_List[i].place(relx=self.Place_Coordinates[0, i], rely=self.Place_Coordinates[1, i],relwidth=self.Place_Coordinates[2, i], relheight=self.Place_Coordinates[3, i])
            self.tvStudent.place(relx=0.01, rely=0.58, relwidth=0.98, relheight=0.295)
            #tvStudent.place(x=40, y=310, height=h / 5, width=w / 1.1)
            self.scrollbar.place(relx=0.99, rely=0.58, relwidth=0.01, relheight=0.295)
            self.lbl_buildings.place(relx=0.45, rely=0.53, relwidth=0.08, relheight=0.03)
            self.lbl_project_name.place(relx=0.304, rely=0.075, relwidth=0.113, relheight=0.03)
            self.txt_project_name.place(relx=0.420, rely=0.075, relwidth=0.113, relheight=0.03)
        self.username_text.place_forget()
        self.username_guess.place_forget()
        self.password_text.place_forget()
        self.password_guess.place_forget()
        self.attempt_login.place_forget()
        self.txt.focus()
        self.add_menu()
        #else:
            #messagebox.showinfo("-- ERROR --", "Please enter valid infomation!", icon="warning")


   def populate_list(self):
        self.tvStudent.delete(*self.tvStudent.get_children())
        for row in db.fetch():
            self.tvStudent.insert("",row[0], values=row)

   def populate_room_list(self):
        self.room_list.delete(*self.room_list.get_children())
        for rooms in db.fetch_rooms_treeview():
            self.room_list.insert("", rooms[0],values=rooms)

   def empty_check(self):
       Textbox_list = [ self.spin1,self.txt_storeyheight,self.txt_width,self.txt_length]
       for text in Textbox_list:
           if len(str(text.get())) == 0:
               text.insert(0, '0')

   def add_item(self):
       #düzelt KOMPOSİT YARISI RC YARISI ÇELİK BİNA TİPİ EKLE
        if self.txt.get() == '' or self.spin1.get() == '' or self.txt_storeyheight.get() == '' or self.combo_structural_type.get() == '' or self.combo_soil.get() == '' or self.combo_found_beam.get() == '' or self.combo_found_wall.get() == '' or self.combo_basement.get() == '' or self.txt_width.get() == '' or self.txt_length.get() == '':
            self.speech.missing_input()
            messagebox.showerror('Required Fields', 'Please enter missing inputs', icon="warning")
            return
        if self.Txtvar.get() == "RC":
            try:
                self.Txtvar.get()
                self.spin1.get()
                self.Txtvar_storeyheight.get()
                self.combo_structural_type.get()
                self.combo_soil.get()
                self.combo_found_beam.get()
                self.combo_found_wall.get()
                self.combo_basement.get()
                self.Txtvar_width.get()
                self.Txtvar_length.get()
            except TclError or TypeError:
                messagebox.showerror('Required Fields','Please enter missing inputs',icon="warning")
            return
            if self.Txtvar.get() == '' or self.spin1.get() == '' or self.txt_storeyheight.get() == '' or self.combo_structural_type.get() == '' or self.combo_soil.get() == '' or self.combo_found_beam.get() == '' or self.combo_found_wall.get() == '' or self.combo_basement.get() == ''or self.txt_width.get() == ''or self.txt_length.get() == "":
                self.speech.missing_input()
                messagebox.showerror('Required Fields', 'Please enter missing inputs',icon="warning")
                return
        elif self.Txtvar.get() == "STEEL":
            try:
                self.Txtvar.get()
                self.spin1.get()
                self.Txtvar_storeyheight.get()
                self.combo_structural_type.get()
                self.combo_soil.get()
                self.combo_found_beam.get()
                self.combo_found_wall.get()
                self.combo_basement.get()
                self.Txtvar_width.get()
                self.Txtvar_length.get()
                self.combo_steeltype.get()
                self.combo_seperated_room.get()
                self.mf_spin.get()
                self.combo_insulation.get()
            except TclError or TypeError:
                messagebox.showerror('Required Fields','Please enter missing inputs',icon="warning")
            return
            if self.Txtvar.get() == '' or self.spin1.get() == '' or self.txt_storeyheight.get() == '' or self.combo_structural_type.get() == '' or self.combo_soil.get() == '' or self.combo_found_beam.get() == '' or self.combo_found_wall.get() == '' or self.combo_basement.get() == ''or self.txt_width.get() == ''or self.txt_length.get() == '' or self.combo_steeltype.get() == '' or self.combo_seperated_room.get() == '' or self.mf_spin.get() == '' or self.combo_insulation.get() == '':
                self.speech.missing_input()
                messagebox.showerror('Required Fields', 'Please enter missing inputs',icon="warning")
                return
        self.empty_check()
        model = ml_model()
        start_time=time.time()
        widthcode  = model.predict(self.Txtvar_width.get(),self.Txtvar_length.get(),self.Txtvar_storeyheight.get())[0]
        lengthcode = model.predict(self.Txtvar_width.get(), self.Txtvar_length.get(), self.Txtvar_storeyheight.get())[1]
        storeycode = model.predict(self.Txtvar_width.get(), self.Txtvar_length.get(), self.Txtvar_storeyheight.get())[2]
        storeyno = self.spin1.get()
        encoded_params = model.encode_parameters(self.combo_structural_type.get(), self.combo_soil.get(), self.combo_found_beam.get(),self.combo_found_wall.get(), self.combo_basement.get())
        structuraltype = encoded_params[0]
        foundationtype = encoded_params[1]
        foundation_beam = encoded_params[2]
        foundation_ground_wall = encoded_params[3]
        basement = encoded_params[4]
        print(storeyno,int(storeycode),structuraltype,foundationtype,foundation_beam,foundation_ground_wall,int(widthcode),int(lengthcode))
        model.create_data_table()
        params = db.parameter_selection(storeyno,int(storeycode),structuraltype,foundationtype,foundation_beam,foundation_ground_wall,int(widthcode),int(lengthcode))
        if len(params) != 0:
            for row in params:
                print(row)
                exc_depth = self.parameter_check(row[0],"exc_depth")
                strfill_depth = self.parameter_check(row[1],"strfill_depth")
                foundation_depth = self.parameter_check(row[2],"foundation_depth")
                foundation_D1 = self.parameter_check(row[3],"foundation_D1")
                foundation_D2 = self.parameter_check(row[4],"foundation_D2")
                tie_beam_d1 = self.parameter_check(row[5],"tie_beam_d1")
                tie_beam_d2 = self.parameter_check(row[6],"tie_beam_d2")
                steel_pedestal_d1 = self.parameter_check(row[7],"steel_pedestal_d1")
                steel_pedestal_d2 = self.parameter_check(row[8],"steel_pedestal_d2")
                steel_pedestal_depth = self.parameter_check(row[9],"steel_pedestal_depth")
                steel_pedestal_rangex = self.parameter_check(row[10],"steel_pedestal_rangex")
                steel_pedestal_rangey = self.parameter_check(row[11],"steel_pedestal_rangey")
                rc_column_width = self.parameter_check(row[12],"rc_column_width")
                rc_column_length = self.parameter_check(row[13],"rc_column_length")
                rc_column_rangex = self.parameter_check(row[14],"rc_column_rangex")
                rc_column_rangey = self.parameter_check(row[15],"rc_column_rangey")
                rc_beam_width = self.parameter_check(row[16],"rc_beam_width")
                rc_beam_length = self.parameter_check(row[17],"rc_beam_length")
                rc_secondary_beam_D1 = self.parameter_check(row[18],"rc_secondary_beam_D1")
                rc_secondary_beam_D2 = self.parameter_check(row[19],"rc_secondary_beam_D2")
                basement_wall_height = self.parameter_check(row[20],"basement_wall_height")
                basement_wall_thickness = self.parameter_check(row[21],"basement_wall_thickness")
                ground_wall_height = self.parameter_check(row[20],"ground_wall_height")
                ground_wall_thickness = self.parameter_check(row[21],"ground_wall_thickness")
                steel_weight = self.parameter_check(self.steel_check(),"steel_weight")
                grouting_depth = self.parameter_check(0.07,"grouting_depth")
                concrete_slab = self.parameter_check(row[22],"concrete_slab")
                ground_slab = self.parameter_check(row[23],"ground_slab")
                paraphet_height = self.parameter_check(row[25],"paraphet_height")
                paraphet_thickness = self.parameter_check(row[24],"paraphet_thickness")

        else:
            strfill_depth=1#ok
            foundation_depth=0.51
            foundation_D1=2.5
            foundation_D2=3
            tie_beam_d1=1
            tie_beam_d2=0.55
            steel_pedestal_d1=0.7
            steel_pedestal_d2=0.65
            steel_pedestal_depth=1.3
            steel_pedestal_rangex=6
            steel_pedestal_rangey=6
            rc_column_width=0.6
            rc_column_length=0.6
            rc_column_rangex=6
            rc_column_rangey=6
            rc_beam_width=0.4
            rc_beam_length=0.6
            rc_secondary_beam_D1=0.6
            rc_secondary_beam_D2=0.4
            basement_wall_height=3
            basement_wall_thickness=0.25
            ground_wall_height=1
            ground_wall_thickness=0.15
            steel_weight=self.steel_check()
            grouting_depth=0.07
            concrete_slab=0.15
            ground_slab = 0.2
            paraphet_height=0.7
            paraphet_thickness=0.15
            exc_depth = self.basement_check(foundation_depth,strfill_depth,basement_wall_height)  # ok
        self.excavationCheck(exc_depth, strfill_depth, foundation_depth,self.combo_basement.get(),basement_wall_height)
        db.insert(self.Txtvar.get(), self.spin1.get(),self.Txtvar_storeyheight.get(), self.combo_structural_type.get(),self.combo_steeltype.get(),self.combo_insulation.get(),self.combo_seperated_room.get(),self.mf_spin.get(),self.combo_soil.get(),self.combo_found_beam.get(),self.combo_found_wall.get(),self.combo_basement.get(),self.Txtvar_width.get(),self.Txtvar_length.get(),exc_depth, strfill_depth,foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2, steel_pedestal_d1,steel_pedestal_d2, steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rc_column_width, rc_column_length, rc_column_rangex, rc_column_rangey, basement_wall_height, basement_wall_thickness, ground_wall_height, ground_wall_thickness, steel_weight, grouting_depth, rc_beam_width,rc_beam_length, rc_secondary_beam_D1, rc_secondary_beam_D2, concrete_slab, ground_slab, paraphet_height, paraphet_thickness)
        self.tvStudent.delete(*self.tvStudent.get_children())
        self.tvStudent.insert("",tk.END,values= (self.Txtvar.get(), self.spin1.get(),self.Txtvar_storeyheight.get(), self.combo_structural_type.get(),self.combo_steeltype.get(),self.combo_insulation.get(),self.combo_seperated_room.get(),self.mf_spin.get(),self.combo_soil.get(),self.combo_found_beam.get(),self.combo_found_wall.get(),self.combo_basement.get(),self.Txtvar_width.get(),self.Txtvar_length.get()))
        self.clear_text()
        self.populate_list()
        self.add_menu()
    #parametreler için messagebox
        print(structuraltype)
        if structuraltype == 0:
            messagebox.showinfo("SELECTED PARAMETERS"
                    ,"exc_depth: {}".format(exc_depth)+
                    "\nstrfill_depth: {}".format(strfill_depth)+
                    "\nfoundation_depth: {}".format(foundation_depth)+
                    "\nfoundation_D1: {}".format(foundation_D1)+
                    "\nfoundation_D2: {}".format(foundation_D2)+
                    "\ntie_beam_d1: {}".format(tie_beam_d1)+
                    "\ntie_beam_d2: {}".format(tie_beam_d2)+
                    "\nrc_column_width: {}".format(rc_column_width)+
                    "\nrc_column_length: {}".format(rc_column_length)+
                    "\nrc_column_rangex: {}".format(rc_column_rangex)+
                    "\nrc_column_rangey: {}".format(rc_column_rangey)+
                    "\nrc_beam_width: {}".format(rc_beam_width)+
                    "\nrc_beam_length: {}".format(rc_beam_length)+
                    "\nrc_secondary_beam_D1: {}".format(rc_secondary_beam_D1)+
                    "\nrc_secondary_beam_D2: {}".format(rc_secondary_beam_D2)+
                    "\nbasement_wall_height: {}".format(basement_wall_height)+
                    "\nbasement_wall_thickness: {}".format(basement_wall_thickness)+
                    "\nground_wall_height: {}".format(ground_wall_height)+
                    "\nground_wall_thickness: {}".format(ground_wall_thickness)+
                    "\nconcrete_slab: {}".format(concrete_slab)+
                    "\nground_slab: {}".format(ground_slab)+
                    "\nparaphet_height: {}".format(paraphet_height)+
                    "\nparaphet_thickness: {}".format(paraphet_thickness)+
                    "\n-------------------------------------"
                    "\n GO OPTIONS MENU TO MAKE ANY CHANGE"
                               , icon="info")
        elif structuraltype == 1:
            messagebox.showinfo("SELECTED PARAMETERS"
                                , "exc_depth: {}".format(exc_depth) +
                                "\nstrfill_depth: {}".format(strfill_depth) +
                                "\nfoundation_depth: {}".format(foundation_depth) +
                                "\nfoundation_D1: {}".format(foundation_D1) +
                                "\nfoundation_D2: {}".format(foundation_D2) +
                                "\ntie_beam_d1: {}".format(tie_beam_d1) +
                                "\ntie_beam_d2: {}".format(tie_beam_d2) +
                                "\nsteel_pedestal_d1: {}".format(steel_pedestal_d1) +
                                "\nsteel_pedestal_d2: {}".format(steel_pedestal_d2) +
                                "\nsteel_pedestal_depth: {}".format(steel_pedestal_depth) +
                                "\nsteel_pedestal_rangex: {}".format(steel_pedestal_rangex) +
                                "\nsteel_pedestal_rangey: {}".format(steel_pedestal_rangey) +
                                "\nground_wall_height: {}".format(ground_wall_height) +
                                "\nground_wall_thickness: {}".format(ground_wall_thickness) +
                                "\nsteel_weight: {}".format(steel_weight) +
                                "\ngrouting_depth: {}".format(grouting_depth) +
                                "\nconcrete_slab: {}".format(concrete_slab) +
                                "\nground_slab: {}".format(ground_slab) +
                                "\n-------------------------------------"
                                "\n GO OPTIONS MENU TO MAKE ANY CHANGE"
                                ,icon="info")

        for name in db.fetch_building_names():
            print(name[0])
            if name[1]=="RC":
                self.submenu_type_rc.add_command(label=name[0],command=lambda index=name[0],type=name[1]: self.change_attr(index,type))
            elif name[1]=="STEEL":
                self.submenu_type_steel.add_command(label=name[0], command=lambda index=name[0],type=name[1]: self.change_attr(index,type))

        print("--- %s seconds ---" % (time.time() - start_time))

   def none_check(self,input):
       if input == None or input == '':
           return ''
       else:
           return input

   def zero_check(self, input):
        if input is None:
            return 0
        else:
            return input

   def parameter_check(self,parameter,key):
       parameter_dict = {"exc_depth" : self.basement_check(0.51,1,3)
            ,"strfill_depth":1#
            ,"foundation_depth":0.51
            ,"foundation_D1":2.5
            ,"foundation_D2":3
            ,"tie_beam_d1":1
            ,"tie_beam_d2":0.55
            ,"steel_pedestal_d1":0.7
            ,"steel_pedestal_d2":0.65
            ,"steel_pedestal_depth":1.3
            ,"steel_pedestal_rangex":6
            ,"steel_pedestal_rangey":6
            ,"rc_column_width":0.6
            ,"rc_column_length":0.6
            ,"rc_column_rangex":6
            ,"rc_column_rangey":6
            ,"rc_beam_width":0.4
            ,"rc_beam_length":0.6
            ,"rc_secondary_beam_D1":0.6
            ,"rc_secondary_beam_D2":0.4
            ,"basement_wall_height":3
            ,"basement_wall_thickness":0.25
            ,"ground_wall_height":1
            ,"ground_wall_thickness":0.15
            ,"steel_weight":self.steel_check()
            ,"grouting_depth":0.07
            ,"concrete_slab":0.15
            ,"ground_slab" : 0.2
            ,"paraphet_height":0.7
            ,"paraphet_thickness":0.15}
       if self.zero_check(parameter) == 0:
           return parameter_dict.get(key)
       else:
           return parameter


   def comboFloorValues(self,event):
       if self.combo_basement.get() == "YES":
           floor_options = {"basement+1":["Basement","1"],
                            "basement+2":["Basement","1","2"],
                            "basement+3":["Basement","1","2","3"],
                            "basement+4":["Basement","1","2","3","4"],
                            "basement+5":["Basement","1","2","3","4","5"]}
           values = floor_options.get("basement+{}".format(self.spin1.get()))
           self.combo_floor['values'] = values
       elif self.combo_basement.get() == "NO":
           floor_options = {"1": ["1"],
                            "2": ["1", "2"],
                            "3": ["1", "2", "3"],
                            "4": ["1", "2", "3", "4"],
                            "5": ["1", "2", "3", "4", "5"]}
           values = floor_options.get("{}".format(self.spin1.get()))
           self.combo_floor['values'] = values
       else:
           floor_options = {"1": ["1"],
                            "2": ["1", "2"],
                            "3": ["1", "2", "3"],
                            "4": ["1", "2", "3", "4"],
                            "5": ["1", "2", "3", "4", "5"]}
           values = floor_options.get("{}".format(self.spin1.get()))
           self.combo_floor['values'] = values

   def comboFloorValues2(self,storey,basement):
       if basement == "YES":
           floor_options = {"basement+1":["Basement","1"],
                            "basement+2":["Basement","1","2"],
                            "basement+3":["Basement","1","2","3"],
                            "basement+4":["Basement","1","2","3","4"],
                            "basement+5":["Basement","1","2","3","4","5"]}
           values = floor_options.get("basement+{}".format(storey))
           self.combo_floor['values'] = values
       elif basement == "NO":
           floor_options = {"1": ["1"],
                            "2": ["1", "2"],
                            "3": ["1", "2", "3"],
                            "4": ["1", "2", "3", "4"],
                            "5": ["1", "2", "3", "4", "5"]}
           values = floor_options.get("{}".format(storey))
           self.combo_floor['values'] = values



   def add_room(self):
        rm=room()
        rm.basement_height = 3
        try:
            room_area = self.room_area.get()
            room_type = self.none_check(self.room_type.get())
            room_qty = self.room_qty.get()
            floor_no = self.none_check(self.floor.get())
            room_place = self.none_check(self.room_place.get())
            around_rooms = self.none_check(self.around_rooms.get())
            rm.storey_height = self.none_check(float(self.Txtvar_storeyheight.get()))
        except TclError or TypeError:
                self.speech.missing_input()
                messagebox.showerror('Required Fields', 'Please enter missing inputs and select a building from below table\n[BUILDING_NAME, FLOOR_NO, ROOM_TYPE, ROOM_AREA, ROOM_QTY]',icon="warning")
                return
        if self.txt.get() == '' or self.room_area.get() == '' or self.room_type.get() == '' or self.room_qty.get() == '' or self.floor.get() == '' or self.room_place.get == '' or self.around_rooms.get() == '':
            self.speech.missing_input()
            messagebox.showerror('Required Fields', 'Please enter missing inputs and select a building from below tabl\n[BUILDING_NAME, FLOOR_NO, ROOM_TYPE, ROOM_AREA, ROOM_QTY]',icon="warning")
            return
        building_name = self.Txtvar.get()
        rm.structural_type = self.combo_structural_type.get()
        building_area = self.Txtvar_width.get() * self.Txtvar_length.get()
        room_area_check = 0
        door_space = 1.05
        for member in db.fetch_rooms_by_floor(building_name, floor_no):
            #print(member)
            #room_area_check += member[3] * member[4] + float(math.sqrt(member[3])) * door_space
            room_area_check += member[3] * member[4]
            print(f"room area exist = {room_area_check}")
        room_area_check += (room_area) * room_qty
        print(f"room area with new room = {room_area_check}")
        if room_area_check > building_area:
            messagebox.showerror('ERROR', 'TOTAL ROOM AREAS ARE MORE THAN BUILDING AREA!!',icon="warning")
            return

        #1
        inside_brick_wall=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[0]
        # 2
        gypsum_part_wall=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[1]
        # 3
        aliminum_suspended_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[2]
        # 4
        acoustical_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[3]
        # 5
        gypsum_suspended_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[4]
        # 6
        rockwool_suspended_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[5]
        # 7
        non_slip_ceramic_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[6]
        # 8
        glazed_ceramic_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[7]
        # 9
        glazed_ceramic_skirting=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[8]
        # 10
        epoxy_painting_floor=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[9]
        # 11
        resistant_floor=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[10]
        # 12
        acid_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[11]
        # 13
        raised_floor=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[12]
        # 14
        laminated_parquet=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[13]
        # 15
        int_plaster=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[14]
        # 16
        ceiling_plaster=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[15]
        # 17
        ceramic_wall_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[16]
        # 18
        int_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[17]
        # 19
        acid_resistant_int_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[18]
        # 20
        ceiling_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[19]
        # 21
        epoxy_wall_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[20]
        #22
        steel_door1 = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[21]
        # 23
        steel_door2 = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[22]
        # 24
        roller_shutter = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[23]
        # 25
        sliding_steel_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[24]
        # 26
        double_wing_aliminium_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[25]
        # 27
        compacted_laminate_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[26]
        # 28
        wooden_internal_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[27]
        # 29
        aliminum_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[28]
        # 30
        aliminum_double_win_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[29]
        # 31
        screed = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[30]
        db.insert_rooms(self.room_type.get(),self.floor.get(),self.room_area.get(),self.room_qty.get(),inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint,steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,building_name,self.combo_room_place.get(),self.combo_around_rooms.get())
        self.room_list.delete(*self.room_list.get_children())
        self.room_list.insert("",tk.END, values=(self.room_type.get(),self.floor.get(),self.room_area.get(),self.room_qty.get(),building_name))
        self.populate_room_list()

   def show_room(self):
       self.populate_room_list()

   def show_item(self):
       self.populate_list()
       self.add_menu()
       for name in db.fetch_building_names():
           print(name[0])
           if name[1] == "RC":
               self.submenu_type_rc.add_command(label=name[0],command=lambda index=name[0],type=name[1]: self.change_attr(index,type))
           elif name[1] == "STEEL":
               self.submenu_type_steel.add_command(label=name[0], command=lambda index=name[0],type=name[1]: self.change_attr(index,type))

   def select_item(self,event):
        try:
            global selected_item
            selected_item = self.tvStudent.item(self.tvStudent.selection())['values']
            self.comboFloorValues2(selected_item[2],selected_item[12])

            if selected_item[4] == "STEEL":
                self.show_steel_selections()
                if selected_item[7] == "YES":
                    self.combo_floor.place(relx=0.68, rely=0.375, relwidth=0.095, relheight=0.03)
                    self.lbl_floor.place(relx=0.6, rely=0.375, relwidth=0.075, relheight=0.03)
                    self.combo_room_type.place(relx=0.68, rely=0.410, relwidth=0.095, relheight=0.03)
                    self.lbl_room.place(relx=0.6, rely=0.410, relwidth=0.075, relheight=0.03)
                    self.txt_room_area.place(relx=0.68, rely=0.445, relwidth=0.045, relheight=0.03)
                    self.lbl_room_area.place(relx=0.6, rely=0.445, relwidth=0.075, relheight=0.03)
                    self.txt_room_qty.place(relx=0.68, rely=0.480, relwidth=0.045, relheight=0.03)
                    self.lbl_room_qty.place(relx=0.6, rely=0.480, relwidth=0.075, relheight=0.03)
                    self.lbl_room_place.place(relx=0.6, rely=0.515, relwidth=0.075, relheight=0.03)
                    self.combo_room_place.place(relx=0.68, rely=0.515, relwidth=0.045, relheight=0.03)
                    self.lbl_around_rooms.place(relx=0.6, rely=0.55, relwidth=0.075, relheight=0.03)
                    self.combo_around_rooms.place(relx=0.68, rely=0.55, relwidth=0.045, relheight=0.03)
                    self.room_list.place(relx=0.6, rely=0.14, relwidth=0.3675, relheight=0.185)
                    self.scrollbar_room.place(relx=0.9574, rely=0.14, relwidth=0.01, relheight=0.185)
                    self.lbl_room_list.place(relx=0.73, rely=0.1, relwidth=0.075, relheight=0.03)
                    self.room_btn.place(relx=0.777, rely=0.375, relwidth=0.049, relheight=0.03)
                    self.room_btn2.place(relx=0.777, rely=0.410, relwidth=0.049, relheight=0.03)
                    self.room_btn3.place(relx=0.777, rely=0.445, relwidth=0.049, relheight=0.03)
                    self.room_btn4.place(relx=0.777, rely=0.480, relwidth=0.049, relheight=0.03)
                else:
                    self.combo_floor.place_forget()
                    self.lbl_floor.place_forget()
                    self.combo_room_type.place_forget()
                    self.lbl_room.place_forget()
                    self.txt_room_area.place_forget()
                    self.lbl_room_area.place_forget()
                    self.txt_room_qty.place_forget()
                    self.lbl_room_qty.place_forget()
                    self.combo_around_rooms.place_forget()
                    self.combo_room_place.place_forget()
                    self.lbl_room_place.place_forget()
                    self.lbl_around_rooms.place_forget()
                    self.room_list.place_forget()
                    self.scrollbar_room.place_forget()
                    self.lbl_room_list.place_forget()
                    self.room_btn.place_forget()
                    self.room_btn2.place_forget()
                    self.room_btn3.place_forget()
                    self.room_btn4.place_forget()
            elif selected_item[4] =="RC":
                self.clear_text_rc()
                self.txt.delete(0, tk.END)
                self.txt.insert(tk.END, selected_item[1])
                self.spin1.delete(0, tk.END)
                self.spin1.set(selected_item[2])
                self.txt_storeyheight.delete(0, tk.END)
                self.txt_storeyheight.insert(tk.END, selected_item[3])
                self.combo_structural_type.delete(0, tk.END)
                self.combo_structural_type.set(selected_item[4])
                self.combo_insulation.delete(0, tk.END)
                self.combo_insulation.set(selected_item[6])
                self.combo_soil.delete(0, tk.END)
                self.combo_soil.set(selected_item[9])
                self.combo_found_beam.delete(0, tk.END)
                self.combo_found_beam.set(selected_item[10])
                self.combo_found_wall.delete(0, tk.END)
                self.combo_found_wall.set(selected_item[11])
                self.combo_basement.delete(0, tk.END)
                self.combo_basement.set(selected_item[12])
                self.txt_width.delete(0, tk.END)
                self.txt_width.insert(tk.END, selected_item[13])
                self.txt_length.delete(0, tk.END)
                self.txt_length.insert(tk.END, selected_item[14])
                self.foundation_selection(event)
                self.combo_floor.place(relx=0.68, rely=0.375, relwidth=0.095, relheight=0.03)
                self.lbl_floor.place(relx=0.6, rely=0.375, relwidth=0.075, relheight=0.03)
                self.combo_room_type.place(relx=0.68, rely=0.410, relwidth=0.095, relheight=0.03)
                self.lbl_room.place(relx=0.6, rely=0.410, relwidth=0.075, relheight=0.03)
                self.txt_room_area.place(relx=0.68, rely=0.445, relwidth=0.045, relheight=0.03)
                self.lbl_room_area.place(relx=0.6, rely=0.445, relwidth=0.075, relheight=0.03)
                self.txt_room_qty.place(relx=0.68, rely=0.480, relwidth=0.045, relheight=0.03)
                self.lbl_room_qty.place(relx=0.6, rely=0.480, relwidth=0.075, relheight=0.03)
                self.lbl_room_place.place(relx=0.6, rely=0.515, relwidth=0.075, relheight=0.03)
                self.combo_room_place.place(relx=0.68, rely=0.515, relwidth=0.045, relheight=0.03)
                self.lbl_around_rooms.place(relx=0.6, rely=0.55, relwidth=0.075, relheight=0.03)
                self.combo_around_rooms.place(relx=0.68, rely=0.55, relwidth=0.045, relheight=0.03)
                self.room_list.place(relx=0.6, rely=0.14, relwidth=0.3675, relheight=0.185)
                self.scrollbar_room.place(relx=0.9574, rely=0.14, relwidth=0.01, relheight=0.185)
                self.lbl_room_list.place(relx=0.73, rely=0.1, relwidth=0.075, relheight=0.03)
                self.room_btn.place(relx=0.777, rely=0.375, relwidth=0.049, relheight=0.03)
                self.room_btn2.place(relx=0.777, rely=0.410, relwidth=0.049, relheight=0.03)
                self.room_btn3.place(relx=0.777, rely=0.445, relwidth=0.049, relheight=0.03)
                self.room_btn4.place(relx=0.777, rely=0.480, relwidth=0.049, relheight=0.03)
        except IndexError:
            pass

   def show_steel_selections(self):
       self.txt.delete(0, tk.END)
       self.txt.insert(tk.END, selected_item[1])
       self.spin1.delete(0, tk.END)
       self.spin1.set(selected_item[2])
       self.txt_storeyheight.delete(0, tk.END)
       self.txt_storeyheight.insert(tk.END, selected_item[3])
       self.combo_structural_type.delete(0, tk.END)
       self.combo_structural_type.set(selected_item[4])
       self.combo_soil.delete(0, tk.END)
       self.combo_soil.set(selected_item[9])
       self.combo_found_beam.delete(0, tk.END)
       self.combo_found_beam.set(selected_item[10])
       self.combo_found_wall.delete(0, tk.END)
       self.combo_found_wall.set(selected_item[11])
       self.combo_basement.delete(0, tk.END)
       self.combo_basement.set(selected_item[12])
       self.txt_width.delete(0, tk.END)
       self.txt_width.insert(tk.END, selected_item[13])
       self.txt_length.delete(0, tk.END)
       self.txt_length.insert(tk.END, selected_item[14])
       self.combo_steeltype.delete(0, tk.END)
       self.combo_steeltype.set(selected_item[5])
       self.combo_insulation.delete(0, tk.END)
       self.combo_insulation.set(selected_item[6])
       self.combo_seperated_room.delete(0, tk.END)
       self.combo_seperated_room.set(selected_item[7])
       self.mf_spin.delete(0, tk.END)
       self.mf_spin.set(selected_item[8])
       self.combo_steeltype.place(relx=0.1904, rely=0.225, relwidth=0.075, relheight=0.03)
       self.lbl_insulation['text'] = "INSULATION"
       self.combo_insulation['values'] = ('CLADDING', 'SHEET')
       self.lbl_insulation.place(relx=0.43, rely=0.3, relwidth=0.075, relheight=0.03)
       self.combo_insulation.place(relx=0.51, rely=0.3, relwidth=0.075, relheight=0.03)
       self.lbl_middle_floor.place(relx=0.458, rely=0.225, relwidth=0.085, relheight=0.03)
       self.mf_spin.place(relx=0.546, rely=0.225, relwidth=0.045, relheight=0.03)
       self.lbl_seperated_room.place(relx=0.28, rely=0.225, relwidth=0.095, relheight=0.03)
       self.combo_seperated_room.place(relx=0.38, rely=0.225, relwidth=0.0675, relheight=0.03)
       self.lbl_found_beam.place(relx=0.26, rely=0.3, relwidth=0.1, relheight=0.03)
       self.combo_found_beam.place(relx=0.364, rely=0.3, relwidth=0.05, relheight=0.03)
       self.lbl_found_wall.place(relx=0.26, rely=0.35, relwidth=0.1, relheight=0.03)
       self.combo_found_wall.place(relx=0.364, rely=0.35, relwidth=0.05, relheight=0.03)


   def select_room(self,event):
        try:
            global selected_room
            #index = self.room_list.curselection()[0]
            #selected_room = self.room_list.get(index)
            selected_room = self.room_list.item(self.room_list.selection())['values']

            self.combo_floor.delete(0, tk.END)
            self.combo_floor.set(selected_room[2])
            self.combo_room_type.delete(0, tk.END)
            self.combo_room_type.set(selected_room[1])
            self.txt_room_area.delete(0, tk.END)
            self.txt_room_area.insert(tk.END, selected_room[3])
            self.txt_room_qty.delete(0, tk.END)
            self.txt_room_qty.insert(tk.END, selected_room[4])
            self.combo_room_place.delete(0, tk.END)
            self.combo_room_place.set(selected_room[5])
            self.combo_around_rooms.delete(0, tk.END)
            self.combo_around_rooms.set(selected_room[6])
        except IndexError:
            pass


   def remove_item(self):
        db.remove(selected_item[0])
        self.clear_text()
        self.populate_list()
        self.add_menu()
        for name in db.fetch_building_names():
            print(name[0])
            if name[1]=="RC":
                self.submenu_type_rc.add_command(label=name[0],command=lambda index=name[0], type=name[1]: self.change_attr(index,type))
            elif name[1] == "STEEL":
                self.submenu_type_steel.add_command(label=name[0],command=lambda index=name[0], type=name[1]: self.change_attr(index,type))

   def remove_room(self):
        db.remove_rooms(selected_room[0])
        self.populate_room_list()


   def update_item(self):
       # DEFAULTS UPDATE
        self.empty_check()
        model = ml_model()
        start_time = time.time()
        widthcode = model.predict(self.Txtvar_width.get(), self.Txtvar_length.get(), self.Txtvar_storeyheight.get())[0]
        lengthcode = model.predict(self.Txtvar_width.get(), self.Txtvar_length.get(), self.Txtvar_storeyheight.get())[1]
        storeycode = model.predict(self.Txtvar_width.get(), self.Txtvar_length.get(), self.Txtvar_storeyheight.get())[2]
        storeyno = self.spin1.get()
        encoded_params = model.encode_parameters(self.combo_structural_type.get(), self.combo_soil.get(),self.combo_found_beam.get(), self.combo_found_wall.get(),self.combo_basement.get())
        structuraltype = encoded_params[0]
        foundationtype = encoded_params[1]
        foundation_beam = encoded_params[2]
        foundation_ground_wall = encoded_params[3]
        basement = encoded_params[4]
        print(storeyno, int(storeycode), structuraltype, foundationtype, foundation_beam, foundation_ground_wall,int(widthcode), int(lengthcode))
        model.create_data_table()
        params = db.parameter_selection(storeyno, int(storeycode), structuraltype, foundationtype, foundation_beam,foundation_ground_wall, int(widthcode), int(lengthcode))
        if len(params) != 0:
           for row in params:
               print(row)
               exc_depth = self.parameter_check(row[0], "exc_depth")
               strfill_depth = self.parameter_check(row[1], "strfill_depth")
               foundation_depth = self.parameter_check(row[2], "foundation_depth")
               foundation_D1 = self.parameter_check(row[3], "foundation_D1")
               foundation_D2 = self.parameter_check(row[4], "foundation_D2")
               tie_beam_d1 = self.parameter_check(row[5], "tie_beam_d1")
               tie_beam_d2 = self.parameter_check(row[6], "tie_beam_d2")
               steel_pedestal_d1 = self.parameter_check(row[7], "steel_pedestal_d1")
               steel_pedestal_d2 = self.parameter_check(row[8], "steel_pedestal_d2")
               steel_pedestal_depth = self.parameter_check(row[9], "steel_pedestal_depth")
               steel_pedestal_rangex = self.parameter_check(row[10], "steel_pedestal_rangex")
               steel_pedestal_rangey = self.parameter_check(row[11], "steel_pedestal_rangey")
               rc_column_width = self.parameter_check(row[12], "rc_column_width")
               rc_column_length = self.parameter_check(row[13], "rc_column_length")
               rc_column_rangex = self.parameter_check(row[14], "rc_column_rangex")
               rc_column_rangey = self.parameter_check(row[15], "rc_column_rangey")
               rc_beam_width = self.parameter_check(row[16], "rc_beam_width")
               rc_beam_length = self.parameter_check(row[17], "rc_beam_length")
               rc_secondary_beam_D1 = self.parameter_check(row[18], "rc_secondary_beam_D1")
               rc_secondary_beam_D2 = self.parameter_check(row[19], "rc_secondary_beam_D2")
               basement_wall_height = self.parameter_check(row[20], "basement_wall_height")
               basement_wall_thickness = self.parameter_check(row[21], "basement_wall_thickness")
               ground_wall_height = self.parameter_check(row[20], "ground_wall_height")
               ground_wall_thickness = self.parameter_check(row[21], "ground_wall_thickness")
               steel_weight = self.parameter_check(self.steel_check(), "steel_weight")
               grouting_depth = self.parameter_check(0.07, "grouting_depth")
               concrete_slab = self.parameter_check(row[22], "concrete_slab")
               ground_slab = self.parameter_check(row[23], "ground_slab")
               paraphet_height = self.parameter_check(row[25], "paraphet_height")
               paraphet_thickness = self.parameter_check(row[24], "paraphet_thickness")
        else:
           strfill_depth = 1  # ok
           foundation_depth = 0.51
           foundation_D1 = 2.5
           foundation_D2 = 3
           tie_beam_d1 = 1
           tie_beam_d2 = 0.55
           steel_pedestal_d1 = 0.7
           steel_pedestal_d2 = 0.65
           steel_pedestal_depth = 1.3
           steel_pedestal_rangex = 6
           steel_pedestal_rangey = 7
           rc_column_width = 0.6
           rc_column_length = 0.6
           rc_column_rangex = 6
           rc_column_rangey = 6
           rc_beam_width = 0.4
           rc_beam_length = 0.6
           rc_secondary_beam_D1 = 0.6
           rc_secondary_beam_D2 = 0.4
           basement_wall_height = 3
           basement_wall_thickness = 0.25
           ground_wall_height = 1
           ground_wall_thickness = 0.15
           steel_weight = self.steel_check()
           grouting_depth = 0.07
           concrete_slab = 0.15
           ground_slab = 0.2
           paraphet_height = 0.7
           paraphet_thickness = 0.15
           exc_depth = self.basement_check(foundation_depth,strfill_depth,basement_wall_height)  # ok

        self.excavationCheck(exc_depth, strfill_depth, foundation_depth,self.combo_basement.get(),basement_wall_height)
        db.update(selected_item[0], self.Txtvar.get(), self.spin1.get(),self.Txtvar_storeyheight.get(), self.combo_structural_type.get(),self.combo_steeltype.get(),self.combo_insulation.get(),self.combo_seperated_room.get(),self.mf_spin.get(),self.combo_soil.get(),self.combo_found_beam.get(),self.combo_found_wall.get(),self.combo_basement.get(),self.Txtvar_width.get(),self.Txtvar_length.get(),exc_depth, strfill_depth,foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2, steel_pedestal_d1,steel_pedestal_d2, steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rc_column_width, rc_column_length, rc_column_rangex, rc_column_rangey, basement_wall_height, basement_wall_thickness, ground_wall_height, ground_wall_thickness, steel_weight, grouting_depth, rc_beam_width,rc_beam_length, rc_secondary_beam_D1, rc_secondary_beam_D2, concrete_slab, ground_slab, paraphet_height, paraphet_thickness)
        self.populate_list()
        self.add_menu()

        if self.combo_structural_type.get() =="RC":
            messagebox.showinfo("UPDATED PARAMETERS"
                    ,"exc_depth: {}".format(exc_depth)+
                    "\nstrfill_depth: {}".format(strfill_depth)+
                    "\nfoundation_depth: {}".format(foundation_depth)+
                    "\nfoundation_D1: {}".format(foundation_D1)+
                    "\nfoundation_D2: {}".format(foundation_D2)+
                    "\ntie_beam_d1: {}".format(tie_beam_d1)+
                    "\ntie_beam_d2: {}".format(tie_beam_d2)+
                    "\nrc_column_width: {}".format(rc_column_width)+
                    "\nrc_column_length: {}".format(rc_column_length)+
                    "\nrc_column_rangex: {}".format(rc_column_rangex)+
                    "\nrc_column_rangey: {}".format(rc_column_rangey)+
                    "\nrc_beam_width: {}".format(rc_beam_width)+
                    "\nrc_beam_length: {}".format(rc_beam_length)+
                    "\nrc_secondary_beam_D1: {}".format(rc_secondary_beam_D1)+
                    "\nrc_secondary_beam_D2: {}".format(rc_secondary_beam_D2)+
                    "\nbasement_wall_height: {}".format(basement_wall_height)+
                    "\nbasement_wall_thickness: {}".format(basement_wall_thickness)+
                    "\nground_wall_height: {}".format(ground_wall_height)+
                    "\nground_wall_thickness: {}".format(ground_wall_thickness)+
                    "\nconcrete_slab: {}".format(concrete_slab)+
                    "\nground_slab: {}".format(ground_slab)+
                    "\nparaphet_height: {}".format(paraphet_height)+
                    "\nparaphet_thickness: {}".format(paraphet_thickness)+
                    "\n-------------------------------------"
                    "\n GO OPTIONS MENU TO MAKE ANY CHANGE"
                               , icon="info")
        elif self.combo_structural_type.get() =="STEEL":
            messagebox.showinfo("UPDATED PARAMETERS"
                                , "exc_depth: {}".format(exc_depth) +
                                "\nstrfill_depth: {}".format(strfill_depth) +
                                "\nfoundation_depth: {}".format(foundation_depth) +
                                "\nfoundation_D1: {}".format(foundation_D1) +
                                "\nfoundation_D2: {}".format(foundation_D2) +
                                "\ntie_beam_d1: {}".format(tie_beam_d1) +
                                "\ntie_beam_d2: {}".format(tie_beam_d2) +
                                "\nsteel_pedestal_d1: {}".format(steel_pedestal_d1) +
                                "\nsteel_pedestal_d2: {}".format(steel_pedestal_d2) +
                                "\nsteel_pedestal_depth: {}".format(steel_pedestal_depth) +
                                "\nsteel_pedestal_rangex: {}".format(steel_pedestal_rangex) +
                                "\nsteel_pedestal_rangey: {}".format(steel_pedestal_rangey) +
                                "\nground_wall_height: {}".format(ground_wall_height) +
                                "\nground_wall_thickness: {}".format(ground_wall_thickness) +
                                "\nsteel_weight: {}".format(steel_weight) +
                                "\ngrouting_depth: {}".format(grouting_depth) +
                                "\nconcrete_slab: {}".format(concrete_slab) +
                                "\nground_slab: {}".format(ground_slab) +
                                "\n-------------------------------------"
                                "\n GO OPTIONS MENU TO MAKE ANY CHANGE"
                                , icon="info")
        for name in db.fetch_building_names():
            print(name[0])
            if name[1]=="RC":
                self.submenu_type_rc.add_command(label=name[0],command=lambda index=name[0], type=name[1]: self.change_attr(index,type))
            elif name[1] == "STEEL":
                self.submenu_type_steel.add_command(label=name[0],command=lambda index=name[0], type=name[1]: self.change_attr(index,type))

   def update_room(self):
       #DEFAULTS UPDATE
        rm = room()
        rm.storey_height = self.none_check(self.Txtvar_storeyheight.get())
        rm.basement_height = 3
        try:
            room_area = self.room_area.get()
            room_type = self.none_check(self.room_type.get())
            room_qty = self.room_qty.get()
            floor_no = self.none_check(self.floor.get())
            room_place = self.none_check(self.room_place.get())
            around_rooms = self.none_check(self.around_rooms.get())
            rm.storey_height = self.none_check(self.Txtvar_storeyheight.get())
        except TclError or TypeError:
                messagebox.showerror('Required Fields', 'Please enter missing inputs and select a building from below table\n[BUILDING_NAME, FLOOR_NO, ROOM_TYPE, ROOM_AREA, ROOM_QTY]',icon="warning")
                return
        if self.Txtvar.get() == '' or self.room_area.get() == '' or self.room_type.get() == '' or self.room_qty.get() == '' or self.floor.get() == '' or self.room_place.get == '' or self.around_rooms.get() == '':
            messagebox.showerror('Required Fields', 'Please enter missing inputs and select a building from below tabl\n[BUILDING_NAME, FLOOR_NO, ROOM_TYPE, ROOM_AREA, ROOM_QTY]',icon="warning")
            return
        building_name = self.Txtvar.get()
        rm.structural_type = self.combo_structural_type.get()
        building_area = self.Txtvar_width.get() * self.Txtvar_length.get()
        if room_type == 0:
            messagebox.showerror('ERROR', 'PLEASE SELECT ROOM TYPE')
        #1
        inside_brick_wall=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[0]
        # 2
        gypsum_part_wall=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[1]
        # 3
        aliminum_suspended_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[2]
        # 4
        acoustical_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[3]
        # 5
        gypsum_suspended_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[4]
        # 6
        rockwool_suspended_ceiling=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[5]
        # 7
        non_slip_ceramic_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[6]
        # 8
        glazed_ceramic_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[7]
        # 9
        glazed_ceramic_skirting=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[8]
        # 10
        epoxy_painting_floor=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[9]
        # 11
        resistant_floor=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[10]
        # 12
        acid_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[11]
        # 13
        raised_floor=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[12]
        # 14
        laminated_parquet=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[13]
        # 15
        int_plaster=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[14]
        # 16
        ceiling_plaster=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[15]
        # 17
        ceramic_wall_tile=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[16]
        # 18
        int_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[17]
        # 19
        acid_resistant_int_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[18]
        # 20
        ceiling_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[19]
        # 21
        epoxy_wall_paint=rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[20]
        #22
        steel_door1 = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[21]
        # 23
        steel_door2 = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[22]
        # 24
        roller_shutter = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[23]
        # 25
        sliding_steel_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[24]
        # 26
        double_wing_aliminium_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[25]
        # 27
        compacted_laminate_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[26]
        # 28
        wooden_internal_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[27]
        # 29
        aliminum_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[28]
        # 30
        aliminum_double_win_door = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[29]
        # 31
        screed = rm.rooms(self.room_type.get(),room_area,room_qty,floor_no,room_place,around_rooms)[30]

        room_area_check = []
        door_space = 1.05
        for member in db.fetch_rooms_by_floor(building_name, floor_no):
           # print(member)
           room_area_check.append(member[3] * member[4])
           print(f"room area exist = {sum(room_area_check)}")
        room_area_new = sum(room_area_check[:-1]) + room_area * room_qty
        print(f"room area new = {room_area_new}")
        if room_area_new > building_area:
           messagebox.showerror('ERROR', 'TOTAL ROOM AREAS ARE MORE THAN BUILDING AREA!!',icon="warning")
           return
        else:
            db.update_rooms(selected_room[0], self.room_type.get(), self.floor.get(), self.room_area.get(),
                            self.room_qty.get(), inside_brick_wall, gypsum_part_wall, aliminum_suspended_ceiling,
                            acoustical_ceiling, gypsum_suspended_ceiling, rockwool_suspended_ceiling,
                            non_slip_ceramic_tile, glazed_ceramic_tile, glazed_ceramic_skirting, epoxy_painting_floor,
                            resistant_floor, acid_tile, raised_floor, laminated_parquet, int_plaster, ceiling_plaster,
                            ceramic_wall_tile, int_paint, acid_resistant_int_paint, ceiling_paint, epoxy_wall_paint,
                            steel_door1, steel_door2, roller_shutter, sliding_steel_door, double_wing_aliminium_door,
                            compacted_laminate_door, wooden_internal_door, aliminum_door, aliminum_double_win_door,
                            screed, building_name, self.combo_room_place.get(), self.combo_around_rooms.get())

        self.populate_room_list()

   def on_closing(self):
       if messagebox.askokcancel("Quit", "Do you want to quit?"):
           self.destroy()

   def reset_project(self):
       if messagebox.askokcancel("Reset", "Do you want to reset database?"):
           db.deleteFromBuildings()
           db.deleteFromRooms()
           self.clear_all()
           self.populate_list()
           self.populate_room_list()


   def change_attr(self,index,type):
        def edit(event):
            if parameter_list.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list.identify_column(event.x)  # identify column
                print(parameter_list.heading(column, 'text'))
                def ok(event):
                    """Change item value."""
                    parameter_list.set(item, column, entry.get())
                    selected_parameter = parameter_list.item(parameter_list.selection())['values']
                    db.update_parameters(parameter_list.heading(column, 'text'),entry.get(),index)
                    print(index)
                    entry.destroy()

                column = parameter_list.identify_column(event.x)  # identify column
                item = parameter_list.identify_row(event.y)  # identify item
                x, y, width, height = parameter_list.bbox(item, column)
                value = parameter_list.set(item, column)

            elif parameter_list.identify_region(event.x, event.y) == 'nothing':
                column = parameter_list.identify_column(event.x)  # identify column
                # check whether we are below the last row:
                x, y, width, height = parameter_list.bbox(parameter_list.get_children('')[-1], column)
                if event.y > y:

                    def ok(event):
                        """Change item value."""
                        # create item
                        item = parameter_list.insert("", "end", values=("", ""))
                        parameter_list.set(item, column, entry.get())
                        entry.destroy()

                    y += height
                    value = ""
                else:
                    return
            else:
                return
            # display the Entry
            entry = ttk.Entry(parameter_list)  # create edition entry
            entry.place(x=x, y=y, width=width, height=height,
                        anchor='nw')  # display entry on top of cell
            entry.insert(0, value)  # put former value in entry
            entry.bind('<FocusOut>', lambda e: entry.destroy())
            entry.bind('<Return>', ok)  # validate with Enter
            entry.focus_set()
        def edit2(event):
            if parameter_list2.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list2.identify_column(event.x)  # identify column
                print(parameter_list2.heading(column, 'text'))
                def ok(event):
                    """Change item value."""
                    parameter_list2.set(item, column, entry.get())
                    selected_parameter = parameter_list2.item(parameter_list2.selection())['values']
                    db.update_parameters(parameter_list2.heading(column, 'text'),entry.get(),index)
                    print(index)
                    entry.destroy()

                column = parameter_list2.identify_column(event.x)  # identify column
                item = parameter_list2.identify_row(event.y)  # identify item
                x, y, width, height = parameter_list2.bbox(item, column)
                value = parameter_list2.set(item, column)

            elif parameter_list2.identify_region(event.x, event.y) == 'nothing':
                column = parameter_list2.identify_column(event.x)  # identify column
                # check whether we are below the last row:
                x, y, width, height = parameter_list2.bbox(parameter_list2.get_children('')[-1], column)
                if event.y > y:

                    def ok(event):
                        """Change item value."""
                        # create item
                        item = parameter_list2.insert("", "end", values=("", ""))
                        parameter_list2.set(item, column, entry.get())
                        entry.destroy()

                    y += height
                    value = ""
                else:
                    return
            else:
                return
            # display the Entry
            entry = ttk.Entry(parameter_list2)  # create edition entry
            entry.place(x=x, y=y, width=width, height=height,
                        anchor='nw')  # display entry on top of cell
            entry.insert(0, value)  # put former value in entry
            entry.bind('<FocusOut>', lambda e: entry.destroy())
            entry.bind('<Return>', ok)  # validate with Enter
            entry.focus_set()
        def edit3(event):
            if parameter_list3.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list3.identify_column(event.x)  # identify column
                print(parameter_list3.heading(column, 'text'))
                def ok(event):
                    """Change item value."""
                    parameter_list3.set(item, column, entry.get())
                    selected_parameter = parameter_list3.item(parameter_list3.selection())['values']
                    db.update_parameters(parameter_list3.heading(column, 'text'),entry.get(),index)
                    print(index)
                    entry.destroy()

                column = parameter_list3.identify_column(event.x)  # identify column
                item = parameter_list3.identify_row(event.y)  # identify item
                x, y, width, height = parameter_list3.bbox(item, column)
                value = parameter_list3.set(item, column)

            elif parameter_list3.identify_region(event.x, event.y) == 'nothing':
                column = parameter_list3.identify_column(event.x)  # identify column
                # check whether we are below the last row:
                x, y, width, height = parameter_list3.bbox(parameter_list3.get_children('')[-1], column)
                if event.y > y:

                    def ok(event):
                        """Change item value."""
                        # create item
                        item = parameter_list3.insert("", "end", values=("", ""))
                        parameter_list3.set(item, column, entry.get())
                        entry.destroy()

                    y += height
                    value = ""
                else:
                    return
            else:
                return
            # display the Entry
            entry = ttk.Entry(parameter_list3)  # create edition entry
            entry.place(x=x, y=y, width=width, height=height,
                        anchor='nw')  # display entry on top of cell
            entry.insert(0, value)  # put former value in entry
            entry.bind('<FocusOut>', lambda e: entry.destroy())
            entry.bind('<Return>', ok)  # validate with Enter
            entry.focus_set()
        def edit4(event):
            if parameter_list4.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list4.identify_column(event.x)  # identify column
                print(parameter_list4.heading(column, 'text'))
                def ok(event):
                    """Change item value."""
                    parameter_list4.set(item, column, entry.get())
                    selected_parameter = parameter_list4.item(parameter_list4.selection())['values']
                    db.update_parameters(parameter_list4.heading(column, 'text'),entry.get(),index)
                    print(index)
                    entry.destroy()

                column = parameter_list4.identify_column(event.x)  # identify column
                item = parameter_list4.identify_row(event.y)  # identify item
                x, y, width, height = parameter_list4.bbox(item, column)
                value = parameter_list4.set(item, column)

            elif parameter_list4.identify_region(event.x, event.y) == 'nothing':
                column = parameter_list4.identify_column(event.x)  # identify column
                # check whether we are below the last row:
                x, y, width, height = parameter_list4.bbox(parameter_list4.get_children('')[-1], column)
                if event.y > y:

                    def ok(event):
                        """Change item value."""
                        # create item
                        item = parameter_list4.insert("", "end", values=("", ""))
                        parameter_list4.set(item, column, entry.get())
                        entry.destroy()

                    y += height
                    value = ""
                else:
                    return
            else:
                return
            # display the Entry
            entry = ttk.Entry(parameter_list4)  # create edition entry
            entry.place(x=x, y=y, width=width, height=height,
                        anchor='nw')  # display entry on top of cell
            entry.insert(0, value)  # put former value in entry
            entry.bind('<FocusOut>', lambda e: entry.destroy())
            entry.bind('<Return>', ok)  # validate with Enter
            entry.focus_set()

        top = Toplevel(self)
        top.title("{} DIMENSIONS".format(index))
        top.config(background="black")
        #w = self.winfo_screenwidth()
        w=550
        h = 220
        top.geometry("{}x{}".format(w,h))
        column_parameter_rc = ("#1", "#2", "#3", "#4", "#5", "#6")
        column_parameter_rc2 = ("#1", "#2", "#3", "#4", "#5")
        column_parameter_steel = ("#1", "#2", "#3", "#4", "#5", "#6")
        if type =="RC":
            w = 750
            h = 180
            top.geometry("{}x{}".format(w, h))

            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_rc,
                                          style="Custom.Treeview")
            parameter_list.heading('#1', text='exc_depth', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='strfill_depth', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='foundation_depth', anchor='center')
            parameter_list.column('#3', width=40, anchor='center', stretch=True)
            parameter_list.heading('#4', text='foundation_D1', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='foundation_D2', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='tie_beam_d1', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)

            parameter_list.pack(fill = BOTH, expand = True)
            parameter_list.bind('<1>', edit)
            # parameter_list.delete(0,END)
            for param in db.fetch_parameters(index, type):
                print(param)
                parameter_list.insert("", tk.END, values=param)
        #SECOND ROW
            parameter_list2 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_rc,
                                          style="Custom.Treeview")
            parameter_list2.heading('#1', text='tie_beam_d2', anchor='center')
            parameter_list2.column('#1', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#2', text='rc_column_width', anchor='center')
            parameter_list2.column('#2', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#3', text='rc_column_length', anchor='center')
            parameter_list2.column('#3', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#4', text='rc_column_rangex', anchor='center')
            parameter_list2.column('#4', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#5', text='rc_column_rangey', anchor='center')
            parameter_list2.column('#5', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#6', text='basement_wall_height', anchor='center')
            parameter_list2.column('#6', width=40, anchor='center', stretch=True)

            parameter_list2.pack(fill = BOTH, expand = True)
            parameter_list2.bind('<1>', edit2)

            # parameter_list2.delete(0,END)
            for param in db.fetch_parameters2(index, type):
                print(param)
                parameter_list2.insert("", tk.END, values=param)
        #THIRD ROW
            parameter_list3 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_rc,
                                          style="Custom.Treeview")
            parameter_list3.heading('#1', text='basement_wall_thickness', anchor='center')
            parameter_list3.column('#1', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#2', text='ground_wall_height', anchor='center')
            parameter_list3.column('#2', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#3', text='ground_wall_thickness', anchor='center')
            parameter_list3.column('#3', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#4', text='rc_beam_width', anchor='center')
            parameter_list3.column('#4', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#5', text='rc_beam_length', anchor='center')
            parameter_list3.column('#5', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#6', text='rc_secondary_beam_D1', anchor='center')
            parameter_list3.column('#6', width=40, anchor='center', stretch=True)

            parameter_list3.pack(fill = BOTH, expand = True)
            parameter_list3.bind('<1>', edit3)

            # parameter_list3.delete(0,END)
            for param in db.fetch_parameters3(index, type):
                print(param)
                parameter_list3.insert("", tk.END, values=param)
        #FOURTH ROW
            parameter_list4 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_rc2,
                                          style="Custom.Treeview")
            parameter_list4.heading('#1', text='rc_secondary_beam_D2', anchor='center')
            parameter_list4.column('#1', width=40, anchor='center', stretch=True)
            parameter_list4.heading('#2', text='concrete_slab', anchor='center')
            parameter_list4.column('#2', width=40, anchor='center', stretch=True)
            parameter_list4.heading('#3', text='ground_slab', anchor='center')
            parameter_list4.column('#3', width=40, anchor='center', stretch=True)
            parameter_list4.heading('#4', text='paraphet_height', anchor='center')
            parameter_list4.column('#4', width=40, anchor='center', stretch=True)
            parameter_list4.heading('#5', text='paraphet_thickness', anchor='center')
            parameter_list4.column('#5', width=40, anchor='center', stretch=True)

            parameter_list4.pack(fill = BOTH, expand = True)
            parameter_list4.bind('<1>', edit4)

            # parameter_list4.delete(0,END)
            for param in db.fetch_parameters4(index, type):
                print(param)
                parameter_list4.insert("", tk.END, values=param)
        elif type =="STEEL":
            w = 750
            h = 135
            top.geometry("{}x{}".format(w, h))
            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_steel,
                                          style="Custom.Treeview")
            parameter_list.heading('#1', text='exc_depth', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='strfill_depth', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='foundation_depth', anchor='center')
            parameter_list.column('#3', width=40, anchor='center', stretch=True)
            parameter_list.heading('#4', text='foundation_D1', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='foundation_D2', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='tie_beam_d1', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)

            parameter_list.pack(fill = BOTH, expand = True)
            parameter_list.bind('<1>', edit)
            # parameter_list.delete(0,END)
            for param in db.fetch_parameters(index, type):
                print(param)
                parameter_list.insert("", tk.END, values=param)

            parameter_list2 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_steel,
                                          style="Custom.Treeview")

            parameter_list2.heading('#1', text='tie_beam_d2', anchor='center')
            parameter_list2.column('#1', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#2', text='steel_pedestal_d1', anchor='center')
            parameter_list2.column('#2', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#3', text='steel_pedestal_d2', anchor='center')
            parameter_list2.column('#3', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#4', text='steel_pedestal_depth', anchor='center')
            parameter_list2.column('#4', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#5', text='steel_pedestal_rangex', anchor='center')
            parameter_list2.column('#5', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#6', text='steel_pedestal_rangey', anchor='center')
            parameter_list2.column('#6', width=40, anchor='center', stretch=True)

            parameter_list2.pack(fill = BOTH, expand = True)
            parameter_list2.bind('<1>', edit2)
            # parameter_list.delete(0,END)
            for param in db.fetch_parameters2(index, type):
                print(param)
                parameter_list2.insert("", tk.END, values=param)

            parameter_list3 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_steel,
                                          style="Custom.Treeview")

            parameter_list3.heading('#1', text='ground_wall_height', anchor='center')
            parameter_list3.column('#1', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#2', text='ground_wall_thickness', anchor='center')
            parameter_list3.column('#2', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#3', text='steel_weight', anchor='center')
            parameter_list3.column('#3', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#4', text='grouting_depth', anchor='center')
            parameter_list3.column('#4', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#5', text='concrete_slab', anchor='center')
            parameter_list3.column('#5', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#6', text='ground_slab', anchor='center')
            parameter_list3.column('#6', width=40, anchor='center', stretch=True)

            parameter_list3.pack(fill = BOTH, expand = True)
            parameter_list3.bind('<1>', edit3)
            # parameter_list.delete(0,END)
            for param in db.fetch_parameters3(index, type):
                print(param)
                parameter_list3.insert("", tk.END, values=param)

   def clear_text(self):
        #Txtvar.get(), spin1.get(),Txtvar_storeyheight.get(), combo_structural_type.get(),combo_steeltype.get(),combo_insulation.get(),combo_thickness.get(),combo_material.get(),combo_soil.get(),combo_basement.get(),Txtvar_width.get(),Txtvar_length.get()
        self.txt.delete(0, tk.END)
        self.txt_storeyheight.delete(0, tk.END)
        self.txt_width.delete(0, tk.END)
        self.txt_length.delete(0, tk.END)
        self.spin1.delete(0, tk.END)

        if self.combo_structural_type.current() == 0:
            self.clear_text_steel()
            self.combo_structural_type.set('')
            self.spin1.delete(0,"end")
            self.combo_steeltype.place_forget()
            self.combo_steeltype.set('')
            self.lbl_insulation.place_forget()
            self.combo_insulation.place_forget()
            self.lbl_middle_floor.place_forget()
            self.mf_spin.place_forget()
            self.lbl_seperated_room.place_forget()
            self.combo_seperated_room.place_forget()

        elif self.combo_structural_type.current() == 1:
            self.clear_text_rc()
            self.combo_structural_type.set('')
            self.spin1.delete(0, "end")

   def clear_all(self):
       self.txt.delete(0, tk.END)
       self.txt_storeyheight.delete(0, tk.END)
       self.txt_width.delete(0, tk.END)
       self.txt_length.delete(0, tk.END)
       self.spin1.delete(0, tk.END)
       self.combo_structural_type.set('')
       self.clear_text_rc()
       self.clear_text_steel()

   def clear_text_rc(self):
       self.lbl_insulation.place_forget()
       self.combo_insulation.place_forget()
       self.combo_insulation.set('')
       self.combo_steeltype.place_forget()
       self.combo_steeltype.set('')
       self.lbl_middle_floor.place_forget()
       self.mf_spin.place_forget()
       self.mf_spin.delete(0, tk.END)
       self.lbl_seperated_room.place_forget()
       self.combo_seperated_room.place_forget()
       self.combo_seperated_room.set('')
       self.lbl_found_wall.place_forget()
       self.combo_found_wall.place_forget()
       self.combo_found_wall.set('')
       self.lbl_found_beam.place_forget()
       self.combo_found_beam.place_forget()
       self.combo_found_beam.set('')
       self.combo_basement.set('')
       self.combo_soil.set('')
       self.txt_room_area.delete(0,tk.END)
       self.txt_room_qty.delete(0,"end")
       self.combo_floor.set('')
       self.combo_room_type.set('')
       self.combo_room_place.set('')
       self.combo_around_rooms.set('')

       self.combo_floor.place(relx=0.68, rely=0.375, relwidth=0.095, relheight=0.03)
       self.lbl_floor.place(relx=0.6, rely=0.375, relwidth=0.075, relheight=0.03)
       self.combo_room_type.place(relx=0.68, rely=0.410, relwidth=0.095, relheight=0.03)
       self.lbl_room.place(relx=0.6, rely=0.410, relwidth=0.075, relheight=0.03)
       self.txt_room_area.place(relx=0.68, rely=0.445, relwidth=0.045, relheight=0.03)
       self.lbl_room_area.place(relx=0.6, rely=0.445, relwidth=0.075, relheight=0.03)
       self.txt_room_qty.place(relx=0.68, rely=0.480, relwidth=0.045, relheight=0.03)
       self.lbl_room_qty.place(relx=0.6, rely=0.480, relwidth=0.075, relheight=0.03)
       self.lbl_room_place.place(relx=0.6, rely=0.515, relwidth=0.075, relheight=0.03)
       self.combo_room_place.place(relx=0.68, rely=0.515, relwidth=0.045, relheight=0.03)
       self.lbl_around_rooms.place(relx=0.6, rely=0.55, relwidth=0.075, relheight=0.03)
       self.combo_around_rooms.place(relx=0.68, rely=0.55, relwidth=0.045, relheight=0.03)
       self.room_list.place(relx=0.6, rely=0.14, relwidth=0.3675, relheight=0.185)
       self.scrollbar_room.place(relx=0.9574, rely=0.14, relwidth=0.01, relheight=0.185)
       self.lbl_room_list.place(relx=0.73, rely=0.1, relwidth=0.075, relheight=0.03)
       self.room_btn.place(relx=0.777, rely=0.375, relwidth=0.049, relheight=0.03)
       self.room_btn2.place(relx=0.777, rely=0.410, relwidth=0.049, relheight=0.03)
       self.room_btn3.place(relx=0.777, rely=0.445, relwidth=0.049, relheight=0.03)
       self.room_btn4.place(relx=0.777, rely=0.480, relwidth=0.049, relheight=0.03)
       self.lbl_insulation.place(relx=0.26, rely=0.225, relwidth=0.1, relheight=0.03)
       self.combo_insulation['values'] = ("NONE", "ALUCOBOND","MARBLE")
       self.lbl_insulation['text'] = "CLADDING"
       self.combo_insulation.place(relx=0.364, rely=0.225, relwidth=0.1, relheight=0.03)



   def clear_text_steel(self):
       self.combo_steeltype.place(relx=0.1904, rely=0.225, relwidth=0.075, relheight=0.03)
       self.combo_floor.place_forget()
       self.combo_floor.set('')
       self.lbl_floor.place_forget()
       self.combo_room_type.place_forget()
       self.combo_room_type.set('')
       self.lbl_room.place_forget()
       self.txt_room_area.place_forget()
       self.txt_room_area.delete(0,"end")
       self.lbl_room_area.place_forget()
       self.txt_room_qty.place_forget()
       self.txt_room_qty.delete(0,"end")
       self.lbl_room_qty.place_forget()
       self.combo_around_rooms.place_forget()
       self.combo_room_place.place_forget()
       self.lbl_room_place.place_forget()
       self.lbl_around_rooms.place_forget()
       self.room_list.place_forget()
       self.scrollbar_room.place_forget()
       self.lbl_room_list.place_forget()
       self.room_btn.place_forget()
       self.room_btn2.place_forget()
       self.room_btn3.place_forget()
       self.room_btn4.place_forget()
       self.lbl_found_wall.place_forget()
       self.combo_found_wall.place_forget()
       self.combo_found_wall.set('')
       self.lbl_found_beam.place_forget()
       self.combo_found_beam.place_forget()
       self.combo_found_beam.set('')
       self.combo_basement.set('')
       self.combo_soil.set('')
       #self.combo_thickness.set('')
       #self.combo_material.set('')
       self.combo_insulation.set('')
       self.combo_seperated_room.set('')
       self.mf_spin.set('')
       self.combo_insulation['values'] = ('CLADDING', 'SHEET')
       self.lbl_insulation['text'] = "INSULATION"
       self.combo_insulation.place_forget()
       self.lbl_insulation.place_forget()


   def steel_selection(self,event):
        if self.combo_structural_type.current() == 0:
            self.clear_text_steel()

        elif self.combo_structural_type.current() == 1:
            self.clear_text_rc()


        if self.combo_steeltype.current() == 0 or self.combo_steeltype.current() == 1 and self.combo_structural_type.current() == 0:
            self.lbl_insulation.place(relx=0.43, rely=0.3, relwidth=0.075, relheight=0.03)
            self.combo_insulation.place(relx=0.51, rely=0.3, relwidth=0.075, relheight=0.03)
            self.lbl_middle_floor.place(relx=0.458, rely=0.225, relwidth=0.085, relheight=0.03)
            self.mf_spin.place(relx=0.546, rely=0.225, relwidth=0.045, relheight=0.03)
            self.lbl_seperated_room.place(relx=0.28, rely=0.225, relwidth=0.095, relheight=0.03)
            self.combo_seperated_room.place(relx=0.38, rely=0.225, relwidth=0.0675, relheight=0.03)

   def foundation_selection(self,event):
       self.lbl_found_beam.place(relx=0.26, rely=0.3, relwidth=0.1, relheight=0.03)
       self.combo_found_beam.place(relx=0.364, rely=0.3, relwidth=0.05, relheight=0.03)
       self.lbl_found_wall.place(relx=0.26, rely=0.35, relwidth=0.1, relheight=0.03)
       self.combo_found_wall.place(relx=0.364, rely=0.35, relwidth=0.05, relheight=0.03)
       if self.combo_soil.current()==0:
           self.combo_found_beam['values'] = ('TWO_WAY', 'NO_BEAM')

       elif self.combo_soil.current() == 1:
           self.combo_found_beam['values'] = ('ONE_WAY','TWO_WAY','NO_BEAM')

       elif self.combo_soil.current() == 2 or self.combo_soil.current() == 3:
           self.combo_found_beam['values'] = ('STRAP_BEAM','NO_BEAM')
       else:
           pass

   def seperated_room_selection(self,event):
       if self.combo_seperated_room.current() == 0:
           self.combo_floor.place(relx=0.68, rely=0.375, relwidth=0.095, relheight=0.03)
           self.lbl_floor.place(relx=0.6, rely=0.375, relwidth=0.075, relheight=0.03)
           self.combo_room_type.place(relx=0.68, rely=0.410, relwidth=0.095, relheight=0.03)
           self.lbl_room.place(relx=0.6, rely=0.410, relwidth=0.075, relheight=0.03)
           self.txt_room_area.place(relx=0.68, rely=0.445, relwidth=0.045, relheight=0.03)
           self.lbl_room_area.place(relx=0.6, rely=0.445, relwidth=0.075, relheight=0.03)
           self.txt_room_qty.place(relx=0.68, rely=0.480, relwidth=0.045, relheight=0.03)
           self.lbl_room_qty.place(relx=0.6, rely=0.480, relwidth=0.075, relheight=0.03)
           self.lbl_room_place.place(relx=0.6, rely=0.515, relwidth=0.075, relheight=0.03)
           self.combo_room_place.place(relx=0.68, rely=0.515, relwidth=0.045, relheight=0.03)
           self.lbl_around_rooms.place(relx=0.6, rely=0.55, relwidth=0.075, relheight=0.03)
           self.combo_around_rooms.place(relx=0.68, rely=0.55, relwidth=0.045, relheight=0.03)
           self.room_list.place(relx=0.6, rely=0.14, relwidth=0.3675, relheight=0.185)
           self.scrollbar_room.place(relx=0.9574, rely=0.14, relwidth=0.01, relheight=0.185)
           self.lbl_room_list.place(relx=0.73, rely=0.1, relwidth=0.075, relheight=0.03)
           self.room_btn.place(relx=0.777, rely=0.375, relwidth=0.047, relheight=0.03)
           self.room_btn2.place(relx=0.777, rely=0.410, relwidth=0.047, relheight=0.03)
           self.room_btn3.place(relx=0.777, rely=0.445, relwidth=0.047, relheight=0.03)
           self.room_btn4.place(relx=0.777, rely=0.480, relwidth=0.049, relheight=0.03)
       elif self.combo_seperated_room.current() == 1:
           self.combo_floor.place_forget()
           self.lbl_floor.place_forget()
           self.combo_room_type.place_forget()
           self.lbl_room.place_forget()
           self.txt_room_area.place_forget()
           self.lbl_room_area.place_forget()
           self.txt_room_qty.place_forget()
           self.lbl_room_qty.place_forget()
           self.lbl_room_place.place_forget()
           self.combo_room_place.place_forget()
           self.lbl_around_rooms.place_forget()
           self.combo_around_rooms.place_forget()
           self.room_list.place_forget()
           self.scrollbar_room.place_forget()
           self.lbl_room_list.place_forget()
           self.room_btn.place_forget()
           self.room_btn2.place_forget()
           self.room_btn3.place_forget()
           self.room_btn4.place_forget()

   def basement_check(self,foundation_depth,strfill_depth,basement_wall_height):
       if self.combo_basement.current()==0:
           exc_depth = basement_wall_height + foundation_depth + 0.1 + 0.05 + strfill_depth + 0.1
       else:
           exc_depth = foundation_depth + 0.1 + 0.05 + strfill_depth + 0.1
       return round(exc_depth,2)

   def excavationCheck(self,exc_depth,strfill_depth,foundation_depth,basement,basement_height):
       minimum_excavation_depth = foundation_depth + strfill_depth + 0.1 + 0.05
       check = exc_depth - strfill_depth - foundation_depth - 0.1 - 0.05
       if basement == "YES":
           check = check - basement_height
           minimum_excavation_depth = minimum_excavation_depth + basement_height
       if check >= 0:
           print(f"Check = {check} so excavation depth is valid!")
       elif check < 0:
           self.speech.excavationError()
           messagebox.showerror("ERROR","Excavation depth should be higher than {}".format(round(minimum_excavation_depth,2)),icon="warning")
           return


   def steel_check(self):
       if self.combo_steeltype.current()==0:
           steel_weight=16
       if self.combo_steeltype.current()==1:
           steel_weight=20
       else:
           steel_weight = 16
       return steel_weight

   def Execute(self):
        start_time=time.time()
        pricesheet.table_output()
        for row in db.fetch():
            print("-------"+(row[1])+"-------")
            if row[4]=="RC":
                self.Rc_Execute(row=row)
                try:
                    db.alter_add_column(row[1])
                except sqlite3.OperationalError:
                    self.speech.duplicated_names()
                    messagebox.showerror("-- ERROR --", "Please change duplicated building names!", icon="warning")
                    return
            elif row[4]=="STEEL":
                self.Steel_Execute(row=row)
                try:
                    db.alter_add_column(row[1])
                except sqlite3.OperationalError:
                    self.speech.duplicated_names()
                    messagebox.showerror("-- ERROR --", "Please change duplicated building names!", icon="warning")
                    return
            else:
                pass

        steel_works=[2.4,2.7,3.2,3.1,3.5,2.11,3.3,3.7,4.1,5.1,3.6,7.1,3.11,6.1,6.2,6.3,17.1,17.2,17.4,8.1,8.3,8.6,8.4
                    ,21.5,19.4,19.2,10.3,10.4,11.1,11.2,11.3,11.4,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,13.1,13.3,14.1,14.2
                    ,14.4,14.5,14.6,16.1,5.2,9.1,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9,20.11,3.9,9.3,9.2]

        for steel in db.fetch_results_steel():
            results=list(steel[2:65])
            for i in range(0,len(steel_works)):
                db.update_works(steel[1],results[i],steel_works[i])

        rc_works=[2.4,2.7,3.2,3.1,3.5,3.3,2.11,3.4,3.6,3.7,4.1,5.1,5.2,19.4,19.2,17.1,17.2,17.4,10.3,10.4,11.1,11.2,11.3,11.4
                ,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,13.1,13.3,14.1,14.2,14.4,14.5,14.6,16.1,21.5,14.8,14.7,10.2,13.2,14.3
                ,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9#DOORS
                ,3.12,21.17,20.11,3.9,21.8,8.6]

        for rc in db.fetch_results_rc():
            results=list(rc[2:63])
            for i in range(0,len(rc_works)):
                db.update_works(rc[1],results[i],rc_works[i])

        print("--- %s seconds ---" % (time.time() - start_time))
        self.speech.progress_completed()
        messagebox.showinfo("COMPLETED", "PROCESS IS COMPLETED!", icon="info")
        pricesheet.print(self.txt_project_name.get())
        pricesheet.open_output()


   def Steel_Execute(self,row):
            steel = steel_bldg()
            steel.name=row[1]
            steel.width = row[13]
            steel.length = row[14]
            steel.storey_height=row[3]
            steel.storey=row[2]
            steel.structural_type = row[4]
            steel.steel_type = row[5]
            steel.insulation = row[6]
            steel.seperated_room = row[7]
            steel.middle_floor = row[8]
            steel.basement = row[12]
            steel.soil_property = row[9]
            steel.beam_connection = row[10]
            steel.ground_wall = row[11]
            steel.depth_lc=0.1
            exc_depth = row[15]
            strfill_depth = row[16]
            foundation_depth = row[17]
            foundation_d1 = row[18]
            foundation_d2 = row[19]
            tie_beam_d1=row[20]
            tie_beam_d2=row[21]
            steel_pedestal_d1 = row[22]
            steel_pedestal_d2 = row[23]
            steel_pedestal_depth=row[24]
            steel_pedestal_rangex=row[25]
            steel_pedestal_rangey=row[26]
            basement_height = row[31]
            basement_thickness = row[32]
            ground_wall_height = row[33]
            ground_wall_thickness = row[34]
            unit_weight = row[35]
            grouting_depth = row[36]
            concrete_slab = row[41]
            ground_slab = row[42]
            #WORKS
            excavation = steel.excavation(exc_depth)
            fill = steel.strfill(strfill_depth)
            foundation_work = steel.foundation(foundation_depth,steel_pedestal_rangex,steel_pedestal_rangey,foundation_d1,foundation_d2,tie_beam_d1,tie_beam_d2,ground_wall_thickness,ground_wall_height)
            basement_work = steel.basement_wall(basement_height,basement_thickness,ground_wall_thickness,ground_wall_height,steel_pedestal_rangex,steel_pedestal_rangey,steel_pedestal_d2,steel_pedestal_d1,foundation_d1)
            pedestal_work = steel.steel_pedestal(steel_pedestal_rangex, steel_pedestal_rangey, steel_pedestal_d1, steel_pedestal_d2, steel_pedestal_depth)

            db.insert_results_steel(steel.name,
                                    excavation,
                                    fill,
                                    foundation_work,
                                    steel.lean_concrete(0.1),
                                    basement_work,
                                    steel.backfill(),
                                    pedestal_work,
                                    steel.ground_slab(ground_slab,steel_pedestal_rangex,steel_pedestal_rangey,steel_pedestal_d2,steel_pedestal_d1),
                                    steel.formwork(0),
                                    steel.rebar(0),
                                    steel.steel_concrete_slab(concrete_slab),
                                    steel.steel_weight(unit_weight),
                                    steel.grouting(grouting_depth),
                                    steel.embedded_steel(),
                                    steel.anchorbolt_m24(),
                                    steel.anchorbolt_m30(),
                                    0, #insulation sika
                                    steel.insulation_membrane(0),
                                    steel.pe_sheet(),
                                    steel.handrail(),
                                    steel.steel_grating(),
                                    steel.steel_ladder(),
                                    steel.chequered_plate(),
                                    steel.water_stop(),
                                    steel.rainwater_gutter(),
                                    steel.rainwater_pipe(),
                                    self.room_execute(steel.name)[0],self.room_execute(steel.name)[1],self.room_execute(steel.name)[2],self.room_execute(steel.name)[3],self.room_execute(steel.name)[4],self.room_execute(steel.name)[5],self.room_execute(steel.name)[6],self.room_execute(steel.name)[7],self.room_execute(steel.name)[8],self.room_execute(steel.name)[9],self.room_execute(steel.name)[10],self.room_execute(steel.name)[11],self.room_execute(steel.name)[12],self.room_execute(steel.name)[13],self.room_execute(steel.name)[14],self.room_execute(steel.name)[15],self.room_execute(steel.name)[16],self.room_execute(steel.name)[17],self.room_execute(steel.name)[18],self.room_execute(steel.name)[19],self.room_execute(steel.name)[20],
                                    steel.pvc_window(),
                                    steel.wire_mesh(),
                                    steel.single_sheet_roof_cladding(),
                                    self.room_execute(steel.name)[21],self.room_execute(steel.name)[22],self.room_execute(steel.name)[23],(self.room_execute(steel.name)[24] + steel.sliding_steel_door_building(steel.structural_type)),self.room_execute(steel.name)[25],self.room_execute(steel.name)[26],self.room_execute(steel.name)[27],self.room_execute(steel.name)[28],self.room_execute(steel.name)[29],
                                    steel.catch_basin(),
                                    steel.concrete_for_pavement(),
                                    steel.insulated_wall_cladding(),
                                    steel.double_sheet_roof_cladding())


   def Rc_Execute(self,row):
            rc = rc_bldg()
            rc.name=row[1]
            rc.width = row[13]
            rc.length = row[14]
            rc.structural_type = row[4]
            rc.insulation = row[6]
            rc.basement=row[12]
            basement_height = row[31]
            basement_thickness = row[32]
            ground_wall_height = row[33]
            ground_wall_thickness = row[34]
            rc.soil_property = row[9]
            rc.beam_connection = row[10]
            rc.ground_wall = row[11]
            rc.storey_height=row[3]
            rc.storey=row[2]
            exc_depth = row[15]
            strfill_depth = row[16]
            foundation_depth = row[17]
            foundation_d1 = row[18]
            foundation_d2 = row[19]
            tie_beam_d1=row[20]
            tie_beam_d2=row[21]
            rc_column_width = row[27]
            rc_column_length = row[28]
            rc_column_rangex = row[29]
            rc_column_rangey = row[30]
            rc_beam_width = row[37]
            rc_beam_length = row[38]
            rc_secondary_beam_d1 = row[39]
            rc_secondary_beam_d2 = row[40]
            concrete_slab = row[41]
            ground_slab = row[42]
            paraphet_height = row[43]
            paraphet_thickness = row[44]
            rc.depth_lc = 0.1
            db.insert_results_rc(rc.name,
                                 rc.excavation(exc_depth),
                                 rc.strfill(strfill_depth),
                                 rc.foundation(foundation_depth,rc_column_rangex,rc_column_rangey,foundation_d1,foundation_d2,tie_beam_d1,tie_beam_d2,ground_wall_thickness,ground_wall_height),
                                 rc.lean_concrete(0.1),
                                 rc.basement_wall(basement_height,basement_thickness,ground_wall_thickness,ground_wall_height,rc_column_rangex,rc_column_rangey,rc_column_width,rc_column_length,foundation_d1),
                                 rc.rc_column(rc_column_length,rc_column_width,rc_column_rangex,rc_column_rangey),
                                 rc.backfill(),
                                 rc.rc_beam(rc_beam_width,rc_beam_length,rc_secondary_beam_d1,rc_secondary_beam_d2),
                                 rc.concrete_slab(concrete_slab,paraphet_height,paraphet_thickness),
                                 rc.ground_slab(ground_slab,rc_column_rangex,rc_column_rangey,rc_column_width,rc_column_length),
                                 rc.formwork(0),
                                 rc.rebar(0),
                                 rc.wire_mesh(),
                                 rc.rainwater_gutter(),
                                 rc.rainwater_pipe(),
                                 0, #insulation sika
                                 rc.insulation_membrane(0),
                                 rc.pe_sheet(),
                                 self.room_execute(rc.name)[0],self.room_execute(rc.name)[1],self.room_execute(rc.name)[2],self.room_execute(rc.name)[3],self.room_execute(rc.name)[4],self.room_execute(rc.name)[5],self.room_execute(rc.name)[6],self.room_execute(rc.name)[7],self.room_execute(rc.name)[8],self.room_execute(rc.name)[9],self.room_execute(rc.name)[10],self.room_execute(rc.name)[11],self.room_execute(rc.name)[12],self.room_execute(rc.name)[13],self.room_execute(rc.name)[14],self.room_execute(rc.name)[15],self.room_execute(rc.name)[16],self.room_execute(rc.name)[17],self.room_execute(rc.name)[18],self.room_execute(rc.name)[19],self.room_execute(rc.name)[20],
                                 rc.pvc_window(),
                                 rc.water_stop(),
                                 rc.marble_cladding(),
                                 rc.alucobond_cladding(),
                                 rc.brick_wall200mm(),
                                 rc.exterior_wall_plaster(),
                                 rc.exterior_wall_paint(),
                                 self.room_execute(rc.name)[21],self.room_execute(rc.name)[22],self.room_execute(rc.name)[23],self.room_execute(rc.name)[24],(self.room_execute(rc.name)[25] + rc.double_wing_aliminium_door_entrance_building(rc.structural_type)),self.room_execute(rc.name)[26],self.room_execute(rc.name)[27],self.room_execute(rc.name)[28],self.room_execute(rc.name)[29],self.room_execute(rc.name)[30],
                                 rc.concrete_stairs(),
                                 rc.catch_basin(),
                                 rc.concrete_for_pavement(),
                                 rc.joint_cutting(rc_column_rangex,rc_column_rangey),
                                 rc.steel_ladder())

   def room_execute(self,building_name):
       inside_brick_wall = 0
       gypsum_part_wall = 0
       aliminum_suspended_ceiling = 0
       acoustical_ceiling = 0
       gypsum_suspended_ceiling = 0
       rockwool_suspended_ceiling = 0
       non_slip_ceramic_tile = 0
       glazed_ceramic_tile = 0
       glazed_ceramic_skirting = 0
       epoxy_floor = 0
       resistant_floor = 0
       acid_tile = 0
       raised_floor = 0
       laminated_parquet = 0
       int_plaster = 0
       ceiling_plaster = 0
       ceramic_wall_tile = 0
       int_paint = 0
       acid_resistant_int_paint = 0
       ceiling_paint = 0
       epoxy_wall_paint = 0
       steel_door1 = 0
       steel_door2 = 0
       roller_shutter = 0
       sliding_steel_door = 0
       double_wing_aliminium_door = 0
       compacted_laminate_door = 0
       wooden_internal_door = 0
       aliminum_door = 0
       aliminum_double_win_door = 0
       screed = 0
       for room in db.fetch_rooms_execute(building_name):
           inside_brick_wall +=  room[5]
           gypsum_part_wall += room[6]
           aliminum_suspended_ceiling += room[7]
           acoustical_ceiling += room[8]
           gypsum_suspended_ceiling += room[9]
           rockwool_suspended_ceiling += room[10]
           non_slip_ceramic_tile += room[11]
           glazed_ceramic_tile += room[12]
           glazed_ceramic_skirting += room[13]
           epoxy_floor += room[14]
           resistant_floor += room[15]
           acid_tile += room[16]
           raised_floor += room[17]
           laminated_parquet += room[18]
           int_plaster += room[19]
           ceiling_plaster += room[20]
           ceramic_wall_tile += room[21]
           int_paint += room[22]
           acid_resistant_int_paint += room[23]
           ceiling_paint += room[24]
           epoxy_wall_paint += room[25]
           steel_door1 += room[26]
           steel_door2 += room[27]
           roller_shutter += room[28]
           sliding_steel_door += room[29]
           double_wing_aliminium_door += room[30]
           compacted_laminate_door += room[31]
           wooden_internal_door += room[32]
           aliminum_door += room[33]
           aliminum_double_win_door += room[34]
           screed += room[35]

       room_works = [inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint, steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed]

       return room_works