import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from openpyxl import *
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from xlsxwriter.workbook import Workbook
from dbase import Database
from output_to_price_sheet import pricesheet
from foundation_calculator import  *
from pit_calculator import *
import sqlite3

db = Database('Database/foundation.db')
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

class found_pic(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)
        self.param_type = None

    def open_image(self):
        self.image = Image.open("img/{}.png".format(self.param_type))
        self.img_copy = self.image.copy()

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
        self.title("CIVIL FOUNDATION TOOL")
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (self.w, self.h))
        self.state('zoomed')
        #self.attributes("-fullscreen", True)
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
                        background="gray", foreground="black", relief="groove", font=(None, 7))
        style.configure("Custom.Treeview", highlightthickness=0, bd=0, font=('Calibri', 8))
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])

        style_button = ttk.Style(self)
        style_button.configure('W.TButton', font=('calibri', 10, 'bold'),foreground='black')



        #FRAME 1 WIDGETS

        #Variables
        self.plant_type = StringVar()
        self.tank_type = StringVar()
        self.selected_hz = IntVar()
        self.gtno = IntVar()
        self.gtindoor = IntVar()
        self.bypass = IntVar()
        self.brand_type = StringVar()
        self.chemical = IntVar()
        self.dykewall_inc = IntVar()

        self.frame1 = Frame(self)
        self.lbl_gt_type = ttk.Label(self.frame1, text='GT TYPE', font=("Pickwick", 8, "bold"))
        self.combo_gt_type = ttk.Combobox(self.frame1, width=27, textvariable=self.plant_type, state='readonly')
        self.combo_gt_band = ttk.Combobox(self.frame1, width=27, textvariable=self.brand_type, state='readonly')
        combo_gt_type_values = [row[1] for row in db.fetch_selection_gt()]
        self.combo_gt_type['values'] =(combo_gt_type_values)
        self.combo_gt_type.current()
        self.rad_50_hz = ttk.Radiobutton(self.frame1, text='50 Hz', variable=self.selected_hz, value=1)
        self.rad_60_hz = ttk.Radiobutton(self.frame1, text='60 Hz', variable=self.selected_hz, value=2)
        self.lbl_gtno = ttk.Label(self.frame1, text='GT NOs',font=("Pickwick", 8, "bold"))
        self.lbl_skid_list = ttk.Label(self.frame1, text='Auxiliary List', font=("Pickwick", 8, "bold"))
        self.lbl_skid_used = ttk.Label(self.frame1, text='Auxiliaries Added', font=("Pickwick", 8, "bold"))
        self.combo_gtno = ttk.Combobox(self.frame1, width=27, textvariable=self.gtno, state='readonly')
        self.combo_gtno['values'] =(1,2,3,4,5,6,7,8,9,10)
        self.combo_gtno.current()
        self.gtindoor_check = ttk.Checkbutton(self.frame1, text='GT Indoor', variable=self.gtindoor, command = self.gtIndoorCheck,onvalue=1, offvalue=0)
        self.bypass_check = ttk.Checkbutton(self.frame1, text='By-Pass Stack', variable=self.bypass, command = self.bypassAdd,onvalue=1,offvalue=0)
        self.aux_list = Listbox(self.frame1)
        self.aux_list2 = Listbox(self.frame1)
        self.add_aux_button = ttk.Button(self.frame1, text="ADD", command=self.add_aux, cursor="hand2",style = 'W.TButton')
        self.remove_aux_button = ttk.Button(self.frame1, text="REMOVE", command=self.remove_aux, cursor="hand2",style = 'W.TButton')
        self.run_button_image = tk.PhotoImage(file='img/run.png').subsample(3, 3)
        self.delete_button_image = tk.PhotoImage(file='img/delete.png').subsample(3, 3)
        self.run_btn = ttk.Button(self, text="RUN", command=self.execute, cursor="hand2",style = 'W.TButton', image=self.run_button_image,compound = LEFT)
        self.delete_btn = ttk.Button(self, text="DELETE", command=self.removeFoundation, cursor="hand2",style = 'W.TButton', image=self.delete_button_image,compound = LEFT).place(relx=0.11, rely=0.9, relwidth=0.09, relheight=0.05)
        self.delete_all_btn = ttk.Button(self, text="DELETE ALL", command=self.removeAllFoundations, cursor="hand2",style = 'W.TButton', image=self.delete_button_image,compound = LEFT).place(relx=0.21, rely=0.9, relwidth=0.09, relheight=0.05)

        self.GT_foundation_btn = ttk.Button(self, text="GT FOUNDATION", command = self.gtFoundation,cursor="hand2", style='W.TButton')
        self.single_footing_btn = ttk.Button(self, text="SINGLE FOOTING", command = self.singleFooting,cursor="hand2", style='W.TButton')
        self.combined_footing_btn = ttk.Button(self, text="COMBINED FOOTING", command = self.combinedFooting,cursor="hand2", style='W.TButton')
        self.mat_foundation_btn = ttk.Button(self, text="MAT FOUNDATION", command = self.matFoundation,cursor="hand2", style='W.TButton')
        self.tank_foundation_btn = ttk.Button(self, text="TANK&DYKE WALL", command = self.tankFoundation,cursor="hand2", style='W.TButton').place(relx=0.41, rely=0.02, relwidth=0.09, relheight=0.03)
        self.pit_calculator_btn = ttk.Button(self, text="PIT CALCULATOR", command = self.pitCalculator,cursor="hand2", style='W.TButton').place(relx=0.51, rely=0.02, relwidth=0.09, relheight=0.03)

        self.frame_sf = Frame(self)
        self.frame2 = Frame(self)
        self.frame_dw = Frame(self)
        self.bypass_button = ttk.Button(self, cursor="hand2",style='W.TButton')

        columns = ("#1", "#2", "#3", "#4","5","#6", "#7", "#8", "#9","10","#11", "#12", "#13", "#14","15","#16", "#17", "#18", "#19","20","21","22","23")
        self.tree_foundations = ttk.Treeview(self,show="headings", height="5", columns=columns, style="Custom.Treeview")
        self.tree_foundations.bind("<<TreeviewSelect>>", self.selectFoundation)
        self.tree_foundations.heading('#1', text='Index', anchor='center')
        self.tree_foundations.column('#1', width=0, anchor='center', stretch=False)
        self.tree_foundations.heading('#2', text='Type', anchor='center')
        self.tree_foundations.column('#2', width=40, anchor='center', stretch=True)
        self.tree_foundations.heading('#3', text='Item', anchor='center')
        self.tree_foundations.column('#3', width=40, anchor='center', stretch=True)
        self.tree_foundations.heading('#4', text='Concrete_Foundation', anchor='center')
        self.tree_foundations.column('#4', width=40, anchor='center', stretch=True)
        self.tree_foundations.heading('#5', text='LeanConcrete', anchor='center')
        self.tree_foundations.column('#5', width=45, anchor='center', stretch=True)
        self.tree_foundations.heading('#6', text='Formwork', anchor='center')
        self.tree_foundations.column('#6', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#7', text='Rebar', anchor='center')
        self.tree_foundations.column('#7', width=30, anchor='center', stretch=True)
        self.tree_foundations.heading('#8', text='ConcreteProtection', anchor='center')
        self.tree_foundations.column('#8', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#9', text='PeSheet', anchor='center')
        self.tree_foundations.column('#9', width=30, anchor='center', stretch=True)
        self.tree_foundations.heading('#10', text='Excavation', anchor='center')
        self.tree_foundations.column('#10', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#11', text='StructuralFill', anchor='center')
        self.tree_foundations.column('#11', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#12', text='Backfill', anchor='center')
        self.tree_foundations.column('#12', width=40, anchor='center', stretch=True)
        self.tree_foundations.heading('#13', text='Grout', anchor='center')
        self.tree_foundations.column('#13', width=30, anchor='center', stretch=True)
        self.tree_foundations.heading('#14', text='Screed', anchor='center')
        self.tree_foundations.column('#14', width=40, anchor='center', stretch=True)
        self.tree_foundations.heading('#15', text='EmbededPlate', anchor='center')
        self.tree_foundations.column('#15', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#16', text='WireMesh', anchor='center')
        self.tree_foundations.column('#16', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#17', text='Anchor24', anchor='center')
        self.tree_foundations.column('#17', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#18', text='Anchor30', anchor='center')
        self.tree_foundations.column('#18', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#19', text='Anchor36', anchor='center')
        self.tree_foundations.column('#19', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#20', text='Anchor42', anchor='center')
        self.tree_foundations.column('#20', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#21', text='StructuralSteel', anchor='center')
        self.tree_foundations.column('#21', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#22', text='JointIsolation', anchor='center')
        self.tree_foundations.column('#22', width=47, anchor='center', stretch=True)
        self.tree_foundations.heading('#23', text='WaterStopper', anchor='center')
        self.tree_foundations.column('#23', width=47, anchor='center', stretch=True)
        self.tree_foundations.place(relx=0, rely=0.6, relwidth=0.99, relheight=0.295)
        self.populate_list_gt()

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.scrollbar.place(relx=0.99, rely=0.6, relwidth=0.01, relheight=0.295)
        self.scrollbar.configure(command=self.tree_foundations.yview)

        self.GT_foundation_btn.place(relx=0.01, rely=0.02, relwidth=0.09, relheight=0.03)
        self.single_footing_btn.place(relx=0.11, rely=0.02, relwidth=0.09, relheight=0.03)
        self.combined_footing_btn.place(relx=0.21, rely=0.02, relwidth=0.09, relheight=0.03)
        self.mat_foundation_btn.place(relx=0.31, rely=0.02, relwidth=0.09, relheight=0.03)
        self.run_btn.place(relx=0.01, rely=0.9, relwidth=0.09, relheight=0.05)

       #Scrollbar
        self.scrollbar_aux_list = Scrollbar(self.frame1)
        self.scrollbar_aux_list2 = Scrollbar(self.frame1)
        self.scrollbar_aux_list.configure(command=self.aux_list.yview)
        self.scrollbar_aux_list.place(relx=0.39, rely=0.45, relwidth=0.02, relheight=0.54)
        self.scrollbar_aux_list2.configure(command=self.aux_list2.yview)
        self.scrollbar_aux_list2.place(relx=0.62, rely=0.45, relwidth=0.02, relheight=0.54)

   def selectFoundation(self,event):
        try:
            global selected_item
            selected_item = self.tree_foundations.item(self.tree_foundations.selection())['values']
            types = {"SINGLE FOOTING": "single_footing",
                     "COMBINED FOOTING": "combined_footing",
                     "MAT FOUNDATION": "mat_foundation",
                     "PIT": "pit_calculator",
                     "WALL FOUNDATION1":"dyke_wall",
                     "CYLINDER TANK":"tank_foundation",
                     "OCTAGON TANK":"tank_foundation",
                     "OCTAGON(SQUARE_BASE) TANK":"tank_foundation",
                     "HEXAGON TANK":"tank_foundation",
                     "HEXAGON(SQUARE_BASE) TANK":"tank_foundation",
                     }
            functions = {"SINGLE FOOTING": self.singleFooting,
                     "COMBINED FOOTING": self.combinedFooting,
                     "MAT FOUNDATION": self.matFoundation,
                     "PIT": self.pitCalculator,
                     "WALL FOUNDATION1":self.dykeWall,
                     "CYLINDER TANK":self.tankFoundation,
                     "OCTAGON TANK":self.tankFoundation,
                     "OCTAGON(SQUARE_BASE) TANK":self.tankFoundation,
                     "HEXAGON TANK":self.tankFoundation,
                     "HEXAGON(SQUARE_BASE) TANK":self.tankFoundation,
                         }
            print(f"Selected item: {selected_item}")
            table = types.get(selected_item[1])
            print(table)
            global selected_ind_found
            try:
                selected_ind_found = [row for row in db.fetchIndFound(table,selected_item[2])]
            except sqlite3.OperationalError:
                pass
            print(selected_ind_found)
            functions.get(selected_item[1])()
        except IndexError:
            print("Index Error")
        except NameError:
            print("Name Error")
        except TypeError:
            print("Type Error")

   def removeFoundation(self):
       print(selected_item[2])
       db.removeFoundation(selected_item[2])
       db.removeIndFound(selected_item[2],selected_item[1])
       self.populate_list_gt()

   def removeAllFoundations(self):
       if messagebox.askokcancel("OK", "Do you want to delete all?"):
           db.delFromResults()
           db.removeAllIndFound(selected_item[1])
           self.populate_list_gt()

   def populate_list_gt(self):
        self.tree_foundations.delete(*self.tree_foundations.get_children())
        for row in db.fetchResults():
            self.tree_foundations.insert("",row[0], values=row)

   def add_aux(self):
       if len(self.aux_list.curselection()) != 0:
           x = self.aux_list.get(self.aux_list.curselection())
           self.aux_list2.insert(END, x)
       print("aux added")

   def remove_aux(self):
       if len(self.aux_list2.curselection()) != 0:
           self.aux_list2.delete(self.aux_list2.curselection())
       print("aux removed")

   def addByPass(self):
       db.delFromStack()
       if self.bypass.get() == 1:
           STACK = Stack()
           STACK.depth_exc = self.zero_check(self.exc_depth.get())
           STACK.depth_fill = self.zero_check(self.strfill.get())
           STACK.depth_found = self.zero_check(self.foundation_depth.get())
           STACK.width = self.zero_check(self.foundation_d1.get())
           STACK.length = self.zero_check(self.foundation_d2.get())
           STACK.steel_weight = self.zero_check(self.steel_weight.get())
           STACK.grout_depth1 = self.zero_check(self.grouting_depth1.get())
           STACK.grout_depth2 = self.zero_check(self.grouting_depth2.get())
           STACK.p1_width = self.zero_check(self.p1_width.get())
           STACK.p1_length = self.zero_check(self.p1_length.get())
           STACK.p1_depth = self.zero_check(self.p1_depth.get())
           STACK.p1_qty = self.zero_check(self.p1_qty.get())
           STACK.p2_width = self.zero_check(self.p2_width.get())
           STACK.p2_length = self.zero_check(self.p2_length.get())
           STACK.p2_depth = self.zero_check(self.p2_depth.get())
           STACK.p2_qty = self.zero_check(self.p2_qty.get())

           db.insertStack(STACK.depth_exc,
                          STACK.depth_fill,
                          STACK.depth_found,
                          STACK.width,
                          STACK.length,
                          STACK.steel_weight,
                          STACK.grout_depth1,
                          STACK.grout_depth2,
                          STACK.p1_width,
                          STACK.p1_length,
                          STACK.p1_depth,
                          STACK.p1_qty,
                          STACK.p2_width,
                          STACK.p2_length,
                          STACK.p2_depth,
                          STACK.p2_qty)
           """
           db.insertResultGTG("BY-PASS STACK",
                              STACK.concreteFoundation(),
                              STACK.lean_concrete(),
                              STACK.formwork(),
                              STACK.rebar(),
                              STACK.insulationSika(),
                              STACK.pe_sheet(),
                              STACK.excavation(),
                              STACK.structuralfill(),
                              STACK.backfill(),
                              STACK.grout(),
                              STACK.screed(),
                              STACK.embeddedPlate(),
                              0,
                              STACK.anchor24(),
                              STACK.anchor30(),
                              STACK.anchor36(),
                              STACK.anchor42(),
                              STACK.structuralSteel(),
                              )
                              """
           messagebox.showinfo("INFO", "BY-PASS STACK ADDED!", icon="info")

   def addSingleFooting(self):
       width = self.zero_check(self.foundation_d1.get())
       length = self.zero_check(self.foundation_d2.get())
       pedestal_length = self.zero_check(self.p1_length.get())
       pedestal_width = self.zero_check(self.p1_width.get())
       foundation_depth = self.zero_check(self.foundation_depth.get())
       pedestal_height = self.zero_check(self.p1_depth.get())
       fill = self.zero_check(self.strfill.get())
       es = 0
       steel = 0
       exc_depth = self.zero_check(self.exc_depth.get())
       grout_depth = self.zero_check(self.grouting_depth1.get())
       quantity = self.zero_check(self.quantity.get())
       anchor_type = self.zero_check(self.anchor_type.get())
       anchor_qty = self.zero_check(self.anchor_qty.get())
       sf = Singlefooting(width,length,pedestal_length,pedestal_width,foundation_depth,pedestal_height,fill,anchor_type,anchor_qty,es,steel,exc_depth,grout_depth)

       concrete_foundation = round(sf.strconcrete(),2)
       lean_concrete = round(sf.leanconc(),2)
       formwork = round(sf.formwork(),2)
       rebar = round(sf.rebar(),2)
       concrete_protection = round(sf.concreteprot(),2)
       pe_sheet = round(sf.polyethylenesheet(),2)
       excavation = round(sf.excavation(),2)
       structural_fill = round(sf.strfill(),2)
       backfill = round(sf.backfill(),2)
       grout = round(sf.grout(),2)
       water_stopper = round(sf.waterStopper(),2)
       joint_isolation = round(sf.jointIsolation(),2)
       screed = 0
       embedded_steel = 0
       wire_mesh = 0
       anchor_24 = sf.anchor().get("M24")
       anchor_30 = sf.anchor().get("M30")
       anchor_36 = sf.anchor().get("M36")
       anchor_42 = sf.anchor().get("M42")
       structural_steel = 0
       names = [row[2] for row in db.fetchResults()]
       name = self.found_name.get()
       for version in range(1, 150):
           if f"{name}" not in names:
               print("Name First Time")
               break
           elif f"{name}{version}" in names:
               print("Name Exist")
           else:
               print("Name Unique")
               name = f"{name}{version}"
               break
       db.insertResultGTG("SINGLE FOOTING",
                          name,
                          concrete_foundation * quantity,
                          lean_concrete * quantity,
                          formwork * quantity,
                          rebar * quantity,
                          concrete_protection * quantity,
                          pe_sheet * quantity,
                          excavation * quantity,
                          structural_fill * quantity,
                          backfill * quantity,
                          grout * quantity,
                          screed * quantity,
                          embedded_steel * quantity,
                          wire_mesh * quantity,
                          anchor_24 * quantity,
                          anchor_30 * quantity,
                          anchor_36 * quantity,
                          anchor_42 * quantity,
                          structural_steel * quantity,
                          joint_isolation * quantity,
                          water_stopper * quantity,
                          )

       db.insertSF(name,
                   exc_depth,
                   fill,
                   foundation_depth,
                   width,
                   length,
                   anchor_type,
                   anchor_qty,
                   grout_depth,
                   pedestal_width,
                   pedestal_length,
                   pedestal_height,
                   quantity)

       self.populate_list_gt()


       
   def addCombinedFooting(self):
       width = self.zero_check(self.foundation_d1.get())
       length = self.zero_check(self.foundation_d2.get())
       pedestal_length = self.zero_check(self.p1_length.get())
       pedestal_width = self.zero_check(self.p1_width.get())
       pedestal_qty = self.zero_check(self.p1_qty.get())
       foundation_depth = self.zero_check(self.foundation_depth.get())
       pedestal_height = self.zero_check(self.p1_depth.get())
       fill = self.zero_check(self.strfill.get())
       pedestal = pedestal_qty
       es = 0.001
       steel = 0
       exc_depth = self.zero_check(self.exc_depth.get())
       grout_depth = self.zero_check(self.grouting_depth1.get())
       quantity = self.zero_check(self.quantity.get())
       anchor_type = self.zero_check(self.anchor_type.get())
       anchor_qty = self.zero_check(self.anchor_qty.get())
       cf = Combinedfooting(width,length,pedestal_length,pedestal_width,foundation_depth,pedestal_height,fill,anchor_type,anchor_qty,pedestal,es,steel,exc_depth,grout_depth)

       concrete_foundation = round(cf.strconcrete(),2)
       lean_concrete = round(cf.leanconc(),2)
       formwork = round(cf.formwork(),2)
       rebar = round(cf.rebar(),2)
       concrete_protection = round(cf.concreteprot(),2)
       pe_sheet = round(cf.polyethylenesheet(),2)
       excavation = round(cf.excavation(),2)
       structural_fill = round(cf.strfill(),2)
       backfill = round(cf.backfill(),2)
       grout = round(cf.grout(),2)
       water_stopper = round(cf.waterStopper(),2)
       joint_isolation = round(cf.jointIsolation(),2)
       screed = 0
       embedded_steel = 0
       wire_mesh = 0
       anchor_24 = cf.anchor().get("M24")
       anchor_30 = cf.anchor().get("M30")
       anchor_36 = cf.anchor().get("M36")
       anchor_42 = cf.anchor().get("M42")
       structural_steel = 0
       names = [row[2] for row in db.fetchResults()]
       name = self.found_name.get()
       for version in range(1, 150):
           if f"{name}" not in names:
               print("Name First Time")
               break
           elif f"{name}{version}" in names:
               print("Name Exist")
           else:
               print("Name Unique")
               name = f"{name}{version}"
               break
       db.insertResultGTG("COMBINED FOOTING",
                          name,
                          concrete_foundation * quantity,
                          lean_concrete * quantity,
                          formwork * quantity,
                          rebar * quantity,
                          concrete_protection * quantity,
                          pe_sheet * quantity,
                          excavation * quantity,
                          structural_fill * quantity,
                          backfill * quantity,
                          grout * quantity,
                          screed * quantity,
                          embedded_steel * quantity,
                          wire_mesh * quantity,
                          anchor_24 * quantity,
                          anchor_30 * quantity,
                          anchor_36 * quantity,
                          anchor_42 * quantity,
                          structural_steel * quantity,
                          joint_isolation * quantity,
                          water_stopper * quantity,
                          )

       db.insertCF(name,exc_depth,fill,foundation_depth,width,length,anchor_type,anchor_qty,grout_depth,pedestal_width,pedestal_length,pedestal_height,pedestal_qty,quantity)

       self.populate_list_gt()


   def addMatFoundation(self):
       width = self.zero_check(self.foundation_d1.get())
       length = self.zero_check(self.foundation_d2.get())
       foundation_depth = self.zero_check(self.foundation_depth.get())
       fill = self.zero_check(self.strfill.get())
       es = 0
       steel = 0
       exc_depth = self.zero_check(self.exc_depth.get())
       grout_depth = self.zero_check(self.grouting_depth1.get())
       quantity = self.zero_check(self.quantity.get())
       anchor_type = self.zero_check(self.anchor_type.get())
       anchor_qty = self.zero_check(self.anchor_qty.get())
       mf = Matfoundation(width,length,foundation_depth,fill,anchor_type,anchor_qty,es,steel,exc_depth,grout_depth)

       concrete_foundation = round(mf.strconcrete(), 2)
       lean_concrete = round(mf.leanconc(), 2)
       formwork = round(mf.formwork(), 2)
       rebar = round(mf.rebar(), 2)
       pe_sheet = round(mf.polyethylenesheet(), 2)
       excavation = round(mf.excavation(), 2)
       structural_fill = round(mf.strfill(), 2)
       backfill = round(mf.backfill(), 2)
       concrete_protection = round(mf.concreteprot(), 2)
       grout = round(mf.grout(), 2)
       water_stopper = round(mf.waterStopper(),2)
       joint_isolation = round(mf.jointIsolation(),2)
       screed = 0
       embedded_steel = 0
       wire_mesh = 0
       anchor_24 = mf.anchor().get("M24")
       anchor_30 = mf.anchor().get("M30")
       anchor_36 = mf.anchor().get("M36")
       anchor_42 = mf.anchor().get("M42")
       structural_steel = 0
       names = [row[2] for row in db.fetchResults()]
       name = self.found_name.get()
       for version in range(1, 150):
           if f"{name}" not in names:
               print("Name First Time")
               break
           elif f"{name}{version}" in names:
               print("Name Exist")
           else:
               print("Name Unique")
               name = f"{name}{version}"
               break
       db.insertResultGTG("MAT FOUNDATION",
                          name,
                          concrete_foundation * quantity,
                          lean_concrete * quantity,
                          formwork * quantity,
                          rebar * quantity,
                          concrete_protection * quantity,
                          pe_sheet * quantity,
                          excavation * quantity,
                          structural_fill * quantity,
                          backfill * quantity,
                          grout * quantity,
                          screed * quantity,
                          embedded_steel * quantity,
                          wire_mesh * quantity,
                          anchor_24 * quantity,
                          anchor_30 * quantity,
                          anchor_36 * quantity,
                          anchor_42 * quantity,
                          structural_steel * quantity,
                          0,
                          water_stopper * quantity,
                          )

       db.insertMF(name,
                   exc_depth,
                   fill,
                   foundation_depth,
                   width,
                   length,
                   anchor_type,
                   anchor_qty,
                   grout_depth,
                   quantity)

       self.populate_list_gt()

   def addGTFoundation(self):
       quantity = getint(self.combo_gtno.get())
       auxiliaries = list(self.aux_list2.get(0, tk.END))
       print(auxiliaries)

       gt = [row for row in db.fetchGTG(self.combo_gt_type.get())]
       db.insertResultGTG("GT FOUNDATION",
                          gt[0][0],
                          self.zero_check(gt[0][1]) * quantity,
                          self.zero_check(gt[0][2]) * quantity,
                          self.zero_check(gt[0][3]) * quantity,
                          self.zero_check(gt[0][4]) * quantity,
                          self.zero_check(gt[0][5]) * quantity,
                          self.zero_check(gt[0][6]) * quantity,
                          self.zero_check(gt[0][7]) * quantity,
                          self.zero_check(gt[0][8]) * quantity,
                          self.zero_check(gt[0][9]) * quantity,
                          self.zero_check(gt[0][10]) * quantity,
                          self.zero_check(gt[0][11]) * quantity,
                          self.zero_check(gt[0][12]) * quantity,
                          self.zero_check(gt[0][13]) * quantity,
                          self.zero_check(gt[0][14]) * quantity,
                          self.zero_check(gt[0][15]) * quantity,
                          self.zero_check(gt[0][16]) * quantity,
                          self.zero_check(gt[0][17]) * quantity,
                          self.zero_check(gt[0][18]) * quantity,
                          0,
                          0)

       if self.bypass.get() == 1:
           self.addByPass()

           stackdim = [row for row in db.fetchStack()]

           STACK = Stack()
           STACK.depth_exc = stackdim[0][0]
           STACK.depth_fill = stackdim[0][1]
           STACK.depth_found = stackdim[0][2]
           STACK.width = stackdim[0][3]
           STACK.length = stackdim[0][4]
           STACK.steel_weight = stackdim[0][5]
           STACK.grout_depth1 = stackdim[0][6]
           STACK.grout_depth2 = stackdim[0][7]
           STACK.p1_width = stackdim[0][8]
           STACK.p1_length = stackdim[0][9]
           STACK.p1_depth = stackdim[0][10]
           STACK.p1_qty = stackdim[0][11]
           STACK.p2_width = stackdim[0][12]
           STACK.p2_length = stackdim[0][13]
           STACK.p2_depth = stackdim[0][14]
           STACK.p2_qty = stackdim[0][15]

           db.insertResultGTG("STACK",
                              "BY-PASS STACK",
                              self.zero_check(STACK.concreteFoundation()) * quantity,
                              self.zero_check(STACK.lean_concrete()) * quantity,
                              self.zero_check(STACK.formwork()) * quantity,
                              self.zero_check(STACK.rebar()) * quantity,
                              self.zero_check(STACK.insulationSika()) * quantity,
                              self.zero_check(STACK.pe_sheet()) * quantity,
                              self.zero_check(STACK.excavation()) * quantity,
                              self.zero_check(STACK.structuralfill()) * quantity,
                              self.zero_check(STACK.backfill()) * quantity,
                              self.zero_check(STACK.grout()) * quantity,
                              self.zero_check(STACK.screed()) * quantity,
                              self.zero_check(STACK.embeddedPlate()) * quantity,
                              0,
                              self.zero_check(STACK.anchor24()) * quantity,
                              self.zero_check(STACK.anchor30()) * quantity,
                              self.zero_check(STACK.anchor36()) * quantity,
                              self.zero_check(STACK.anchor42()) * quantity,
                              self.zero_check(STACK.structuralSteel()) * quantity,
                              self.zero_check(STACK.jointIsolation()) * quantity,
                              self.zero_check(STACK.waterStopper()) * quantity,
                              )

       for aux in auxiliaries:
           self.auxExecute(aux)

       self.populate_list_gt()


   def addPit(self):
       print("pit")
       a = self.zero_check(self.dim_a.get()) #a
       b = self.zero_check(self.dim_b.get()) #b
       c = self.zero_check(self.dim_c.get()) #c
       d = self.zero_check(self.dim_d.get()) #d
       e = self.zero_check(self.dim_e.get()) #e
       f = self.zero_check(self.dim_f.get()) #f
       g = self.zero_check(self.dim_g.get()) #g
       h = self.zero_check(self.dim_h.get()) #h
       k = self.zero_check(self.dim_k.get()) #k
       fill = self.zero_check(self.fill.get()) #strfill
       quantity = self.zero_check(self.quantity.get())
       pit = Pit(a,b,c,d,e,f,g,h,k,fill)

       concrete_foundation = round(pit.strconcrete(), 2)
       lean_concrete = round(pit.leanConcrete(), 2)
       formwork = round(pit.formwork(), 2)
       rebar = round(pit.rebar(), 2)
       pe_sheet = round(pit.polyethylenesheet(), 2)
       excavation = round(pit.excavation(), 2)
       structural_fill = round(pit.strFill(), 2)
       backfill = round(pit.backFilling(), 2)
       concrete_protection = round(pit.concreteProtection(), 2)
       water_stopper = round(pit.waterStopper(),2)
       joint_isolation = round(pit.jointIsolation(),2)
       grout = 0
       screed = 0
       embedded_steel = 0
       wire_mesh = 0
       anchor_24 = 0
       anchor_30 = 0
       anchor_36 = 0
       anchor_42 = 0
       structural_steel = 0
       names = [row[2] for row in db.fetchResults()]
       name = self.found_name.get()
       for version in range(1, 150):
           if f"{name}" not in names:
               print("Name First Time")
               break
           elif f"{name}{version}" in names:
               print("Name Exist")
           else:
               print("Name Unique")
               name = f"{name}{version}"
               break
       db.insertResultGTG("PIT",
                          name,
                          concrete_foundation * quantity,
                          lean_concrete * quantity,
                          formwork * quantity,
                          rebar * quantity,
                          concrete_protection * quantity,
                          pe_sheet * quantity,
                          excavation * quantity,
                          structural_fill * quantity,
                          backfill * quantity,
                          grout * quantity,
                          screed * quantity,
                          embedded_steel * quantity,
                          wire_mesh * quantity,
                          anchor_24 * quantity,
                          anchor_30 * quantity,
                          anchor_36 * quantity,
                          anchor_42 * quantity,
                          structural_steel * quantity,
                          joint_isolation * quantity,
                          water_stopper * quantity,
                          )

       db.insertPIT(name,
                    a,
                    b,
                    c,
                    d,
                    e,
                    f,
                    g,
                    h,
                    k,
                    fill,
                    quantity)

       self.populate_list_gt()

   def addTankFoundation(self):
       print(f"{self.tank_type.get()} Tank Added")
       print(f"TANK TYPE: {self.tank_type.get()}")
       if self.tank_type.get() == "CYLINDER":
           quantity = self.zero_check(self.quantity.get())
           found_name = self.zero_check(self.found_name.get())
           D1 = self.zero_check(self.R1.get())
           D2 = self.zero_check(self.R2.get())
           dim_a = self.zero_check(self.a.get())
           dim_b = self.zero_check(self.b.get())
           dim_c = self.zero_check(self.c.get())
           dim_d = self.zero_check(self.d.get())
           dim_e = self.zero_check(self.e.get())
           exc_depth = self.zero_check(self.exc_depth.get())
           fill = self.zero_check(self.strfill.get())
           tank_height = self.zero_check(self.tank_height.get())
           anchor_type = self.zero_check(self.anchor_type.get())
           anchor_qty = self.zero_check(self.anchor_qty.get())
           is_chemical = self.zero_check(self.chemical.get())
           tank_type = self.zero_check(self.tank_type.get())

           cylinder_tank = CylinderTank(D1,D2,dim_a,dim_b,dim_c,dim_d,dim_e,exc_depth,fill,tank_height,anchor_type,anchor_qty,0.025,is_chemical)

           concrete_foundation = round(cylinder_tank.strconcrete(), 2)
           lean_concrete = round(cylinder_tank.leanconc(), 2)
           formwork = round(cylinder_tank.formwork(), 2)
           rebar = round(cylinder_tank.rebar(), 2)
           concrete_protection = round(cylinder_tank.concreteprot(), 2)
           pe_sheet = round(cylinder_tank.polyethylenesheet(), 2)
           excavation = round(cylinder_tank.excavation(), 2)
           structural_fill = round(cylinder_tank.strfill(), 2)
           backfill = round(cylinder_tank.backfill(), 2)
           grout = round(cylinder_tank.grout(), 2)
           water_stopper = round(cylinder_tank.waterStopper(), 2)
           joint_isolation = round(cylinder_tank.jointIsolation(), 2)
           screed = 0
           embedded_steel = 0
           wire_mesh = 0
           anchor_24 = cylinder_tank.anchor().get("M24")
           anchor_30 = cylinder_tank.anchor().get("M30")
           anchor_36 = cylinder_tank.anchor().get("M36")
           anchor_42 = cylinder_tank.anchor().get("M42")
           structural_steel = 0
           names = [row[2] for row in db.fetchResults()]
           name = self.found_name.get()
           for version in range(1, 150):
               if f"{name}" not in names:
                   print("Name First Time")
                   break
               elif f"{name}{version}" in names:
                   print("Name Exist")
               else:
                   print("Name Unique")
                   name = f"{name}{version}"
                   break
           db.insertResultGTG("CYLINDER TANK",
                              name,
                              concrete_foundation * quantity,
                              lean_concrete * quantity,
                              formwork * quantity,
                              rebar * quantity,
                              concrete_protection * quantity,
                              pe_sheet * quantity,
                              excavation * quantity,
                              structural_fill * quantity,
                              backfill * quantity,
                              grout * quantity,
                              screed * quantity,
                              embedded_steel * quantity,
                              wire_mesh * quantity,
                              anchor_24 * quantity,
                              anchor_30 * quantity,
                              anchor_36 * quantity,
                              anchor_42 * quantity,
                              structural_steel * quantity,
                              joint_isolation * quantity,
                              water_stopper * quantity,
                              )

           db.insertcylinderTANK(name,
                         tank_type,
                         is_chemical,
                         D1,
                         D2,
                         dim_a,
                         dim_b,
                         dim_c,
                         dim_d,
                         dim_e,
                         exc_depth,
                         fill,
                         tank_height,
                         anchor_type,
                         anchor_qty,
                         quantity)

           self.populate_list_gt()
       elif self.tank_type.get() == "HEXAGON":
           quantity = self.zero_check(self.quantity.get())
           found_name = self.zero_check(self.found_name.get())
           D1 = self.zero_check(self.D1.get())
           D2 = self.zero_check(self.D2.get())
           dim_a = self.zero_check(self.a.get())
           dim_b = self.zero_check(self.b.get())
           exc_depth = self.zero_check(self.exc_depth.get())
           fill = self.zero_check(self.strfill.get())
           tank_height = self.zero_check(self.tank_height.get())
           anchor_type = self.zero_check(self.anchor_type.get())
           anchor_qty = self.zero_check(self.anchor_qty.get())
           is_chemical = self.zero_check(self.chemical.get())
           tank_type = self.zero_check(self.tank_type.get())

           other_tank = HexTank(D1, D2, dim_a, dim_b, exc_depth, fill, tank_height,anchor_type, anchor_qty, 0.025, is_chemical)

           concrete_foundation = round(other_tank.strconcrete(), 2)
           lean_concrete = round(other_tank.leanconc(), 2)
           formwork = round(other_tank.formwork(), 2)
           rebar = round(other_tank.rebar(), 2)
           concrete_protection = round(other_tank.concreteprot(), 2)
           pe_sheet = round(other_tank.polyethylenesheet(), 2)
           excavation = round(other_tank.excavation(), 2)
           structural_fill = round(other_tank.strfill(), 2)
           backfill = round(other_tank.backfill(), 2)
           grout = round(other_tank.grout(), 2)
           water_stopper = round(other_tank.waterStopper(), 2)
           joint_isolation = round(other_tank.jointIsolation(), 2)
           screed = 0
           embedded_steel = 0
           wire_mesh = 0
           anchor_24 = other_tank.anchor().get("M24")
           anchor_30 = other_tank.anchor().get("M30")
           anchor_36 = other_tank.anchor().get("M36")
           anchor_42 = other_tank.anchor().get("M42")
           structural_steel = 0
           names = [row[2] for row in db.fetchResults()]
           name = self.found_name.get()
           for version in range(1, 150):
               if f"{name}" not in names:
                   print("Name First Time")
                   break
               elif f"{name}{version}" in names:
                   print("Name Exist")
               else:
                   print("Name Unique")
                   name = f"{name}{version}"
                   break
           db.insertResultGTG("HEXAGON TANK",
                              name,
                              concrete_foundation * quantity,
                              lean_concrete * quantity,
                              formwork * quantity,
                              rebar * quantity,
                              concrete_protection * quantity,
                              pe_sheet * quantity,
                              excavation * quantity,
                              structural_fill * quantity,
                              backfill * quantity,
                              grout * quantity,
                              screed * quantity,
                              embedded_steel * quantity,
                              wire_mesh * quantity,
                              anchor_24 * quantity,
                              anchor_30 * quantity,
                              anchor_36 * quantity,
                              anchor_42 * quantity,
                              structural_steel * quantity,
                              joint_isolation * quantity,
                              water_stopper * quantity,
                              )

           db.insertTANK(name,
                         tank_type,
                         is_chemical,
                         D1,
                         D2,
                         dim_a,
                         dim_b,
                         exc_depth,
                         fill,
                         tank_height,
                         anchor_type,
                         anchor_qty,
                         quantity)

           self.populate_list_gt()
       elif self.tank_type.get() == "HEXAGON(SQUARE_BASE)":
           quantity = self.zero_check(self.quantity.get())
           found_name = self.zero_check(self.found_name.get())
           D1 = self.zero_check(self.D1.get())
           D2 = self.zero_check(self.D2.get())
           dim_a = self.zero_check(self.a.get())
           dim_b = self.zero_check(self.b.get())
           exc_depth = self.zero_check(self.exc_depth.get())
           fill = self.zero_check(self.strfill.get())
           tank_height = self.zero_check(self.tank_height.get())
           anchor_type = self.zero_check(self.anchor_type.get())
           anchor_qty = self.zero_check(self.anchor_qty.get())
           is_chemical = self.zero_check(self.chemical.get())
           tank_type = self.zero_check(self.tank_type.get())

           other_tank = HexSqTank(D1, D2, dim_a, dim_b, exc_depth, fill, tank_height,anchor_type, anchor_qty, 0.025, is_chemical)

           concrete_foundation = round(other_tank.strconcrete(), 2)
           lean_concrete = round(other_tank.leanconc(), 2)
           formwork = round(other_tank.formwork(), 2)
           rebar = round(other_tank.rebar(), 2)
           concrete_protection = round(other_tank.concreteprot(), 2)
           pe_sheet = round(other_tank.polyethylenesheet(), 2)
           excavation = round(other_tank.excavation(), 2)
           structural_fill = round(other_tank.strfill(), 2)
           backfill = round(other_tank.backfill(), 2)
           grout = round(other_tank.grout(), 2)
           water_stopper = round(other_tank.waterStopper(), 2)
           joint_isolation = round(other_tank.jointIsolation(), 2)
           screed = 0
           embedded_steel = 0
           wire_mesh = 0
           anchor_24 = other_tank.anchor().get("M24")
           anchor_30 = other_tank.anchor().get("M30")
           anchor_36 = other_tank.anchor().get("M36")
           anchor_42 = other_tank.anchor().get("M42")
           structural_steel = 0
           names = [row[2] for row in db.fetchResults()]
           name = self.found_name.get()
           for version in range(1, 150):
               if f"{name}" not in names:
                   print("Name First Time")
                   break
               elif f"{name}{version}" in names:
                   print("Name Exist")
               else:
                   print("Name Unique")
                   name = f"{name}{version}"
                   break
           db.insertResultGTG("HEXAGON(SQUARE_BASE) TANK",
                              name,
                              concrete_foundation * quantity,
                              lean_concrete * quantity,
                              formwork * quantity,
                              rebar * quantity,
                              concrete_protection * quantity,
                              pe_sheet * quantity,
                              excavation * quantity,
                              structural_fill * quantity,
                              backfill * quantity,
                              grout * quantity,
                              screed * quantity,
                              embedded_steel * quantity,
                              wire_mesh * quantity,
                              anchor_24 * quantity,
                              anchor_30 * quantity,
                              anchor_36 * quantity,
                              anchor_42 * quantity,
                              structural_steel * quantity,
                              joint_isolation * quantity,
                              water_stopper * quantity,
                              )

           db.insertTANK(name,
                         tank_type,
                         is_chemical,
                         D1,
                         D2,
                         dim_a,
                         dim_b,
                         exc_depth,
                         fill,
                         tank_height,
                         anchor_type,
                         anchor_qty,
                         quantity)

           self.populate_list_gt()
       elif self.tank_type.get() == "OCTAGON":
           quantity = self.zero_check(self.quantity.get())
           found_name = self.zero_check(self.found_name.get())
           D1 = self.zero_check(self.D1.get())
           D2 = self.zero_check(self.D2.get())
           dim_a = self.zero_check(self.a.get())
           dim_b = self.zero_check(self.b.get())
           exc_depth = self.zero_check(self.exc_depth.get())
           fill = self.zero_check(self.strfill.get())
           tank_height = self.zero_check(self.tank_height.get())
           anchor_type = self.zero_check(self.anchor_type.get())
           anchor_qty = self.zero_check(self.anchor_qty.get())
           is_chemical = self.zero_check(self.chemical.get())
           tank_type = self.zero_check(self.tank_type.get())

           other_tank = OctTank(D1, D2, dim_a, dim_b, exc_depth, fill, tank_height,anchor_type, anchor_qty, 0.025, is_chemical)

           concrete_foundation = round(other_tank.strconcrete(), 2)
           lean_concrete = round(other_tank.leanconc(), 2)
           formwork = round(other_tank.formwork(), 2)
           rebar = round(other_tank.rebar(), 2)
           concrete_protection = round(other_tank.concreteprot(), 2)
           pe_sheet = round(other_tank.polyethylenesheet(), 2)
           excavation = round(other_tank.excavation(), 2)
           structural_fill = round(other_tank.strfill(), 2)
           backfill = round(other_tank.backfill(), 2)
           grout = round(other_tank.grout(), 2)
           water_stopper = round(other_tank.waterStopper(), 2)
           joint_isolation = round(other_tank.jointIsolation(), 2)
           screed = 0
           embedded_steel = 0
           wire_mesh = 0
           anchor_24 = other_tank.anchor().get("M24")
           anchor_30 = other_tank.anchor().get("M30")
           anchor_36 = other_tank.anchor().get("M36")
           anchor_42 = other_tank.anchor().get("M42")
           structural_steel = 0
           names = [row[2] for row in db.fetchResults()]
           name = self.found_name.get()
           for version in range(1, 150):
               if f"{name}" not in names:
                   print("Name First Time")
                   break
               elif f"{name}{version}" in names:
                   print("Name Exist")
               else:
                   print("Name Unique")
                   name = f"{name}{version}"
                   break
           db.insertResultGTG("OCTAGON TANK",
                              name,
                              concrete_foundation * quantity,
                              lean_concrete * quantity,
                              formwork * quantity,
                              rebar * quantity,
                              concrete_protection * quantity,
                              pe_sheet * quantity,
                              excavation * quantity,
                              structural_fill * quantity,
                              backfill * quantity,
                              grout * quantity,
                              screed * quantity,
                              embedded_steel * quantity,
                              wire_mesh * quantity,
                              anchor_24 * quantity,
                              anchor_30 * quantity,
                              anchor_36 * quantity,
                              anchor_42 * quantity,
                              structural_steel * quantity,
                              joint_isolation * quantity,
                              water_stopper * quantity,
                              )

           db.insertTANK(name,
                         tank_type,
                         is_chemical,
                         D1,
                         D2,
                         dim_a,
                         dim_b,
                         exc_depth,
                         fill,
                         tank_height,
                         anchor_type,
                         anchor_qty,
                         quantity)

           self.populate_list_gt()
       elif self.tank_type.get() == "OCTAGON(SQUARE_BASE)":
           quantity = self.zero_check(self.quantity.get())
           found_name = self.zero_check(self.found_name.get())
           D1 = self.zero_check(self.D1.get())
           D2 = self.zero_check(self.D2.get())
           dim_a = self.zero_check(self.a.get())
           dim_b = self.zero_check(self.b.get())
           exc_depth = self.zero_check(self.exc_depth.get())
           fill = self.zero_check(self.strfill.get())
           tank_height = self.zero_check(self.tank_height.get())
           anchor_type = self.zero_check(self.anchor_type.get())
           anchor_qty = self.zero_check(self.anchor_qty.get())
           is_chemical = self.zero_check(self.chemical.get())
           tank_type = self.zero_check(self.tank_type.get())

           other_tank = OctSqTank(D1, D2, dim_a, dim_b, exc_depth, fill, tank_height,anchor_type, anchor_qty, 0.025, is_chemical)

           concrete_foundation = round(other_tank.strconcrete(), 2)
           lean_concrete = round(other_tank.leanconc(), 2)
           formwork = round(other_tank.formwork(), 2)
           rebar = round(other_tank.rebar(), 2)
           concrete_protection = round(other_tank.concreteprot(), 2)
           pe_sheet = round(other_tank.polyethylenesheet(), 2)
           excavation = round(other_tank.excavation(), 2)
           structural_fill = round(other_tank.strfill(), 2)
           backfill = round(other_tank.backfill(), 2)
           grout = round(other_tank.grout(), 2)
           water_stopper = round(other_tank.waterStopper(), 2)
           joint_isolation = round(other_tank.jointIsolation(), 2)
           screed = 0
           embedded_steel = 0
           wire_mesh = 0
           anchor_24 = other_tank.anchor().get("M24")
           anchor_30 = other_tank.anchor().get("M30")
           anchor_36 = other_tank.anchor().get("M36")
           anchor_42 = other_tank.anchor().get("M42")
           structural_steel = 0
           names = [row[2] for row in db.fetchResults()]
           name = self.found_name.get()
           for version in range(1, 150):
               if f"{name}" not in names:
                   print("Name First Time")
                   break
               elif f"{name}{version}" in names:
                   print("Name Exist")
               else:
                   print("Name Unique")
                   name = f"{name}{version}"
                   break
           db.insertResultGTG("OCTAGON(SQUARE_BASE) TANK",
                              name,
                              concrete_foundation * quantity,
                              lean_concrete * quantity,
                              formwork * quantity,
                              rebar * quantity,
                              concrete_protection * quantity,
                              pe_sheet * quantity,
                              excavation * quantity,
                              structural_fill * quantity,
                              backfill * quantity,
                              grout * quantity,
                              screed * quantity,
                              embedded_steel * quantity,
                              wire_mesh * quantity,
                              anchor_24 * quantity,
                              anchor_30 * quantity,
                              anchor_36 * quantity,
                              anchor_42 * quantity,
                              structural_steel * quantity,
                              joint_isolation * quantity,
                              water_stopper * quantity,
                              )

           db.insertTANK(name,
                         tank_type,
                         is_chemical,
                         D1,
                         D2,
                         dim_a,
                         dim_b,
                         exc_depth,
                         fill,
                         tank_height,
                         anchor_type,
                         anchor_qty,
                         quantity)

           self.populate_list_gt()



   def addDW(self):
       print("Dyke Wall Added")
       dw_thickness = self.zero_check(self.dyke_wall_thk2.get())
       dw_height = self.zero_check(self.dyke_wall_height2.get())
       dw_perimeter_width = self.zero_check(self.dw_width2.get())
       dw_perimeter_length = self.zero_check(self.dw_length2.get())
       dw_foundation_depth = self.zero_check(self.dw_found_depth2.get())
       dw_foundation_width = self.zero_check(self.dw_found_width2.get())
       dw_exc_depth = self.zero_check(self.dw_exc_depth2.get())
       dw_strfill = self.zero_check(self.dw_strfill.get())
       dw = DykeWall(dw_thickness,
                     dw_height,
                     dw_perimeter_width,
                     dw_perimeter_length,
                     dw_foundation_depth,
                     dw_foundation_width,
                     dw_exc_depth,
                     dw_strfill)
       concrete_foundation = round(dw.strconcrete(), 2)
       lean_concrete = round(dw.leanconc(), 2)
       formwork = round(dw.formwork(), 2)
       rebar = round(dw.rebar(), 2)
       pe_sheet = round(dw.polyethylenesheet(), 2)
       excavation = round(dw.excavation(), 2)
       structural_fill = round(dw.strfill(), 2)
       backfill = round(dw.backfill(), 2)
       concrete_protection = round(dw.concreteprot(), 2)
       grout = round(dw.grout(), 2)
       water_stopper = round(dw.waterStopper(),2)
       joint_isolation = round(dw.jointIsolation(),2)
       screed = 0
       embedded_steel = 0
       wire_mesh = 0
       anchor_24 = 0
       anchor_30 = 0
       anchor_36 = 0
       anchor_42 = 0
       structural_steel = 0
       names = [row[2] for row in db.fetchResults()]
       name = "DYKE WALL"
       for version in range(1, 150):
           if f"DYKE WALL{version}" in names:
               print("Name Exist")
           else:
               print("Name Unique")
               name = f"DYKE WALL{version}"
               break



       quantity = 1
       db.insertResultGTG("WALL FOUNDATION1",
                          name,
                          concrete_foundation * quantity,
                          lean_concrete * quantity,
                          formwork * quantity,
                          rebar * quantity,
                          concrete_protection * quantity,
                          pe_sheet * quantity,
                          excavation * quantity,
                          structural_fill * quantity,
                          backfill * quantity,
                          grout * quantity,
                          screed * quantity,
                          embedded_steel * quantity,
                          wire_mesh * quantity,
                          anchor_24 * quantity,
                          anchor_30 * quantity,
                          anchor_36 * quantity,
                          anchor_42 * quantity,
                          structural_steel * quantity,
                          joint_isolation * quantity,
                          water_stopper * quantity,
                          )

       db.insertDW(name,
                   dw_thickness,
                   dw_height,
                   dw_perimeter_width,
                   dw_perimeter_length,
                   dw_foundation_depth,
                   dw_foundation_width,
                   dw_exc_depth,
                   dw_strfill)

       self.populate_list_gt()

   def addGSU(self):
       pass

   def zero_check(self, input):
        if input is None or input == '':
            return 0
        else:
            return input

   def execute(self):
       db.drop_table_works()
       pricesheet.table_output()

       works = [3.2, 3.1, 4.1, 5.1, 17.1, 17.4, 2.4, 2.7, 2.11, 3.11, 3.12, 5.2, 6.1, 6.2, 6.3, 6.4, 7.1,21.8,21.5]

       items = [row[2] for row in db.fetchResults()]
       try:
           for item in items:
               db.alter_add_column(item)
       except sqlite3.OperationalError:
           messagebox.showerror("-- ERROR --", "Please change duplicated foundation names!", icon="warning")
           return


       for work in db.fetchResults():
           print(work)
           results = list(work[3:])
           print(results)
           for i in range(0, len(works)):
               db.update_works(work[2], results[i], works[i])

       pricesheet.print()
       pricesheet.open_output()


   def auxExecute(self,aux):
       #aux = auxillary()
       if self.gtindoor.get() == 1:
           AUX_RESULT = [row for row in db.fetchAUX_indoor(aux)]
       else:
           AUX_RESULT = [row for row in db.fetchAUX(aux)]
       db.insertResultGTG("SKID",
                          AUX_RESULT[0][0],
                          round( self.zero_check(AUX_RESULT[0][1]),2),
                          round(self.zero_check(AUX_RESULT[0][2]),2),
                          round(self.zero_check(AUX_RESULT[0][3]),2),
                          round(self.zero_check(AUX_RESULT[0][4]),2),
                          round(self.zero_check(AUX_RESULT[0][5]),2),
                          round(self.zero_check(AUX_RESULT[0][6]),2),
                          round(self.zero_check(AUX_RESULT[0][7]),2),
                          round(self.zero_check(AUX_RESULT[0][8]),2),
                          round(self.zero_check(AUX_RESULT[0][9]),2),
                          round(self.zero_check(AUX_RESULT[0][10]),2),
                          round(self.zero_check(AUX_RESULT[0][11]),2),
                          round(self.zero_check(AUX_RESULT[0][12]),2),
                          round(self.zero_check(AUX_RESULT[0][13]),2),
                          round(self.zero_check(AUX_RESULT[0][14]),2),
                          round(self.zero_check(AUX_RESULT[0][15]),2),
                          round(self.zero_check(AUX_RESULT[0][16]),2),
                          round(self.zero_check(AUX_RESULT[0][17]),2),
                          round(self.zero_check(AUX_RESULT[0][18]),2),
                          0,
                          0,
                          )

   def bypassAdd(self):
       """
       exc_depth
       strfill
       foundation_depth
       foundation_D1
       foundation_D2
       pedestals:
            pedestal_d1
            pedestal_d2
            pedestal_depth
            pedestal_qty
      steel_weight
      grouting_depth
       """
       print(self.bypass.get())
       if self.bypass.get() == 1:
           self.frame2 = Frame(self)
           self.frame2.place(relx=0.42, rely=0.075, relwidth=0.35, relheight=0.3)
           self.lbl_exc_depth = ttk.Label(self.frame2, text='Excavation Depth:', font=("Pickwick", 8, "bold"))
           self.lbl_strfill = ttk.Label(self.frame2, text='Structural Fill:', font=("Pickwick", 8, "bold"))
           self.lbl_foundation_depth = ttk.Label(self.frame2, text='Foundation Depth:', font=("Pickwick", 8, "bold"))
           self.lbl_foundation_d1 = ttk.Label(self.frame2, text='Foundation Width:', font=("Pickwick", 8, "bold"))
           self.lbl_foundation_d2 = ttk.Label(self.frame2, text='Foundation Length:', font=("Pickwick", 8, "bold"))
           self.lbl_p1 = ttk.Label(self.frame2, text='Pedestal Type1', font=("Pickwick", 8, "bold"))
           self.lbl_p1_width = ttk.Label(self.frame2, text='P1_Width', font=("Pickwick", 8, "bold"))
           self.lbl_p1_length = ttk.Label(self.frame2, text='P1_Length', font=("Pickwick", 8, "bold"))
           self.lbl_p1_depth = ttk.Label(self.frame2, text='P1_Depth', font=("Pickwick", 8, "bold"))
           self.lbl_p1_qty = ttk.Label(self.frame2, text='P1_Qty', font=("Pickwick", 8, "bold"))
           self.lbl_p2 = ttk.Label(self.frame2, text='Pedestal Type2', font=("Pickwick", 8, "bold"))
           self.lbl_p2_width = ttk.Label(self.frame2, text='P2_Width', font=("Pickwick", 8, "bold"))
           self.lbl_p2_length = ttk.Label(self.frame2, text='P2_Length', font=("Pickwick", 8, "bold"))
           self.lbl_p2_depth = ttk.Label(self.frame2, text='P2_Depth', font=("Pickwick", 8, "bold"))
           self.lbl_p2_qty = ttk.Label(self.frame2, text='P2_Qty', font=("Pickwick", 8, "bold"))
           self.lbl_steel_weight = ttk.Label(self.frame2, text='Steel Weight:', font=("Pickwick", 8, "bold"))
           self.lbl_grouting_depth1 = ttk.Label(self.frame2, text='Grout Depth P1:', font=("Pickwick", 8, "bold"))
           self.lbl_grouting_depth2 = ttk.Label(self.frame2, text='Grout Depth P2:', font=("Pickwick", 8, "bold"))

           self.exc_depth = DoubleVar()
           self.strfill = DoubleVar()
           self.foundation_depth = DoubleVar()
           self.foundation_d1 = DoubleVar()
           self.foundation_d2 = DoubleVar()
           self.steel_weight = DoubleVar()
           self.grouting_depth1 = DoubleVar()
           self.grouting_depth2 = DoubleVar()
           self.p1_width = DoubleVar()
           self.p1_length = DoubleVar()
           self.p1_depth = DoubleVar()
           self.p1_qty = DoubleVar()
           self.p2_width = DoubleVar()
           self.p2_length = DoubleVar()
           self.p2_depth = DoubleVar()
           self.p2_qty = DoubleVar()

           self.txt_exc_depth = ttk.Entry(self.frame2, width=5, textvariable=self.exc_depth)
           self.txt_strfill = ttk.Entry(self.frame2, width=5, textvariable=self.strfill)
           self.txt_foundation_depth = ttk.Entry(self.frame2, width=5, textvariable=self.foundation_depth)
           self.txt_foundation_d1 = ttk.Entry(self.frame2, width=5, textvariable=self.foundation_d1)
           self.txt_foundation_d2 = ttk.Entry(self.frame2, width=5, textvariable=self.foundation_d2)
           self.txt_steel_weight = ttk.Entry(self.frame2, width=5, textvariable=self.steel_weight)
           self.txt_grouting_depth1 = ttk.Entry(self.frame2, width=5, textvariable=self.grouting_depth1)
           self.txt_grouting_depth2 = ttk.Entry(self.frame2, width=5, textvariable=self.grouting_depth2)
           self.txt_p1_width = ttk.Entry(self.frame2, width=5, textvariable=self.p1_width)
           self.txt_p1_length = ttk.Entry(self.frame2, width=5, textvariable=self.p1_length)
           self.txt_p1_depth = ttk.Entry(self.frame2, width=5, textvariable=self.p1_depth)
           self.txt_p1_qty = ttk.Entry(self.frame2, width=5, textvariable=self.p1_qty)
           self.txt_p2_width = ttk.Entry(self.frame2, width=5, textvariable=self.p2_width)
           self.txt_p2_length = ttk.Entry(self.frame2, width=5, textvariable=self.p2_length)
           self.txt_p2_depth = ttk.Entry(self.frame2, width=5, textvariable=self.p2_depth)
           self.txt_p2_qty = ttk.Entry(self.frame2, width=5, textvariable=self.p2_qty)

           self.lbl_exc_depth.place(relx=0.01, rely=0.04, relwidth=0.25, relheight=0.075)
           self.lbl_strfill.place(relx=0.01, rely=0.116, relwidth=0.25, relheight=0.075)
           self.lbl_foundation_depth.place(relx=0.01, rely=0.191, relwidth=0.25, relheight=0.075)
           self.lbl_foundation_d1.place(relx=0.01, rely=0.267, relwidth=0.25, relheight=0.075)
           self.lbl_foundation_d2.place(relx=0.01, rely=0.343, relwidth=0.25, relheight=0.075)
           self.lbl_steel_weight.place(relx=0.01, rely=0.419, relwidth=0.25, relheight=0.075)
           self.lbl_grouting_depth1.place(relx=0.01, rely=0.495, relwidth=0.25, relheight=0.075)
           self.lbl_grouting_depth2.place(relx=0.4, rely=0.495, relwidth=0.25, relheight=0.075)

           self.txt_exc_depth.place(relx=0.27, rely=0.04, relwidth=0.08, relheight=0.075)
           self.txt_strfill.place(relx=0.27, rely=0.116, relwidth=0.08, relheight=0.075)
           self.txt_foundation_depth.place(relx=0.27, rely=0.191, relwidth=0.08, relheight=0.075)
           self.txt_foundation_d1.place(relx=0.27, rely=0.267, relwidth=0.08, relheight=0.075)
           self.txt_foundation_d2.place(relx=0.27, rely=0.343, relwidth=0.08, relheight=0.075)
           self.txt_steel_weight.place(relx=0.27, rely=0.419, relwidth=0.08, relheight=0.075)
           self.txt_grouting_depth1.place(relx=0.27, rely=0.495, relwidth=0.08, relheight=0.075)
           self.txt_grouting_depth2.place(relx=0.62, rely=0.495, relwidth=0.08, relheight=0.075)


           self.lbl_p1.place(relx=0.37, rely=0.561, relwidth=0.2, relheight=0.075)
           self.lbl_p1_width.place(relx=0.01, rely=0.636, relwidth=0.12, relheight=0.075)
           self.txt_p1_width.place(relx=0.14, rely=0.636, relwidth=0.08, relheight=0.075)
           self.lbl_p1_length.place(relx=0.23, rely=0.636, relwidth=0.12, relheight=0.075)
           self.txt_p1_length.place(relx=0.36, rely=0.636, relwidth=0.08, relheight=0.075)
           self.lbl_p1_depth.place(relx=0.45, rely=0.636, relwidth=0.12, relheight=0.075)
           self.txt_p1_depth.place(relx=0.58, rely=0.636, relwidth=0.08, relheight=0.075)
           self.lbl_p1_qty.place(relx=0.67, rely=0.636, relwidth=0.12, relheight=0.075)
           self.txt_p1_qty.place(relx=0.8, rely=0.636, relwidth=0.08, relheight=0.075)

           self.lbl_p2.place(relx=0.37, rely=0.732, relwidth=0.2, relheight=0.075)
           self.lbl_p2_width.place(relx=0.01, rely=0.808, relwidth=0.12, relheight=0.075)
           self.txt_p2_width.place(relx=0.14, rely=0.808, relwidth=0.08, relheight=0.075)
           self.lbl_p2_length.place(relx=0.23, rely=0.808, relwidth=0.12, relheight=0.075)
           self.txt_p2_length.place(relx=0.36, rely=0.808, relwidth=0.08, relheight=0.075)
           self.lbl_p2_depth.place(relx=0.45, rely=0.808, relwidth=0.12, relheight=0.075)
           self.txt_p2_depth.place(relx=0.58, rely=0.808, relwidth=0.08, relheight=0.075)
           self.lbl_p2_qty.place(relx=0.67, rely=0.808, relwidth=0.12, relheight=0.075)
           self.txt_p2_qty.place(relx=0.8, rely=0.808, relwidth=0.08, relheight=0.075)
       else:
           self.frame2.place_forget()

   def singleFooting(self):
       """
       exc_depth
       strfill
       foundation_depth
       foundation_d1
       foundation_d2
       pedestals:
            pedestal_d1
            pedestal_d2
            pedestal_depth
      anchor
      grouting_depth
       """
       print("Single Footing")
       self.frame2.place_forget()
       self.frame1.place_forget()
       self.frame_dw.place_forget()
       self.frame_sf.place(relx=0.01, rely=0.075, relwidth=0.7, relheight=0.5)
       self.bypass_button.place_forget()
       for widgets in self.frame_sf.winfo_children():
           widgets.destroy()
       param_img = found_pic(self.frame_sf)
       param_img.param_type = "sf"
       param_img.open_image()
       param_img.place(relx=0.4, rely=0.116, relwidth=0.6, relheight=0.85)

       self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth:', font=("Pickwick", 8, "bold"))
       self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_depth = ttk.Label(self.frame_sf, text='Foundation Depth:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_d1 = ttk.Label(self.frame_sf, text='Foundation Width:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_d2 = ttk.Label(self.frame_sf, text='Foundation Length:', font=("Pickwick", 8, "bold"))
       self.lbl_p1 = ttk.Label(self.frame_sf, text='Pedestal', font=("Pickwick", 8, "bold"))
       self.lbl_p1_width = ttk.Label(self.frame_sf, text='Pedestal_Width', font=("Pickwick", 8, "bold"))
       self.lbl_p1_length = ttk.Label(self.frame_sf, text='Pedestal_Length', font=("Pickwick", 8, "bold"))
       self.lbl_p1_depth = ttk.Label(self.frame_sf, text='Pedestal_Depth', font=("Pickwick", 8, "bold"))
       self.lbl_grouting_depth1 = ttk.Label(self.frame_sf, text='Grout Depth:', font=("Pickwick", 8, "bold"))

       self.exc_depth = DoubleVar()
       self.strfill = DoubleVar()
       self.foundation_depth = DoubleVar()
       self.foundation_d1 = DoubleVar()
       self.foundation_d2 = DoubleVar()
       self.grouting_depth1 = DoubleVar()
       self.p1_width = DoubleVar()
       self.p1_length = DoubleVar()
       self.p1_depth = DoubleVar()
       self.found_name = StringVar()
       self.quantity = IntVar()
       self.anchor_qty = IntVar()
       self.anchor_type = StringVar()

       self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
       self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
       self.txt_foundation_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_depth)
       self.txt_foundation_d1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_d1)
       self.txt_foundation_d2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_d2)
       self.txt_grouting_depth1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.grouting_depth1)
       self.txt_p1_width = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_width)
       self.txt_p1_length = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_length)
       self.txt_p1_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_depth)

       self.lbl_exc_depth.place(relx=0.01, rely=0.04, relwidth=0.1, relheight=0.075)
       self.lbl_strfill.place(relx=0.01, rely=0.116, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_depth.place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_d1.place(relx=0.01, rely=0.267, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_d2.place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
       self.lbl_grouting_depth1.place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)

       self.txt_exc_depth.place(relx=0.12, rely=0.04, relwidth=0.08, relheight=0.075)
       self.txt_strfill.place(relx=0.12, rely=0.116, relwidth=0.08, relheight=0.075)
       self.txt_foundation_depth.place(relx=0.12, rely=0.191, relwidth=0.08, relheight=0.075)
       self.txt_foundation_d1.place(relx=0.12, rely=0.267, relwidth=0.08, relheight=0.075)
       self.txt_foundation_d2.place(relx=0.12, rely=0.343, relwidth=0.08, relheight=0.075)
       self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
       self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
       self.txt_anchor_qty.place(relx=0.12, rely=0.419, relwidth=0.08, relheight=0.075)
       self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.23,rely=0.419,relwidth=0.1,relheight=0.075)
       self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
       self.combo_anchor_type['values'] = ("M24", "M30", "M36", "M42")
       self.combo_anchor_type.set(f'{self.anchor_type.get()}')
       self.combo_anchor_type.place(relx=0.34, rely=0.419, relwidth=0.05, relheight=0.075)
       self.txt_grouting_depth1.place(relx=0.12, rely=0.495, relwidth=0.08, relheight=0.075)


       self.lbl_p1_width.place(relx=0.23, rely=0.191, relwidth=0.1, relheight=0.075)
       self.txt_p1_width.place(relx=0.34, rely=0.191, relwidth=0.05, relheight=0.075)
       self.lbl_p1_length.place(relx=0.23, rely=0.267, relwidth=0.1, relheight=0.075)
       self.txt_p1_length.place(relx=0.34, rely=0.267, relwidth=0.05, relheight=0.075)
       self.lbl_p1_depth.place(relx=0.23, rely=0.343, relwidth=0.1, relheight=0.075)
       self.txt_p1_depth.place(relx=0.34, rely=0.343, relwidth=0.05, relheight=0.075)

       self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.04, relwidth=0.1, relheight=0.075)
       self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
       self.txt_found_name.place(relx=0.34, rely=0.04, relwidth=0.25, relheight=0.075)
       self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.116, relwidth=0.1, relheight=0.075)
       self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
       self.txt_quantity.place(relx=0.34, rely=0.116, relwidth=0.05, relheight=0.075)

       self.bypass_button = ttk.Button(self, text="ADD FOUNDATION", command=self.addSingleFooting, cursor="hand2",style = 'W.TButton')
       self.bypass_button.place(relx=0.72, rely=0.377, relwidth=0.09, relheight=0.05)

       try:
           if selected_item[1] == "SINGLE FOOTING":
               try:
                   self.txt_exc_depth.delete(0,tk.END)
                   self.txt_strfill.delete(0,tk.END)
                   self.txt_foundation_depth.delete(0,tk.END)
                   self.txt_foundation_d1.delete(0,tk.END)
                   self.txt_foundation_d2.delete(0,tk.END)
                   self.txt_anchor_qty.delete(0,tk.END)
                   self.txt_grouting_depth1.delete(0,tk.END)
                   self.txt_quantity.delete(0,tk.END)
                   self.txt_p1_width.delete(0,tk.END)
                   self.txt_p1_length.delete(0,tk.END)
                   self.txt_p1_depth.delete(0,tk.END)
                   self.combo_anchor_type.delete(0,tk.END)
                   self.txt_found_name.delete(0,tk.END)
                   self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                   self.txt_exc_depth.insert(tk.END,selected_ind_found[0][2])
                   self.txt_strfill.insert(tk.END,selected_ind_found[0][3])
                   self.txt_foundation_depth.insert(tk.END,selected_ind_found[0][4])
                   self.txt_foundation_d1.insert(tk.END,selected_ind_found[0][5])
                   self.txt_foundation_d2.insert(tk.END,selected_ind_found[0][6])
                   self.combo_anchor_type.set(selected_ind_found[0][7])
                   self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][8])
                   self.txt_grouting_depth1.insert(tk.END,selected_ind_found[0][9])
                   self.txt_p1_width.insert(tk.END,selected_ind_found[0][10])
                   self.txt_p1_length.insert(tk.END,selected_ind_found[0][11])
                   self.txt_p1_depth.insert(tk.END,selected_ind_found[0][12])
                   self.txt_quantity.insert(tk.END,selected_ind_found[0][13])
               except NameError:
                   pass
               except IndexError:
                   pass
       except NameError:
           pass

   def gtFoundation(self):
       print("GT Foundation")
       self.bypass_button.place_forget()
       self.frame_sf.place_forget()
       self.frame_dw.place_forget()
       self.frame1.place(relx=0.01, rely=0.075, relwidth=0.4, relheight=0.5)
       # FRAME 1 WIDGET PLACE
       self.combo_gt_type.place(relx=0.12, rely=0.04, relwidth=0.2, relheight=0.075)
       self.lbl_gt_type.place(relx=0.01, rely=0.04, relwidth=0.1, relheight=0.075)
       # self.rad_50_hz.place(relx=0.45, rely=0.04, relwidth=0.2, relheight=0.1)
       # self.rad_60_hz.place(relx=0.45, rely=0.16, relwidth=0.2, relheight=0.1)
       self.lbl_gtno.place(relx=0.65, rely=0.04, relwidth=0.2, relheight=0.075)
       self.lbl_skid_list.place(relx=0.08, rely=0.4, relwidth=0.5, relheight=0.075)
       self.lbl_skid_used.place(relx=0.74, rely=0.4, relwidth=0.5, relheight=0.075)
       self.combo_gtno.place(relx=0.86, rely=0.04, relwidth=0.12, relheight=0.075)
       self.gtindoor_check.place(relx=0.65, rely=0.12, relwidth=0.25, relheight=0.075)
       self.bypass_check.place(relx=0.65, rely=0.2, relwidth=0.32, relheight=0.075)
       # self.gt_treeview.place(relx=0.01, rely=0.45, relwidth=0.98, relheight=0.55)
       self.aux_list.place(relx=0.01, rely=0.45, relwidth=0.38, relheight=0.54)
       AUXILIARIES = [row[0] for row in db.fetchAuxNames()]
       for aux in AUXILIARIES:
           self.aux_list.insert(END, aux)
       self.aux_list2.place(relx=0.64, rely=0.45, relwidth=0.38, relheight=0.54)
       self.add_aux_button.place(relx=0.41, rely=0.6, relwidth=0.19, relheight=0.1)
       self.remove_aux_button.place(relx=0.41, rely=0.75, relwidth=0.19, relheight=0.1)
       self.bypass_button = ttk.Button(self, text="ADD FOUNDATION", command=self.addGTFoundation, cursor="hand2",style = 'W.TButton')
       self.bypass_button.place(relx=0.42, rely=0.377, relwidth=0.09, relheight=0.05)

   def stFoundation(self):
       print("ST Foundation")
   def combinedFooting(self):
       print("Combined Footing")
       """
              exc_depth
              strfill
              foundation_depth
              foundation_d1
              foundation_d2
              pedestals:
                   pedestal_d1
                   pedestal_d2
                   pedestal_depth
                   pedestal_qty
             anchor
             grouting_depth
              """
       self.frame2.place_forget()
       self.frame1.place_forget()
       self.frame_dw.place_forget()
       self.frame_sf.place(relx=0.01, rely=0.075, relwidth=0.7, relheight=0.5)
       self.bypass_button.place_forget()
       for widgets in self.frame_sf.winfo_children():
           widgets.destroy()
       param_img = found_pic(self.frame_sf)
       param_img.param_type = "cf"
       param_img.open_image()
       param_img.place(relx=0.4, rely=0.116, relwidth=0.6, relheight=0.85)

       self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth:', font=("Pickwick", 8, "bold"))
       self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_depth = ttk.Label(self.frame_sf, text='Foundation Depth:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_d1 = ttk.Label(self.frame_sf, text='Foundation Width:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_d2 = ttk.Label(self.frame_sf, text='Foundation Length:', font=("Pickwick", 8, "bold"))
       self.lbl_p1 = ttk.Label(self.frame_sf, text='Pedestal', font=("Pickwick", 8, "bold"))
       self.lbl_p1_width = ttk.Label(self.frame_sf, text='Pedestal_Width', font=("Pickwick", 8, "bold"))
       self.lbl_p1_length = ttk.Label(self.frame_sf, text='Pedestal_Length', font=("Pickwick", 8, "bold"))
       self.lbl_p1_depth = ttk.Label(self.frame_sf, text='Pedestal_Depth', font=("Pickwick", 8, "bold"))
       self.lbl_grouting_depth1 = ttk.Label(self.frame_sf, text='Grout Depth:', font=("Pickwick", 8, "bold"))

       self.exc_depth = DoubleVar()
       self.strfill = DoubleVar()
       self.foundation_depth = DoubleVar()
       self.foundation_d1 = DoubleVar()
       self.foundation_d2 = DoubleVar()
       self.grouting_depth1 = DoubleVar()
       self.p1_width = DoubleVar()
       self.p1_length = DoubleVar()
       self.p1_depth = DoubleVar()
       self.p1_qty = IntVar()
       self.found_name = StringVar()
       self.quantity = IntVar()
       self.anchor_type = StringVar()
       self.anchor_qty = IntVar()

       self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
       self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
       self.txt_foundation_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_depth)
       self.txt_foundation_d1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_d1)
       self.txt_foundation_d2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_d2)
       self.txt_grouting_depth1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.grouting_depth1)
       self.txt_p1_width = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_width)
       self.txt_p1_length = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_length)
       self.txt_p1_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_depth)


       self.lbl_exc_depth.place(relx=0.01, rely=0.04, relwidth=0.1, relheight=0.075)
       self.lbl_strfill.place(relx=0.01, rely=0.116, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_depth.place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_d1.place(relx=0.01, rely=0.267, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_d2.place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
       self.lbl_grouting_depth1.place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)

       self.txt_exc_depth.place(relx=0.12, rely=0.04, relwidth=0.08, relheight=0.075)
       self.txt_strfill.place(relx=0.12, rely=0.116, relwidth=0.08, relheight=0.075)
       self.txt_foundation_depth.place(relx=0.12, rely=0.191, relwidth=0.08, relheight=0.075)
       self.txt_foundation_d1.place(relx=0.12, rely=0.267, relwidth=0.08, relheight=0.075)
       self.txt_foundation_d2.place(relx=0.12, rely=0.343, relwidth=0.08, relheight=0.075)
       self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
       self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
       self.txt_anchor_qty.place(relx=0.12, rely=0.495, relwidth=0.08, relheight=0.075)
       self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.23,rely=0.495,relwidth=0.1,relheight=0.075)
       self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
       self.combo_anchor_type['values'] = ("M24", "M30", "M36", "M42")
       self.combo_anchor_type.set(f'{self.anchor_type.get()}')
       self.combo_anchor_type.place(relx=0.34, rely=0.495, relwidth=0.05, relheight=0.075)
       self.txt_grouting_depth1.place(relx=0.12, rely=0.419, relwidth=0.08, relheight=0.075)

       self.lbl_p1_width.place(relx=0.23, rely=0.191, relwidth=0.1, relheight=0.075)
       self.txt_p1_width.place(relx=0.34, rely=0.191, relwidth=0.05, relheight=0.075)
       self.lbl_p1_length.place(relx=0.23, rely=0.267, relwidth=0.1, relheight=0.075)
       self.txt_p1_length.place(relx=0.34, rely=0.267, relwidth=0.05, relheight=0.075)
       self.lbl_p1_depth.place(relx=0.23, rely=0.343, relwidth=0.1, relheight=0.075)
       self.txt_p1_depth.place(relx=0.34, rely=0.343, relwidth=0.05, relheight=0.075)
       self.lbl_p1_qty = ttk.Label(self.frame_sf, text='Pedestal_Qty', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.419, relwidth=0.1, relheight=0.075)
       self.txt_p1_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.p1_qty)
       self.txt_p1_qty.place(relx=0.34, rely=0.419, relwidth=0.04, relheight=0.075)

       self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.23,
                                                                                                             rely=0.04,
                                                                                                             relwidth=0.1,
                                                                                                             relheight=0.075)
       self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
       self.txt_found_name.place(relx=0.34, rely=0.04,relwidth=0.25,relheight=0.075)
       self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.116, relwidth=0.1, relheight=0.075)
       self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
       self.txt_quantity.place(relx=0.34, rely=0.116, relwidth=0.05, relheight=0.075)

       self.bypass_button = ttk.Button(self, text="ADD FOUNDATION", command=self.addCombinedFooting, cursor="hand2",
                                       style='W.TButton')
       self.bypass_button.place(relx=0.72, rely=0.377, relwidth=0.09, relheight=0.05)

       try:
           if selected_item[1] == "COMBINED FOOTING":
               try:
                   self.txt_exc_depth.delete(0,tk.END)
                   self.txt_strfill.delete(0,tk.END)
                   self.txt_foundation_depth.delete(0,tk.END)
                   self.txt_foundation_d1.delete(0,tk.END)
                   self.txt_foundation_d2.delete(0,tk.END)
                   self.txt_anchor_qty.delete(0,tk.END)
                   self.txt_grouting_depth1.delete(0,tk.END)
                   self.txt_quantity.delete(0,tk.END)
                   self.txt_p1_width.delete(0,tk.END)
                   self.txt_p1_length.delete(0,tk.END)
                   self.txt_p1_depth.delete(0,tk.END)
                   self.combo_anchor_type.delete(0,tk.END)
                   self.txt_found_name.delete(0,tk.END)
                   self.txt_p1_qty.delete(0,tk.END)
                   self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                   self.txt_exc_depth.insert(tk.END,selected_ind_found[0][2])
                   self.txt_strfill.insert(tk.END,selected_ind_found[0][3])
                   self.txt_foundation_depth.insert(tk.END,selected_ind_found[0][4])
                   self.txt_foundation_d1.insert(tk.END,selected_ind_found[0][5])
                   self.txt_foundation_d2.insert(tk.END,selected_ind_found[0][6])
                   self.combo_anchor_type.set(selected_ind_found[0][7])
                   self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][8])
                   self.txt_grouting_depth1.insert(tk.END,selected_ind_found[0][9])
                   self.txt_p1_width.insert(tk.END,selected_ind_found[0][10])
                   self.txt_p1_length.insert(tk.END,selected_ind_found[0][11])
                   self.txt_p1_depth.insert(tk.END,selected_ind_found[0][12])
                   self.txt_p1_qty.insert(tk.END,selected_ind_found[0][13])
                   self.txt_quantity.insert(tk.END,selected_ind_found[0][14])
               except NameError:
                   pass
               except IndexError:
                   pass
       except NameError:
           pass

   def matFoundation(self):
       print("Mat Foundation")
       """
              exc_depth
              strfill
              foundation_depth
              foundation_d1
              foundation_d2
              pedestals:
                   pedestal_d1
                   pedestal_d2
                   pedestal_depth
                   pedestal_qty
             anchor
             grouting_depth
              """
       self.frame2.place_forget()
       self.frame1.place_forget()
       self.frame_dw.place_forget()
       self.frame_sf.place(relx=0.01, rely=0.075, relwidth=0.7, relheight=0.5)
       self.bypass_button.place_forget()
       for widgets in self.frame_sf.winfo_children():
           widgets.destroy()
       param_img = found_pic(self.frame_sf)
       param_img.param_type = "mat_found"
       param_img.open_image()
       param_img.place(relx=0.4, rely=0.116, relwidth=0.6, relheight=0.8)
       self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth:', font=("Pickwick", 8, "bold"))
       self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_depth = ttk.Label(self.frame_sf, text='Foundation Depth:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_d1 = ttk.Label(self.frame_sf, text='Foundation Width:', font=("Pickwick", 8, "bold"))
       self.lbl_foundation_d2 = ttk.Label(self.frame_sf, text='Foundation Length:', font=("Pickwick", 8, "bold"))
       self.lbl_grouting_depth1 = ttk.Label(self.frame_sf, text='Grout Depth:', font=("Pickwick", 8, "bold"))

       self.exc_depth = DoubleVar()
       self.strfill = DoubleVar()
       self.foundation_depth = DoubleVar()
       self.foundation_d1 = DoubleVar()
       self.foundation_d2 = DoubleVar()
       self.grouting_depth1 = DoubleVar()
       self.p1_width = DoubleVar()
       self.p1_length = DoubleVar()
       self.p1_depth = DoubleVar()
       self.p1_qty = IntVar()
       self.found_name = StringVar()
       self.quantity = IntVar()
       self.anchor_qty = IntVar()
       self.anchor_type = StringVar()

       self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
       self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
       self.txt_foundation_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_depth)
       self.txt_foundation_d1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_d1)
       self.txt_foundation_d2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.foundation_d2)
       self.txt_grouting_depth1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.grouting_depth1)

       self.lbl_exc_depth.place(relx=0.01, rely=0.04, relwidth=0.1, relheight=0.075)
       self.lbl_strfill.place(relx=0.01, rely=0.116, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_depth.place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_d1.place(relx=0.01, rely=0.267, relwidth=0.1, relheight=0.075)
       self.lbl_foundation_d2.place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
       self.lbl_grouting_depth1.place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)

       self.txt_exc_depth.place(relx=0.12, rely=0.04, relwidth=0.08, relheight=0.075)
       self.txt_strfill.place(relx=0.12, rely=0.116, relwidth=0.08, relheight=0.075)
       self.txt_foundation_depth.place(relx=0.12, rely=0.191, relwidth=0.08, relheight=0.075)
       self.txt_foundation_d1.place(relx=0.12, rely=0.267, relwidth=0.08, relheight=0.075)
       self.txt_foundation_d2.place(relx=0.12, rely=0.343, relwidth=0.08, relheight=0.075)
       self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
       self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
       self.txt_anchor_qty.place(relx=0.12, rely=0.419, relwidth=0.08, relheight=0.075)
       self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.23,rely=0.419,relwidth=0.1,relheight=0.075)
       self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
       self.combo_anchor_type['values'] = ("M24", "M30", "M36", "M42")
       self.combo_anchor_type.set(f'{self.anchor_type.get()}')
       self.combo_anchor_type.place(relx=0.34, rely=0.419, relwidth=0.05, relheight=0.075)
       self.txt_grouting_depth1.place(relx=0.12, rely=0.495, relwidth=0.08, relheight=0.075)

       self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.23,
                                                                                                             rely=0.04,
                                                                                                             relwidth=0.1,
                                                                                                             relheight=0.075)
       self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
       self.txt_found_name.place(relx=0.34, rely=0.04,relwidth=0.25,relheight=0.075)
       self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.116, relwidth=0.1, relheight=0.075)
       self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
       self.txt_quantity.place(relx=0.34, rely=0.116, relwidth=0.05, relheight=0.075)

       self.bypass_button = ttk.Button(self, text="ADD FOUNDATION", command=self.addMatFoundation, cursor="hand2",style='W.TButton')
       self.bypass_button.place(relx=0.72, rely=0.377, relwidth=0.09, relheight=0.05)

       try:
           if selected_item[1] == "MAT FOUNDATION":
               try:
                   self.txt_exc_depth.delete(0,tk.END)
                   self.txt_strfill.delete(0,tk.END)
                   self.txt_foundation_depth.delete(0,tk.END)
                   self.txt_foundation_d1.delete(0,tk.END)
                   self.txt_foundation_d2.delete(0,tk.END)
                   self.txt_grouting_depth1.delete(0,tk.END)
                   self.txt_anchor_qty.delete(0,tk.END)
                   self.txt_quantity.delete(0,tk.END)
                   self.combo_anchor_type.delete(0,tk.END)
                   self.txt_found_name.delete(0,tk.END)
                   self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                   self.txt_exc_depth.insert(tk.END,selected_ind_found[0][2])
                   self.txt_strfill.insert(tk.END,selected_ind_found[0][3])
                   self.txt_foundation_depth.insert(tk.END,selected_ind_found[0][4])
                   self.txt_foundation_d1.insert(tk.END,selected_ind_found[0][5])
                   self.txt_foundation_d2.insert(tk.END,selected_ind_found[0][6])
                   self.combo_anchor_type.set(selected_ind_found[0][7])
                   self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][8])
                   self.txt_grouting_depth1.insert(tk.END,selected_ind_found[0][9])
                   self.txt_quantity.insert(tk.END,selected_ind_found[0][10])
               except NameError:
                   pass
               except IndexError:
                   pass
       except NameError:
           pass

   def tankFoundation(self):
       def addCommonWidgets():
           self.combo_tank_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.tank_type, state='readonly')
           self.combo_tank_type.place(relx=0.12, rely=0.04, relwidth=0.15, relheight=0.075)
           self.lbl_tank_type = ttk.Label(self.frame_sf, text='TANK TYPE', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.04, relwidth=0.1, relheight=0.075)
           self.combo_tank_type['values'] = ("CYLINDER","OCTAGON","OCTAGON(SQUARE_BASE)","HEXAGON","HEXAGON(SQUARE_BASE)")
           self.combo_tank_type.set(f'{self.tank_type.get()}')
           self.combo_tank_type.bind("<<ComboboxSelected>>", tank_selection)
           self.ischemical = ttk.Checkbutton(self.frame_sf, text='Is Chemical?', variable=self.chemical,onvalue=1, offvalue=0)
           self.ischemical.place(relx=0.01, rely=0.12, relwidth=0.1, relheight=0.075)
           #self.isdykewall.place(relx=0.01, rely=0.85, relwidth=0.2, relheight=0.075)

           self.bypass_button = ttk.Button(self.frame_sf, text="ADD TANK", command=self.addTankFoundation, cursor="hand2",style='W.TButton')
           self.bypass_button.place(relx=0.22, rely=0.85, relwidth=0.09, relheight=0.075)


           self.lbl_dw = ttk.Label(self.frame_sf, text='DYKE WALL DIMENSIONS', font=("Pickwick", 8, "bold"))
           self.lbl_dw_thk = ttk.Label(self.frame_sf, text='DW Thickness:', font=("Pickwick", 8, "bold"))
           self.lbl_dw_height = ttk.Label(self.frame_sf, text='DW Height:', font=("Pickwick", 8, "bold"))
           self.lbl_dw_perimeter_width = ttk.Label(self.frame_sf, text='DW Perimeter Width:', font=("Pickwick", 8, "bold"))
           self.lbl_dw_perimeter_length = ttk.Label(self.frame_sf, text='DW Perimeter Length:',font=("Pickwick", 8, "bold"))
           self.lbl_dw_foundation_depth = ttk.Label(self.frame_sf, text='DW Foundation Depth:',font=("Pickwick", 8, "bold"))
           self.lbl_dw_foundation_width = ttk.Label(self.frame_sf, text='DW Foundation Width:',font=("Pickwick", 8, "bold"))

           self.txt_dw_thk = ttk.Entry(self.frame_sf, width=5, textvariable=self.dyke_wall_thk)
           self.txt_dw_height = ttk.Entry(self.frame_sf, width=5, textvariable=self.dyke_wall_height)
           self.txt_perimeter_width = ttk.Entry(self.frame_sf, width=5, textvariable=self.dw_width)
           self.txt_perimeter_length = ttk.Entry(self.frame_sf, width=5, textvariable=self.dw_length)
           self.txt_foundation_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.dw_found_depth)
           self.txt_foundation_width = ttk.Entry(self.frame_sf, width=5, textvariable=self.dw_found_width)

       def tank_selection(event):
           if self.tank_type.get() == "CYLINDER":
               print("CYLINDER")

               self.R1 = DoubleVar()
               self.R2 = DoubleVar()
               self.a = DoubleVar()
               self.b = DoubleVar()
               self.c = DoubleVar()
               self.d = DoubleVar()
               self.e = DoubleVar()
               self.exc_depth = DoubleVar()
               self.tank_height = DoubleVar()
               self.strfill = DoubleVar()
               self.quantity = IntVar()
               self.found_name = StringVar()
               self.anchor_qty = IntVar()
               self.anchor_type = StringVar()

               for widgets in self.frame_sf.winfo_children():
                   widgets.destroy()

               param_img = found_pic(self.frame_sf)
               param_img.param_type = "cylinder_tank"
               param_img.open_image()
               param_img.place(relx=0.4, rely=0.12, relwidth=0.6, relheight=0.85)

               addCommonWidgets()

               self.lbl_r1 = ttk.Label(self.frame_sf, text='D1:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_r1 = ttk.Label(self.frame_sf, text='D1:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_r2 = ttk.Label(self.frame_sf, text='D2:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.27, relwidth=0.1, relheight=0.075)
               self.lbl_a = ttk.Label(self.frame_sf, text='Dimension a:',font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
               self.lbl_b = ttk.Label(self.frame_sf, text='Dimension b:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
               self.lbl_c = ttk.Label(self.frame_sf, text='Dimension c:',font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
               self.lbl_d = ttk.Label(self.frame_sf, text='Dimension d:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.58, relwidth=0.1, relheight=0.075)
               self.lbl_e = ttk.Label(self.frame_sf, text='Dimension e', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.656, relwidth=0.1, relheight=0.075)
               self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.732, relwidth=0.1, relheight=0.075)
               self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.808, relwidth=0.1, relheight=0.075)
               self.lbl_tank_height = ttk.Label(self.frame_sf, text='Tank Height', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.884, relwidth=0.1, relheight=0.075)



               self.txt_r1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.R1)
               self.txt_r1.place(relx=0.12, rely=0.191, relwidth=0.05, relheight=0.075)
               self.txt_r2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.R2)
               self.txt_r2.place(relx=0.12, rely=0.27, relwidth=0.05, relheight=0.075)
               self.txt_a = ttk.Entry(self.frame_sf, width=5, textvariable=self.a)
               self.txt_a.place(relx=0.12, rely=0.348, relwidth=0.05, relheight=0.075)
               self.txt_b = ttk.Entry(self.frame_sf, width=5, textvariable=self.b)
               self.txt_b.place(relx=0.12, rely=0.424, relwidth=0.05, relheight=0.075)
               self.txt_c = ttk.Entry(self.frame_sf, width=5, textvariable=self.c)
               self.txt_c.place(relx=0.12, rely=0.5, relwidth=0.05, relheight=0.075)
               self.txt_d = ttk.Entry(self.frame_sf, width=5, textvariable=self.d)
               self.txt_d.place(relx=0.12, rely=0.58, relwidth=0.05, relheight=0.075)
               self.txt_e = ttk.Entry(self.frame_sf, width=5, textvariable=self.e)
               self.txt_e.place(relx=0.12, rely=0.656, relwidth=0.05, relheight=0.075)
               self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
               self.txt_exc_depth.place(relx=0.12, rely=0.732, relwidth=0.05, relheight=0.075)
               self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
               self.txt_strfill.place(relx=0.12, rely=0.808, relwidth=0.05, relheight=0.075)
               self.txt_tank_height = ttk.Entry(self.frame_sf, width=5, textvariable=self.tank_height)
               self.txt_tank_height.place(relx=0.12, rely=0.884, relwidth=0.05, relheight=0.075)

               self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.28,rely=0.04,relwidth=0.1,relheight=0.075)
               self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
               self.txt_found_name.place(relx=0.36, rely=0.04,relwidth=0.25,relheight=0.075)
               self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.12, rely=0.116, relwidth=0.1, relheight=0.075)
               self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
               self.txt_quantity.place(relx=0.22, rely=0.116, relwidth=0.05, relheight=0.075)

               self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
               self.combo_anchor_type['values'] = ("M24","M30","M36","M42")
               self.combo_anchor_type.set(f'{self.anchor_type.get()}')
               self.combo_anchor_type.place(relx=0.31,rely=0.191,relwidth=0.07,relheight=0.075)
               self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.27, relwidth=0.1, relheight=0.075)
               self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
               self.txt_anchor_qty.place(relx=0.31, rely=0.27, relwidth=0.07, relheight=0.075)

               try:
                   if selected_item[1] == "CYLINDER TANK":
                       try:
                           self.txt_found_name.delete(0,tk.END)
                           self.txt_r1.delete(0,tk.END)
                           self.txt_r2.delete(0,tk.END)
                           self.txt_a.delete(0,tk.END)
                           self.txt_b.delete(0,tk.END)
                           self.txt_c.delete(0,tk.END)
                           self.txt_d.delete(0,tk.END)
                           self.txt_e.delete(0,tk.END)
                           self.txt_exc_depth.delete(0,tk.END)
                           self.txt_strfill.delete(0,tk.END)
                           self.txt_tank_height.delete(0,tk.END)
                           self.combo_anchor_type.delete(0,tk.END)
                           self.txt_anchor_qty.delete(0,tk.END)
                           self.txt_quantity.delete(0,tk.END)
                           self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                           self.chemical.set(selected_ind_found[0][3])
                           self.txt_r1.insert(tk.END,selected_ind_found[0][4])
                           self.txt_r2.insert(tk.END,selected_ind_found[0][5])
                           self.txt_a.insert(tk.END,selected_ind_found[0][6])
                           self.txt_b.insert(tk.END,selected_ind_found[0][7])
                           self.txt_c.insert(tk.END,selected_ind_found[0][8])
                           self.txt_d.insert(tk.END,selected_ind_found[0][9])
                           self.txt_e.insert(tk.END,selected_ind_found[0][10])
                           self.txt_exc_depth.insert(tk.END,selected_ind_found[0][11])
                           self.txt_strfill.insert(tk.END,selected_ind_found[0][12])
                           self.txt_tank_height.insert(tk.END,selected_ind_found[0][13])
                           self.combo_anchor_type.set(selected_ind_found[0][14])
                           self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][15])
                           self.txt_quantity.insert(tk.END,selected_ind_found[0][16])
                       except NameError:
                           pass
                       except IndexError:
                           pass
               except NameError:
                   pass
           elif self.tank_type.get() == "HEXAGON":
               print("HEXAGON")

               self.D1 = DoubleVar()
               self.D2 = DoubleVar()
               self.a = DoubleVar()
               self.b = DoubleVar()
               self.exc_depth = DoubleVar()
               self.tank_height = DoubleVar()
               self.strfill = DoubleVar()
               self.found_name = StringVar()
               self.quantity = IntVar()
               self.anchor_qty = IntVar()
               self.anchor_type = StringVar()

               for widgets in self.frame_sf.winfo_children():
                   widgets.destroy()

               param_img = found_pic(self.frame_sf)
               param_img.param_type = "hexagon_tank"
               param_img.open_image()
               param_img.place(relx=0.4, rely=0.12, relwidth=0.6, relheight=0.85)

               addCommonWidgets()

               self.lbl_D1 = ttk.Label(self.frame_sf, text='D1:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_D2 = ttk.Label(self.frame_sf, text='D2:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.26, relwidth=0.1, relheight=0.075)
               self.lbl_a = ttk.Label(self.frame_sf, text='Dimension a:',font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
               self.lbl_b = ttk.Label(self.frame_sf, text='Dimension b:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
               self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
               self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.561, relwidth=0.1, relheight=0.075)
               self.lbl_tank_height = ttk.Label(self.frame_sf, text='Tank Height', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.637, relwidth=0.1, relheight=0.075)

               self.txt_D1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D1)
               self.txt_D1.place(relx=0.12, rely=0.191, relwidth=0.05, relheight=0.075)
               self.txt_D2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D2)
               self.txt_D2.place(relx=0.12, rely=0.26, relwidth=0.05, relheight=0.075)
               self.txt_a = ttk.Entry(self.frame_sf, width=5, textvariable=self.a)
               self.txt_a.place(relx=0.12, rely=0.343, relwidth=0.05, relheight=0.075)
               self.txt_b = ttk.Entry(self.frame_sf, width=5, textvariable=self.b)
               self.txt_b.place(relx=0.12, rely=0.419, relwidth=0.05, relheight=0.075)
               self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
               self.txt_exc_depth.place(relx=0.12, rely=0.495, relwidth=0.05, relheight=0.075)
               self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
               self.txt_strfill.place(relx=0.12, rely=0.561, relwidth=0.05, relheight=0.075)
               self.txt_tank_height = ttk.Entry(self.frame_sf, width=5, textvariable=self.tank_height)
               self.txt_tank_height.place(relx=0.12, rely=0.637, relwidth=0.05, relheight=0.075)

               self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.28,rely=0.04,relwidth=0.1,relheight=0.075)
               self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
               self.txt_found_name.place(relx=0.36, rely=0.04,relwidth=0.25,relheight=0.075)
               self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.12, rely=0.116, relwidth=0.1, relheight=0.075)
               self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
               self.txt_quantity.place(relx=0.22, rely=0.116, relwidth=0.05, relheight=0.075)


               self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
               self.combo_anchor_type['values'] = ("M24","M30","M36","M42")
               self.combo_anchor_type.set(f'{self.anchor_type.get()}')
               self.combo_anchor_type.place(relx=0.31,rely=0.191,relwidth=0.07,relheight=0.075)
               self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.27, relwidth=0.1, relheight=0.075)
               self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
               self.txt_anchor_qty.place(relx=0.31, rely=0.27, relwidth=0.07, relheight=0.075)

               try:
                   if selected_item[1] == "HEXAGON TANK":
                       try:
                           self.txt_found_name.delete(0,tk.END)
                           self.txt_D1.delete(0,tk.END)
                           self.txt_D2.delete(0,tk.END)
                           self.txt_a.delete(0,tk.END)
                           self.txt_b.delete(0,tk.END)
                           self.txt_exc_depth.delete(0,tk.END)
                           self.txt_strfill.delete(0,tk.END)
                           self.txt_tank_height.delete(0,tk.END)
                           self.combo_anchor_type.delete(0,tk.END)
                           self.txt_anchor_qty.delete(0,tk.END)
                           self.txt_quantity.delete(0,tk.END)
                           self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                           self.chemical.set(selected_ind_found[0][3])
                           self.txt_D1.insert(tk.END,selected_ind_found[0][4])
                           self.txt_D2.insert(tk.END,selected_ind_found[0][5])
                           self.txt_a.insert(tk.END,selected_ind_found[0][6])
                           self.txt_b.insert(tk.END,selected_ind_found[0][7])
                           self.txt_exc_depth.insert(tk.END,selected_ind_found[0][11])
                           self.txt_strfill.insert(tk.END,selected_ind_found[0][12])
                           self.txt_tank_height.insert(tk.END,selected_ind_found[0][13])
                           self.combo_anchor_type.set(selected_ind_found[0][14])
                           self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][15])
                           self.txt_quantity.insert(tk.END,selected_ind_found[0][16])
                       except NameError:
                           pass
                       except IndexError:
                           pass
               except NameError:
                   pass
           elif self.tank_type.get() == "HEXAGON(SQUARE_BASE)":
               print("HEXAGON(SQUARE_BASE)")

               self.D1 = DoubleVar()
               self.D2 = DoubleVar()
               self.a = DoubleVar()
               self.b = DoubleVar()
               self.exc_depth = DoubleVar()
               self.tank_height = DoubleVar()
               self.strfill = DoubleVar()
               self.found_name = StringVar()
               self.quantity = IntVar()
               self.anchor_qty = IntVar()
               self.anchor_type = StringVar()

               for widgets in self.frame_sf.winfo_children():
                   widgets.destroy()

               param_img = found_pic(self.frame_sf)
               param_img.param_type = "hexagon_square_base_tank"
               param_img.open_image()
               param_img.place(relx=0.4, rely=0.12, relwidth=0.6, relheight=0.85)

               addCommonWidgets()

               self.lbl_D1 = ttk.Label(self.frame_sf, text='D1:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_D2 = ttk.Label(self.frame_sf, text='D2:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.26, relwidth=0.1, relheight=0.075)
               self.lbl_a = ttk.Label(self.frame_sf, text='Dimension a:',font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
               self.lbl_b = ttk.Label(self.frame_sf, text='Dimension b:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
               self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
               self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.561, relwidth=0.1, relheight=0.075)
               self.lbl_tank_height = ttk.Label(self.frame_sf, text='Tank Height', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.637, relwidth=0.1, relheight=0.075)

               self.txt_D1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D1)
               self.txt_D1.place(relx=0.12, rely=0.191, relwidth=0.05, relheight=0.075)
               self.txt_D2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D2)
               self.txt_D2.place(relx=0.12, rely=0.26, relwidth=0.05, relheight=0.075)
               self.txt_a = ttk.Entry(self.frame_sf, width=5, textvariable=self.a)
               self.txt_a.place(relx=0.12, rely=0.343, relwidth=0.05, relheight=0.075)
               self.txt_b = ttk.Entry(self.frame_sf, width=5, textvariable=self.b)
               self.txt_b.place(relx=0.12, rely=0.419, relwidth=0.05, relheight=0.075)
               self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
               self.txt_exc_depth.place(relx=0.12, rely=0.495, relwidth=0.05, relheight=0.075)
               self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
               self.txt_strfill.place(relx=0.12, rely=0.561, relwidth=0.05, relheight=0.075)
               self.txt_tank_height = ttk.Entry(self.frame_sf, width=5, textvariable=self.tank_height)
               self.txt_tank_height.place(relx=0.12, rely=0.637, relwidth=0.05, relheight=0.075)

               self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.28,rely=0.04,relwidth=0.1,relheight=0.075)
               self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
               self.txt_found_name.place(relx=0.36, rely=0.04,relwidth=0.25,relheight=0.075)
               self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.12, rely=0.116, relwidth=0.1, relheight=0.075)
               self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
               self.txt_quantity.place(relx=0.22, rely=0.116, relwidth=0.05, relheight=0.075)


               self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
               self.combo_anchor_type['values'] = ("M24","M30","M36","M42")
               self.combo_anchor_type.set(f'{self.anchor_type.get()}')
               self.combo_anchor_type.place(relx=0.31,rely=0.191,relwidth=0.07,relheight=0.075)
               self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.27, relwidth=0.1, relheight=0.075)
               self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
               self.txt_anchor_qty.place(relx=0.31, rely=0.27, relwidth=0.07, relheight=0.075)

               try:
                   if selected_item[1] == "HEXAGON(SQUARE_BASE) TANK":
                       try:
                           self.txt_found_name.delete(0,tk.END)
                           self.txt_D1.delete(0,tk.END)
                           self.txt_D2.delete(0,tk.END)
                           self.txt_a.delete(0,tk.END)
                           self.txt_b.delete(0,tk.END)
                           self.txt_exc_depth.delete(0,tk.END)
                           self.txt_strfill.delete(0,tk.END)
                           self.txt_tank_height.delete(0,tk.END)
                           self.combo_anchor_type.delete(0,tk.END)
                           self.txt_anchor_qty.delete(0,tk.END)
                           self.txt_quantity.delete(0,tk.END)
                           self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                           self.chemical.set(selected_ind_found[0][3])
                           self.txt_D1.insert(tk.END,selected_ind_found[0][4])
                           self.txt_D2.insert(tk.END,selected_ind_found[0][5])
                           self.txt_a.insert(tk.END,selected_ind_found[0][6])
                           self.txt_b.insert(tk.END,selected_ind_found[0][7])
                           self.txt_exc_depth.insert(tk.END,selected_ind_found[0][11])
                           self.txt_strfill.insert(tk.END,selected_ind_found[0][12])
                           self.txt_tank_height.insert(tk.END,selected_ind_found[0][13])
                           self.combo_anchor_type.set(selected_ind_found[0][14])
                           self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][15])
                           self.txt_quantity.insert(tk.END,selected_ind_found[0][16])
                       except NameError:
                           pass
                       except IndexError:
                           pass
               except NameError:
                   pass
           elif self.tank_type.get() == "OCTAGON":
               print("OCTAGON")

               self.D1 = DoubleVar()
               self.D2 = DoubleVar()
               self.a = DoubleVar()
               self.b = DoubleVar()
               self.exc_depth = DoubleVar()
               self.tank_height = DoubleVar()
               self.strfill = DoubleVar()
               self.found_name = StringVar()
               self.quantity = IntVar()
               self.anchor_qty = IntVar()
               self.anchor_type = StringVar()

               for widgets in self.frame_sf.winfo_children():
                   widgets.destroy()

               param_img = found_pic(self.frame_sf)
               param_img.param_type = "octagon_tank"
               param_img.open_image()
               param_img.place(relx=0.4, rely=0.12, relwidth=0.6, relheight=0.85)

               addCommonWidgets()

               self.lbl_D1 = ttk.Label(self.frame_sf, text='D1:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_D2 = ttk.Label(self.frame_sf, text='D2:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.26, relwidth=0.1, relheight=0.075)
               self.lbl_a = ttk.Label(self.frame_sf, text='Dimension a:',font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
               self.lbl_b = ttk.Label(self.frame_sf, text='Dimension b:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
               self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
               self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.561, relwidth=0.1, relheight=0.075)
               self.lbl_tank_height = ttk.Label(self.frame_sf, text='Tank Height', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.637, relwidth=0.1, relheight=0.075)

               self.txt_D1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D1)
               self.txt_D1.place(relx=0.12, rely=0.191, relwidth=0.05, relheight=0.075)
               self.txt_D2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D2)
               self.txt_D2.place(relx=0.12, rely=0.26, relwidth=0.05, relheight=0.075)
               self.txt_a = ttk.Entry(self.frame_sf, width=5, textvariable=self.a)
               self.txt_a.place(relx=0.12, rely=0.343, relwidth=0.05, relheight=0.075)
               self.txt_b = ttk.Entry(self.frame_sf, width=5, textvariable=self.b)
               self.txt_b.place(relx=0.12, rely=0.419, relwidth=0.05, relheight=0.075)
               self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
               self.txt_exc_depth.place(relx=0.12, rely=0.495, relwidth=0.05, relheight=0.075)
               self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
               self.txt_strfill.place(relx=0.12, rely=0.561, relwidth=0.05, relheight=0.075)
               self.txt_tank_height = ttk.Entry(self.frame_sf, width=5, textvariable=self.tank_height)
               self.txt_tank_height.place(relx=0.12, rely=0.637, relwidth=0.05, relheight=0.075)

               self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.28,rely=0.04,relwidth=0.1,relheight=0.075)
               self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
               self.txt_found_name.place(relx=0.36, rely=0.04,relwidth=0.25,relheight=0.075)
               self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.12, rely=0.116, relwidth=0.1, relheight=0.075)
               self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
               self.txt_quantity.place(relx=0.22, rely=0.116, relwidth=0.05, relheight=0.075)


               self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
               self.combo_anchor_type['values'] = ("M24","M30","M36","M42")
               self.combo_anchor_type.set(f'{self.anchor_type.get()}')
               self.combo_anchor_type.place(relx=0.31,rely=0.191,relwidth=0.07,relheight=0.075)
               self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.27, relwidth=0.1, relheight=0.075)
               self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
               self.txt_anchor_qty.place(relx=0.31, rely=0.27, relwidth=0.07, relheight=0.075)

               try:
                   if selected_item[1] == "OCTAGON TANK":
                       try:
                           self.txt_found_name.delete(0,tk.END)
                           self.txt_D1.delete(0,tk.END)
                           self.txt_D2.delete(0,tk.END)
                           self.txt_a.delete(0,tk.END)
                           self.txt_b.delete(0,tk.END)
                           self.txt_exc_depth.delete(0,tk.END)
                           self.txt_strfill.delete(0,tk.END)
                           self.txt_tank_height.delete(0,tk.END)
                           self.combo_anchor_type.delete(0,tk.END)
                           self.txt_anchor_qty.delete(0,tk.END)
                           self.txt_quantity.delete(0,tk.END)
                           self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                           self.chemical.set(selected_ind_found[0][3])
                           self.txt_D1.insert(tk.END,selected_ind_found[0][4])
                           self.txt_D2.insert(tk.END,selected_ind_found[0][5])
                           self.txt_a.insert(tk.END,selected_ind_found[0][6])
                           self.txt_b.insert(tk.END,selected_ind_found[0][7])
                           self.txt_exc_depth.insert(tk.END,selected_ind_found[0][11])
                           self.txt_strfill.insert(tk.END,selected_ind_found[0][12])
                           self.txt_tank_height.insert(tk.END,selected_ind_found[0][13])
                           self.combo_anchor_type.set(selected_ind_found[0][14])
                           self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][15])
                           self.txt_quantity.insert(tk.END,selected_ind_found[0][16])
                       except NameError:
                           pass
                       except IndexError:
                           pass
               except NameError:
                   pass
           elif self.tank_type.get() == "OCTAGON(SQUARE_BASE)":
               print("OCTAGON(SQUARE_BASE)")

               self.D1 = DoubleVar()
               self.D2 = DoubleVar()
               self.a = DoubleVar()
               self.b = DoubleVar()
               self.exc_depth = DoubleVar()
               self.tank_height = DoubleVar()
               self.strfill = DoubleVar()
               self.found_name = StringVar()
               self.quantity = IntVar()
               self.anchor_qty = IntVar()
               self.anchor_type = StringVar()

               for widgets in self.frame_sf.winfo_children():
                   widgets.destroy()

               param_img = found_pic(self.frame_sf)
               param_img.param_type = "octagon_square_base_tank"
               param_img.open_image()
               param_img.place(relx=0.4, rely=0.12, relwidth=0.6, relheight=0.85)

               addCommonWidgets()

               self.lbl_D1 = ttk.Label(self.frame_sf, text='D1:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_D2 = ttk.Label(self.frame_sf, text='D2:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.26, relwidth=0.1, relheight=0.075)
               self.lbl_a = ttk.Label(self.frame_sf, text='Dimension a:',font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
               self.lbl_b = ttk.Label(self.frame_sf, text='Dimension b:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
               self.lbl_exc_depth = ttk.Label(self.frame_sf, text='Excavation Depth', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
               self.lbl_strfill = ttk.Label(self.frame_sf, text='Structural Fill', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.561, relwidth=0.1, relheight=0.075)
               self.lbl_tank_height = ttk.Label(self.frame_sf, text='Tank Height', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.637, relwidth=0.1, relheight=0.075)

               self.txt_D1 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D1)
               self.txt_D1.place(relx=0.12, rely=0.191, relwidth=0.05, relheight=0.075)
               self.txt_D2 = ttk.Entry(self.frame_sf, width=5, textvariable=self.D2)
               self.txt_D2.place(relx=0.12, rely=0.26, relwidth=0.05, relheight=0.075)
               self.txt_a = ttk.Entry(self.frame_sf, width=5, textvariable=self.a)
               self.txt_a.place(relx=0.12, rely=0.343, relwidth=0.05, relheight=0.075)
               self.txt_b = ttk.Entry(self.frame_sf, width=5, textvariable=self.b)
               self.txt_b.place(relx=0.12, rely=0.419, relwidth=0.05, relheight=0.075)
               self.txt_exc_depth = ttk.Entry(self.frame_sf, width=5, textvariable=self.exc_depth)
               self.txt_exc_depth.place(relx=0.12, rely=0.495, relwidth=0.05, relheight=0.075)
               self.txt_strfill = ttk.Entry(self.frame_sf, width=5, textvariable=self.strfill)
               self.txt_strfill.place(relx=0.12, rely=0.561, relwidth=0.05, relheight=0.075)
               self.txt_tank_height = ttk.Entry(self.frame_sf, width=5, textvariable=self.tank_height)
               self.txt_tank_height.place(relx=0.12, rely=0.637, relwidth=0.05, relheight=0.075)

               self.lbl_found_name = ttk.Label(self.frame_sf, text='Found_Name', font=("Pickwick", 8, "bold")).place(relx=0.28,rely=0.04,relwidth=0.1,relheight=0.075)
               self.txt_found_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
               self.txt_found_name.place(relx=0.36, rely=0.04,relwidth=0.25,relheight=0.075)
               self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.12, rely=0.116, relwidth=0.1, relheight=0.075)
               self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
               self.txt_quantity.place(relx=0.22, rely=0.116, relwidth=0.05, relheight=0.075)


               self.combo_anchor_type = ttk.Combobox(self.frame_sf, width=27, textvariable=self.anchor_type, state='readonly')
               self.combo_anchor_type['values'] = ("M24","M30","M36","M42")
               self.combo_anchor_type.set(f'{self.anchor_type.get()}')
               self.combo_anchor_type.place(relx=0.31,rely=0.191,relwidth=0.07,relheight=0.075)
               self.lbl_anchor_type = ttk.Label(self.frame_sf, text='Anchor_Type', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.191, relwidth=0.1, relheight=0.075)
               self.lbl_anchor_qty = ttk.Label(self.frame_sf, text='Anchor_Qty', font=("Pickwick", 8, "bold")).place(relx=0.2, rely=0.27, relwidth=0.1, relheight=0.075)
               self.txt_anchor_qty = ttk.Entry(self.frame_sf, width=5, textvariable=self.anchor_qty)
               self.txt_anchor_qty.place(relx=0.31, rely=0.27, relwidth=0.07, relheight=0.075)

               try:
                   if selected_item[1] == "OCTAGON(SQUARE_BASE) TANK":
                       try:
                           self.txt_found_name.delete(0,tk.END)
                           self.txt_D1.delete(0,tk.END)
                           self.txt_D2.delete(0,tk.END)
                           self.txt_a.delete(0,tk.END)
                           self.txt_b.delete(0,tk.END)
                           self.txt_exc_depth.delete(0,tk.END)
                           self.txt_strfill.delete(0,tk.END)
                           self.txt_tank_height.delete(0,tk.END)
                           self.combo_anchor_type.delete(0,tk.END)
                           self.txt_anchor_qty.delete(0,tk.END)
                           self.txt_quantity.delete(0,tk.END)
                           self.txt_found_name.insert(tk.END,selected_ind_found[0][1])
                           self.chemical.set(selected_ind_found[0][3])
                           self.txt_D1.insert(tk.END,selected_ind_found[0][4])
                           self.txt_D2.insert(tk.END,selected_ind_found[0][5])
                           self.txt_a.insert(tk.END,selected_ind_found[0][6])
                           self.txt_b.insert(tk.END,selected_ind_found[0][7])
                           self.txt_exc_depth.insert(tk.END,selected_ind_found[0][11])
                           self.txt_strfill.insert(tk.END,selected_ind_found[0][12])
                           self.txt_tank_height.insert(tk.END,selected_ind_found[0][13])
                           self.combo_anchor_type.set(selected_ind_found[0][14])
                           self.txt_anchor_qty.insert(tk.END,selected_ind_found[0][15])
                           self.txt_quantity.insert(tk.END,selected_ind_found[0][16])
                       except NameError:
                           pass
                       except IndexError:
                           pass
               except NameError:
                   pass

       self.dyke_wall_thk = DoubleVar()
       self.dyke_wall_height = DoubleVar()
       self.dw_width = DoubleVar()
       self.dw_length = DoubleVar()
       self.dw_found_depth = DoubleVar()
       self.dw_found_width = DoubleVar()
       self.dw_exc_depth = DoubleVar()
       self.dw_strfill = DoubleVar()
       self.dyke_wall_thk2 = DoubleVar()
       self.dyke_wall_height2 = DoubleVar()
       self.dw_width2 = DoubleVar()
       self.dw_length2 = DoubleVar()
       self.dw_found_depth2 = DoubleVar()
       self.dw_found_width2 = DoubleVar()
       self.dw_exc_depth2 = DoubleVar()

       print("Tank Foundation")
       self.frame2.place_forget()
       self.frame1.place_forget()
       self.bypass_button.place_forget()
       self.frame_sf.place(relx=0.01, rely=0.075, relwidth=0.655, relheight=0.5)
       for widgets in self.frame_sf.winfo_children():
           widgets.destroy()
       addCommonWidgets()
       self.combo_tank_type.set('')
       for widgets in self.frame_dw.winfo_children():
           widgets.destroy()
       self.frame_dw.place(relx=0.666, rely=0.075, relwidth=0.33, relheight=0.5)

       self.lbl_dw2 = ttk.Label(self.frame_dw, text='DYKE WALL DIMENSIONS', font=("Pickwick", 8, "bold"))
       self.lbl_dw_thk2 = ttk.Label(self.frame_dw, text='DW Thickness:', font=("Pickwick", 8, "bold"))
       self.lbl_dw_height2 = ttk.Label(self.frame_dw, text='DW Height:', font=("Pickwick", 8, "bold"))
       self.lbl_dw_perimeter_width2 = ttk.Label(self.frame_dw, text='DW Perimeter Width:', font=("Pickwick", 8, "bold"))
       self.lbl_dw_perimeter_length2 = ttk.Label(self.frame_dw, text='DW Perimeter Length:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_foundation_depth2 = ttk.Label(self.frame_dw, text='DW Foundation Depth:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_foundation_width2 = ttk.Label(self.frame_dw, text='DW Foundation Width:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_exc_depth = ttk.Label(self.frame_dw, text='DW Excavation Depth:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_strfill = ttk.Label(self.frame_dw, text='DW Structural Fill:',font=("Pickwick", 8, "bold"))
       self.dw_button = ttk.Button(self.frame_dw, text="ADD DW", command=self.addDW, cursor="hand2",style='W.TButton')

       self.txt_dw_thk2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dyke_wall_thk2)
       self.txt_dw_height2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dyke_wall_height2)
       self.txt_perimeter_width2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_width2)
       self.txt_perimeter_length2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_length2)
       self.txt_foundation_depth2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_found_depth2)
       self.txt_foundation_width2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_found_width2)
       self.txt_dw_exc_depth2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_exc_depth2)
       self.txt_dw_strfill2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_strfill)

       self.lbl_dw2.place(relx=0.01, rely=0.04, relwidth=0.3, relheight=0.075)
       self.lbl_dw_thk2.place(relx=0.01, rely=0.116, relwidth=0.25, relheight=0.075)
       self.lbl_dw_height2.place(relx=0.01, rely=0.192, relwidth=0.25, relheight=0.075)
       self.lbl_dw_perimeter_width2.place(relx=0.01, rely=0.268, relwidth=0.25, relheight=0.075)
       self.lbl_dw_perimeter_length2.place(relx=0.01, rely=0.334, relwidth=0.25, relheight=0.075)
       self.lbl_dw_foundation_depth2.place(relx=0.01, rely=0.410, relwidth=0.25, relheight=0.075)
       self.lbl_dw_foundation_width2.place(relx=0.01, rely=0.486, relwidth=0.25, relheight=0.075)
       self.lbl_dw_exc_depth.place(relx=0.01, rely=0.562, relwidth=0.25, relheight=0.075)
       self.lbl_dw_strfill.place(relx=0.01, rely=0.638, relwidth=0.25, relheight=0.075)
       self.dw_button.place(relx=0.01, rely=0.85, relwidth=0.13, relheight=0.075)

       self.txt_dw_thk2.place(relx=0.27, rely=0.116, relwidth=0.05, relheight=0.075)
       self.txt_dw_height2.place(relx=0.27, rely=0.192, relwidth=0.05, relheight=0.075)
       self.txt_perimeter_width2.place(relx=0.27, rely=0.268, relwidth=0.05, relheight=0.075)
       self.txt_perimeter_length2.place(relx=0.27, rely=0.334, relwidth=0.05, relheight=0.075)
       self.txt_foundation_depth2.place(relx=0.27, rely=0.410, relwidth=0.05, relheight=0.075)
       self.txt_foundation_width2.place(relx=0.27, rely=0.486, relwidth=0.05, relheight=0.075)
       self.txt_dw_exc_depth2.place(relx=0.27, rely=0.562, relwidth=0.05, relheight=0.075)
       self.txt_dw_strfill2.place(relx=0.27, rely=0.638, relwidth=0.05, relheight=0.075)

       param_img = found_pic(self.frame_dw)
       param_img.param_type = "dyke_wall"
       param_img.open_image()
       param_img.place(relx=0.35, rely=0.12, relwidth=0.65, relheight=0.85)
       try:
           self.tank_type.set(selected_ind_found[0][2])
           tank_selection(selected_ind_found[0][2])
       except NameError:
           pass


   def dykeWall(self):
       self.frame_sf.place_forget()
       self.frame2.place_forget()
       self.frame1.place_forget()
       self.bypass_button.place_forget()
       for widgets in self.frame_dw.winfo_children():
           widgets.destroy()
       self.frame_dw.place(relx=0.666, rely=0.075, relwidth=0.33, relheight=0.5)

       self.dyke_wall_thk = DoubleVar()
       self.dyke_wall_height = DoubleVar()
       self.dw_width = DoubleVar()
       self.dw_length = DoubleVar()
       self.dw_found_depth = DoubleVar()
       self.dw_found_width = DoubleVar()
       self.dw_exc_depth = DoubleVar()
       self.dw_strfill = DoubleVar()
       self.dyke_wall_thk2 = DoubleVar()
       self.dyke_wall_height2 = DoubleVar()
       self.dw_width2 = DoubleVar()
       self.dw_length2 = DoubleVar()
       self.dw_found_depth2 = DoubleVar()
       self.dw_found_width2 = DoubleVar()
       self.dw_exc_depth2 = DoubleVar()

       self.lbl_dw2 = ttk.Label(self.frame_dw, text='DYKE WALL DIMENSIONS', font=("Pickwick", 8, "bold"))
       self.lbl_dw_thk2 = ttk.Label(self.frame_dw, text='DW Thickness:', font=("Pickwick", 8, "bold"))
       self.lbl_dw_height2 = ttk.Label(self.frame_dw, text='DW Height:', font=("Pickwick", 8, "bold"))
       self.lbl_dw_perimeter_width2 = ttk.Label(self.frame_dw, text='DW Perimeter Width:', font=("Pickwick", 8, "bold"))
       self.lbl_dw_perimeter_length2 = ttk.Label(self.frame_dw, text='DW Perimeter Length:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_foundation_depth2 = ttk.Label(self.frame_dw, text='DW Foundation Depth:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_foundation_width2 = ttk.Label(self.frame_dw, text='DW Foundation Width:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_exc_depth = ttk.Label(self.frame_dw, text='DW Excavation Depth:',font=("Pickwick", 8, "bold"))
       self.lbl_dw_strfill = ttk.Label(self.frame_dw, text='DW Structural Fill:',font=("Pickwick", 8, "bold"))
       self.dw_button = ttk.Button(self.frame_dw, text="ADD DW", command=self.addDW, cursor="hand2",style='W.TButton')

       self.txt_dw_thk2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dyke_wall_thk2)
       self.txt_dw_height2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dyke_wall_height2)
       self.txt_perimeter_width2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_width2)
       self.txt_perimeter_length2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_length2)
       self.txt_foundation_depth2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_found_depth2)
       self.txt_foundation_width2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_found_width2)
       self.txt_dw_exc_depth2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_exc_depth2)
       self.txt_dw_strfill2 = ttk.Entry(self.frame_dw, width=5, textvariable=self.dw_strfill)

       self.lbl_dw2.place(relx=0.01, rely=0.04, relwidth=0.3, relheight=0.075)
       self.lbl_dw_thk2.place(relx=0.01, rely=0.116, relwidth=0.25, relheight=0.075)
       self.lbl_dw_height2.place(relx=0.01, rely=0.192, relwidth=0.25, relheight=0.075)
       self.lbl_dw_perimeter_width2.place(relx=0.01, rely=0.268, relwidth=0.25, relheight=0.075)
       self.lbl_dw_perimeter_length2.place(relx=0.01, rely=0.334, relwidth=0.25, relheight=0.075)
       self.lbl_dw_foundation_depth2.place(relx=0.01, rely=0.410, relwidth=0.25, relheight=0.075)
       self.lbl_dw_foundation_width2.place(relx=0.01, rely=0.486, relwidth=0.25, relheight=0.075)
       self.lbl_dw_exc_depth.place(relx=0.01, rely=0.562, relwidth=0.25, relheight=0.075)
       self.lbl_dw_strfill.place(relx=0.01, rely=0.638, relwidth=0.25, relheight=0.075)
       self.dw_button.place(relx=0.01, rely=0.85, relwidth=0.13, relheight=0.075)

       self.txt_dw_thk2.place(relx=0.27, rely=0.116, relwidth=0.05, relheight=0.075)
       self.txt_dw_height2.place(relx=0.27, rely=0.192, relwidth=0.05, relheight=0.075)
       self.txt_perimeter_width2.place(relx=0.27, rely=0.268, relwidth=0.05, relheight=0.075)
       self.txt_perimeter_length2.place(relx=0.27, rely=0.334, relwidth=0.05, relheight=0.075)
       self.txt_foundation_depth2.place(relx=0.27, rely=0.410, relwidth=0.05, relheight=0.075)
       self.txt_foundation_width2.place(relx=0.27, rely=0.486, relwidth=0.05, relheight=0.075)
       self.txt_dw_exc_depth2.place(relx=0.27, rely=0.562, relwidth=0.05, relheight=0.075)
       self.txt_dw_strfill2.place(relx=0.27, rely=0.638, relwidth=0.05, relheight=0.075)

       param_img = found_pic(self.frame_dw)
       param_img.param_type = "dyke_wall"
       param_img.open_image()
       param_img.place(relx=0.35, rely=0.12, relwidth=0.65, relheight=0.85)

       try:
           if selected_item[1] == "WALL FOUNDATION1":
               try:
                   self.txt_dw_thk2.delete(0,tk.END)
                   self.txt_dw_height2.delete(0,tk.END)
                   self.txt_perimeter_width2.delete(0,tk.END)
                   self.txt_perimeter_length2.delete(0,tk.END)
                   self.txt_foundation_depth2.delete(0,tk.END)
                   self.txt_foundation_width2.delete(0,tk.END)
                   self.txt_dw_exc_depth2.delete(0,tk.END)
                   self.txt_dw_strfill2.delete(0,tk.END)
                   self.txt_dw_thk2.insert(tk.END,selected_ind_found[0][2])
                   self.txt_dw_height2.insert(tk.END,selected_ind_found[0][3])
                   self.txt_perimeter_width2.insert(tk.END,selected_ind_found[0][4])
                   self.txt_perimeter_length2.insert(tk.END,selected_ind_found[0][5])
                   self.txt_foundation_depth2.insert(tk.END,selected_ind_found[0][6])
                   self.txt_foundation_width2.insert(tk.END,selected_ind_found[0][7])
                   self.txt_dw_exc_depth2.insert(tk.END,selected_ind_found[0][8])
                   self.txt_dw_strfill2.insert(tk.END,selected_ind_found[0][9])
               except NameError:
                   pass
               except IndexError:
                   pass
       except NameError:
           pass

   def pitCalculator(self):
       print("Pit Calculator")
       """
              exc_depth
              strfill
              mid_height
              mid_width
              mid_length
              wall_thickness
              bottom_thickness
              top_thickness
              """
       self.frame2.place_forget()
       self.frame1.place_forget()
       self.frame_dw.place_forget()
       self.frame_sf.place(relx=0.01, rely=0.075, relwidth=0.7, relheight=0.5)
       self.bypass_button.place_forget()
       for widgets in self.frame_sf.winfo_children():
           widgets.destroy()
       param_img = found_pic(self.frame_sf)
       param_img.param_type = "pit"
       param_img.open_image()
       param_img.place(relx=0.4, rely=0.116, relwidth=0.6, relheight=0.85)

       self.lbl_a = ttk.Label(self.frame_sf, text='Dimension a:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.04, relwidth=0.1, relheight=0.075)
       self.lbl_b = ttk.Label(self.frame_sf, text='Dimension b:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.116, relwidth=0.1, relheight=0.075)
       self.lbl_c = ttk.Label(self.frame_sf, text='Dimension c:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.191, relwidth=0.1, relheight=0.075)
       self.lbl_d = ttk.Label(self.frame_sf, text='Dimension d:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.267, relwidth=0.1, relheight=0.075)
       self.lbl_e = ttk.Label(self.frame_sf, text='Dimension e:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.343, relwidth=0.1, relheight=0.075)
       self.lbl_f = ttk.Label(self.frame_sf, text='Dimension f:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.419, relwidth=0.1, relheight=0.075)
       self.lbl_g = ttk.Label(self.frame_sf, text='Dimension g:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.495, relwidth=0.1, relheight=0.075)
       self.lbl_h = ttk.Label(self.frame_sf, text='Dimension h:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.571, relwidth=0.1, relheight=0.075)
       self.lbl_k = ttk.Label(self.frame_sf, text='Dimension k:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.647, relwidth=0.1, relheight=0.075)
       self.lbl_fill = ttk.Label(self.frame_sf, text='Structural Fill:', font=("Pickwick", 8, "bold")).place(relx=0.01, rely=0.724, relwidth=0.1, relheight=0.075)

       self.dim_a = DoubleVar()
       self.dim_b = DoubleVar()
       self.dim_c = DoubleVar()
       self.dim_d = DoubleVar()
       self.dim_e = DoubleVar()
       self.dim_f = DoubleVar()
       self.dim_g = DoubleVar()
       self.dim_h = DoubleVar()
       self.dim_k = DoubleVar()
       self.found_name = StringVar()
       self.quantity = IntVar()
       self.fill = DoubleVar()

       self.txt_a = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_a)
       self.txt_a.place(relx=0.12, rely=0.04, relwidth=0.08, relheight=0.075)
       self.txt_b = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_b)
       self.txt_b.place(relx=0.12, rely=0.116, relwidth=0.08, relheight=0.075)
       self.txt_c = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_c)
       self.txt_c.place(relx=0.12, rely=0.191, relwidth=0.08, relheight=0.075)
       self.txt_d = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_d)
       self.txt_d.place(relx=0.12, rely=0.267, relwidth=0.08, relheight=0.075)
       self.txt_e = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_e)
       self.txt_e.place(relx=0.12, rely=0.343, relwidth=0.08, relheight=0.075)
       self.txt_f = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_f)
       self.txt_f.place(relx=0.12, rely=0.419, relwidth=0.08, relheight=0.075)
       self.txt_g = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_g)
       self.txt_g.place(relx=0.12, rely=0.495, relwidth=0.08, relheight=0.075)
       self.txt_h = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_h)
       self.txt_h.place(relx=0.12, rely=0.571, relwidth=0.08, relheight=0.075)
       self.txt_k = ttk.Entry(self.frame_sf, width=5, textvariable=self.dim_k)
       self.txt_k.place(relx=0.12, rely=0.647, relwidth=0.08, relheight=0.075)
       self.txt_fill = ttk.Entry(self.frame_sf, width=5, textvariable=self.fill)
       self.txt_fill.place(relx=0.12, rely=0.724, relwidth=0.08, relheight=0.075)

       self.lbl_found_name = ttk.Label(self.frame_sf, text='Pit_Name', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.04, relwidth=0.1, relheight=0.075)
       self.txt_pit_name = ttk.Entry(self.frame_sf, width=5, textvariable=self.found_name)
       self.txt_pit_name.place(relx=0.34, rely=0.04, relwidth=0.25, relheight=0.075)
       self.lbl_quantity = ttk.Label(self.frame_sf, text='Quantity', font=("Pickwick", 8, "bold")).place(relx=0.23, rely=0.116, relwidth=0.1, relheight=0.075)
       self.txt_quantity = ttk.Entry(self.frame_sf, width=5, textvariable=self.quantity)
       self.txt_quantity.place(relx=0.34, rely=0.116, relwidth=0.05, relheight=0.075)

       self.bypass_button = ttk.Button(self, text="ADD PIT", command=self.addPit, cursor="hand2",style='W.TButton')
       self.bypass_button.place(relx=0.72, rely=0.377, relwidth=0.09, relheight=0.05)

       try:
           if selected_item[1] == "PIT":
               try:
                   self.txt_a.delete(0,tk.END)
                   self.txt_b.delete(0,tk.END)
                   self.txt_c.delete(0,tk.END)
                   self.txt_d.delete(0,tk.END)
                   self.txt_e.delete(0,tk.END)
                   self.txt_f.delete(0,tk.END)
                   self.txt_g.delete(0,tk.END)
                   self.txt_h.delete(0,tk.END)
                   self.txt_k.delete(0,tk.END)
                   self.txt_fill.delete(0,tk.END)
                   self.txt_quantity.delete(0,tk.END)
                   self.txt_pit_name.delete(0,tk.END)
                   self.txt_pit_name.insert(tk.END,selected_ind_found[0][1])
                   self.txt_a.insert(tk.END,selected_ind_found[0][2])
                   self.txt_b.insert(tk.END,selected_ind_found[0][3])
                   self.txt_c.insert(tk.END,selected_ind_found[0][4])
                   self.txt_d.insert(tk.END,selected_ind_found[0][5])
                   self.txt_e.insert(tk.END,selected_ind_found[0][6])
                   self.txt_f.insert(tk.END,selected_ind_found[0][7])
                   self.txt_g.insert(tk.END,selected_ind_found[0][8])
                   self.txt_h.insert(tk.END,selected_ind_found[0][9])
                   self.txt_k.insert(tk.END,selected_ind_found[0][10])
                   self.txt_fill.insert(tk.END,selected_ind_found[0][11])
                   self.txt_quantity.insert(tk.END,selected_ind_found[0][12])
               except NameError:
                   pass
               except IndexError:
                   pass
       except NameError:
           pass

   def GSUandFireWallCalculator(self):
       print("Fire Wall Calculator")

   def pavementCalculator(self):
       print("Pavement Calculator")



   def gtIndoorCheck(self):
       print(self.gtindoor.get())






app = main_gui()
app.mainloop()