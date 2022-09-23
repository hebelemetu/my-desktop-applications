from dbase import Database
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
from tkinter import ttk
from foundation_works import *
import pandas as pd
import sqlite3
import os
import time
from output_to_price_sheet import pricesheet
from foundation_works import *

db = Database('Database/swy_db.db')
pricesheet = pricesheet()
"""    ohl = getdouble(txt.get())
coupling = getdouble(txt2.get())
transformer = getdouble(txt3.get()) + getdouble(txt13.get())
transfer = getdouble(txt4.get())
"""


class background(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)



        self.image = Image.open("img/bg.png")
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

class parameter_bg(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)
        self.param_type = None

    def open_image(self):
        self.image = Image.open("img/{}.jpg".format(self.param_type))
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

class swy_gui(tk.Tk):
    def __init__(self):
        super().__init__()
        path = os.getcwd()
        print(path)
        self.title("Switchyard Tool")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.state("zoomed")



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
        style_button.configure('W.TButton', font=('calibri', 10, 'bold'), foreground='black')


#e = Example(window)
#e.pack(fill=BOTH, expand=YES)
#header.configure(font=("Times New Roman", 10, "bold"))
        self.Txtvar=IntVar()
        self.Txtvar2=IntVar()
        self.Txtvar3=IntVar()
        self.Txtvar4=IntVar()
        self.Txtvar5=IntVar()
        self.Txtvar6=IntVar()
        self.Txtvar7=IntVar()
        self.Txtvar8=IntVar()
        self.Txtvar9=IntVar()
        self.Txtvar10=IntVar()
        self.Txtvar11=IntVar()
        self.Txtvar12=IntVar()
        self.Txtvar13=IntVar()
        self.Txtvar14=IntVar()
        self.Txtvar15=IntVar()
        self.project_name = StringVar()
        self.lbl= Label(self, text="Outgoing Feeder Quantity", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl.place(relx=0.01,rely=0.075,relwidth=0.103,relheight=0.03)
        self.lbl2= Label(self, text="  Coupling Feeder Quantity  ", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl2.place(relx=0.01,rely=0.15,relwidth=0.103,relheight=0.03)
        self.lbl3= Label(self, text="  Transformer Feeder Quantity  ", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl3.place(relx=0.01,rely=0.225,relwidth=0.103,relheight=0.03)
        self.lbl5= Label(self, text="  Incoming Feeder Quantity  ", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl5.place(relx=0.01,rely=0.3,relwidth=0.103,relheight=0.03)
        self.lbl4= Label(self, text="Transfer Feeder Quantity", relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.lbl4.place(relx=0.01,rely=0.375,relwidth=0.103,relheight=0.03)
        self.lbl_project_name = Label(self, text="PROJECT NAME:", relief="groove", borderwidth=2,font=("Allegro", 8, "bold"))
        self.lbl_project_name.place(relx=0.35, rely=0.04, relwidth=0.07, relheight=0.03)
        self.txt_project_name = ttk.Entry(self, width=5, textvariable=self.project_name)
        self.txt_project_name.place(relx=0.425, rely=0.04, relwidth=0.1, relheight=0.03)
        self.txt =ttk.Entry(self,width=5,textvariable=self.Txtvar)
        self.txt2=ttk.Entry(self,width=5,textvariable=self.Txtvar2)
        self.txt3=ttk.Entry(self,width=5,textvariable=self.Txtvar3)
        self.txt13 = ttk.Entry(self,width=5,textvariable=self.Txtvar13)
        self.txt4=ttk.Entry(self,width=5,textvariable=self.Txtvar4)
        self.txt5 = ttk.Entry(self,width=5,textvariable=self.Txtvar5)
        self.txt6 = ttk.Entry(self,width=5,textvariable=self.Txtvar6)
        self.txt7 = ttk.Entry(self,width=5,textvariable=self.Txtvar7)
        self.txt14 = ttk.Entry(self,width=5,textvariable=self.Txtvar14)
        self.txt8 = ttk.Entry(self,width=5,textvariable=self.Txtvar8)
        self.txt9=ttk.Entry(self,width=5,textvariable=self.Txtvar9)
        self.txt10 = ttk.Entry(self,width=5,textvariable=self.Txtvar10)
        self.txt11=ttk.Entry(self,width=5,textvariable=self.Txtvar11)
        self.txt15 = ttk.Entry(self,width=5,textvariable=self.Txtvar15)
        self.txt12 = ttk.Entry(self,width=5,textvariable=self.Txtvar12)

        self.txt.place(relx=0.1204,rely=0.075,relwidth=0.05,relheight=0.03)
        self.txt2.place(relx=0.1204,rely=0.15,relwidth=0.05,relheight=0.03)
        self.txt3.place(relx=0.1204,rely=0.225,relwidth=0.05,relheight=0.03)
        self.txt4.place(relx=0.1204,rely=0.375,relwidth=0.05,relheight=0.03)
        self.txt5.place(relx=0.2,rely=0.075,relwidth=0.05,relheight=0.03)
        self.txt6.place(relx=0.2,rely=0.15,relwidth=0.05,relheight=0.03)
        self.txt7.place(relx=0.2,rely=0.225,relwidth=0.05,relheight=0.03)
        self.txt8.place(relx=0.2,rely=0.375,relwidth=0.05,relheight=0.03)
        self.txt9.place(relx=0.28,rely=0.075,relwidth=0.05,relheight=0.03)
        self.txt10.place(relx=0.28,rely=0.15,relwidth=0.05,relheight=0.03)
        self.txt11.place(relx=0.28,rely=0.225,relwidth=0.05,relheight=0.03)
        self.txt12.place(relx=0.28,rely=0.375,relwidth=0.05,relheight=0.03)
        self.txt13.place(relx=0.1204,rely=0.3,relwidth=0.05,relheight=0.03)
        self.txt14.place(relx=0.2,rely=0.3,relwidth=0.05,relheight=0.03)
        self.txt15.place(relx=0.28,rely=0.3,relwidth=0.05,relheight=0.03)




        self.selected=IntVar()
        self.lbl110kv= Label(self, text="110kv",relief="raised",borderwidth=2,font=("Allegro",10))
        self.lbl220kv= Label(self, text="220kv",relief="raised",borderwidth=2,font=("Allegro",10))
        self.lbl500kv= Label(self, text="500kv",relief="raised",borderwidth=2,font=("Allegro",10))


        self.rad4 = Radiobutton(self, text='TUBULAR', variable=self.selected, value=1, relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.rad5 = Radiobutton(self, text='WIRE', variable=self.selected, value=2, relief="groove", borderwidth=2, font=("Allegro", 8, "bold"))
        self.rad4.place(relx=0.35, rely=0.075, relwidth=0.055, relheight=0.03)
        self.rad5.place(relx=0.35, rely=0.15, relwidth=0.045, relheight=0.03)


        self.lbl110kv.place(relx=0.123,rely=0.04,relwidth=0.045,relheight=0.03)
        self.lbl220kv.place(relx=0.203,rely=0.04,relwidth=0.045,relheight=0.03)
        self.lbl500kv.place(relx=0.283,rely=0.04,relwidth=0.045,relheight=0.03)

        #image1 = PhotoImage(file="run.png")
        #image2=image1.subsample(5,4)
        self.run_button_image = tk.PhotoImage(file='img/run.png').subsample(3, 3)
        self.btn = ttk.Button(self, text="RUN", command=self.runbutton,cursor="hand2",style = 'W.TButton', image=self.run_button_image,compound = LEFT)
        self.btn.place(relx=0.1,rely=0.5,relwidth=0.05,relheight=0.05)
        self.quit_button_image = tk.PhotoImage(file='img/quit.png').subsample(3, 3)
        self.btn2 = ttk.Button(self, text="QUIT", command=self.on_closing,cursor="hand2",style = 'W.TButton', image=self.quit_button_image,compound = LEFT)
        self.btn2.place(relx=0.95,rely=0.01,relwidth=0.04,relheight=0.04)



        self.Widget_List=[self.txt,self.txt2,self.txt3,self.txt4,self.txt5,self.txt6,self.txt7,self.txt8,self.txt9,self.txt10,self.txt11,self.txt12,self.txt13,self.txt14,self.txt15,self.lbl,self.lbl2,self.lbl3,self.lbl4,self.lbl5,self.lbl110kv,self.lbl220kv,self.lbl500kv,self.btn,self.btn2,self.rad4,self.rad5]
        self.Place_Coordinates=np.array([[0.1204,0.1204,0.1204,0.1204,0.2,0.2,0.2,0.2,0.28,0.28,0.28,0.28,0.1204,0.2,0.28,0.01,0.01,0.01,0.01,0.01,0.123,0.203,0.283,0.1,0.95,0.35,0.35],
                                    [0.075,0.15,0.225,0.375,0.075,0.15,0.225,0.375,0.075,0.15,0.225,0.375,0.3,0.3,0.3,0.075,0.15,0.225,0.3,0.375,0.04,0.04,0.040,0.50,0.01,0.075,0.15],
                                    [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.106,0.106,0.106,0.106,0.106,0.045,0.045,0.045,0.05,0.04,0.055,0.045],
                                    [0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.05,0.04,0.03,0.03]])
        #for i in range(0, len(self.Widget_List)):
        #    self.Widget_List[i].place_forget()

        db.restartDatabase()
        self.add_menu()

            # Creating the username & password entry boxes
        self.username_text = Label(self, text="Username:", bg='light goldenrod', relief='groove')
        self.username_guess = ttk.Entry(self)
        self.username_guess.focus()
        self.password_text = Label(self, text="Password:", bg='light goldenrod', relief='groove')
        self.password_guess = ttk.Entry(self, show="*")

        self.attempt_login = ttk.Button(text="Login", command=self.try_login,style = 'W.TButton')

        """
        self.username_text.place(relx=0.45, rely=0.1455, relwidth=0.15, relheight=0.035)
        self.username_guess.place(relx=0.45, rely=0.1855, relwidth=0.15, relheight=0.035)
        self.password_text.place(relx=0.45, rely=0.2255, relwidth=0.15, relheight=0.035)
        self.password_guess.place(relx=0.45, rely=0.2655, relwidth=0.15, relheight=0.035)
        self.attempt_login.place(relx=0.45, rely=0.3055, relwidth=0.15, relheight=0.035)
        """
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def runbutton(self):
        start_time=time.time()
        pricesheet.table_output()
        self.empty_check()
        outgoing = getdouble(self.txt.get())
        coupling = getdouble(self.txt2.get())
        transformer = getdouble(self.txt3.get())
        transfer = getdouble(self.txt13.get())
        incoming = getdouble(self.txt4.get())
        outgoing2 = getdouble(self.txt5.get())
        coupling2 = getdouble(self.txt6.get())
        transformer2 = getdouble(self.txt7.get())
        transfer2 = getdouble(self.txt14.get())
        incoming2 = getdouble(self.txt8.get())
        outgoing3 = getdouble(self.txt9.get())
        coupling3 = getdouble(self.txt10.get())
        transformer3 = getdouble(self.txt11.get())
        transfer3 = getdouble(self.txt15.get())
        incoming3 = getdouble(self.txt12.get())
        project_name = self.txt_project_name.get()

        Feeder_Qty = (outgoing + coupling + transformer + transfer + incoming)
        Feeder_Qty2 = (outgoing2 + coupling2 + transformer2 + transfer2 + incoming2)
        Feeder_Qty3 = (outgoing3 + coupling3 + transformer3 + transfer3 + incoming3)


        outgoing110kv = [outgoing * x for x in db.fetchfeederType110("outgoing")[0]]
        coupling110kv = [coupling * x for x in db.fetchfeederType110("coupling")[0]]
        transformer110kv = [transformer * x for x in db.fetchfeederType110("transformer")[0]]
        transfer110kv = [transfer * x for x in db.fetchfeederType110("transfer")[0]]
        incoming110kv = [incoming * x for x in db.fetchfeederType110("incoming")[0]]

        sum110 = [sum(x) for x in zip(outgoing110kv, coupling110kv, transformer110kv, transfer110kv, incoming110kv)]

        outgoing220kv = [outgoing2 * x for x in db.fetchfeederType220("outgoing")[0]]
        coupling220kv = [coupling2 * x for x in db.fetchfeederType220("coupling")[0]]
        transformer220kv = [transformer2 * x for x in db.fetchfeederType220("transformer")[0]]
        transfer220kv = [transfer2 * x for x in db.fetchfeederType220("transfer")[0]]
        incoming220kv = [incoming2 * x for x in db.fetchfeederType220("incoming")[0]]

        sum220 = [sum(x) for x in zip(outgoing220kv, coupling220kv, transformer220kv, transfer220kv, incoming220kv)]

        outgoing500kv = [outgoing3 * x for x in db.fetchfeederType500("outgoing")[0]]
        coupling500kv = [coupling3 * x for x in db.fetchfeederType500("coupling")[0]]
        transformer500kv = [transformer3 * x for x in db.fetchfeederType500("transformer")[0]]
        transfer500kv = [transfer3 * x for x in db.fetchfeederType500("transfer")[0]]
        incoming500kv = [incoming3 * x for x in db.fetchfeederType500("incoming")[0]]

        sum500 = [sum(x) for x in zip(outgoing500kv, coupling500kv, transformer500kv, transfer500kv, incoming500kv)]


        works = [2.7, 3.1, 3.2, 3.13, 4.1, 5.1, 6.1, 6.3, 7.3, 17.1,21.5,21.8]
        site_works = [ 2.13, 18.1, 20.2, 20.7, 20.11, 21.6, 21.8, 21.11, 2.4 ,2.11]

        if self.selected.get() == 2:
            print(self.selected.get())

            min_exc_depth_110 = db.fetchMinimumDepthWire("110kv")[0][0]
            min_exc_depth_220 = db.fetchMinimumDepthWire("220kv")[0][0]
            min_exc_depth_500 = db.fetchMinimumDepthWire("500kv")[0][0]


            for row,qty in zip(db.fetchFoundationWire110(),sum110):
                self.execute_wire(row=row,qty=qty,min_exc_depth=min_exc_depth_110)
            for row,qty in zip(db.fetchFoundationWire220(),sum220):
                self.execute_wire(row=row,qty=qty,min_exc_depth=min_exc_depth_220)
            for row,qty in zip(db.fetchFoundationWire500(),sum500):
                self.execute_wire(row=row,qty=qty,min_exc_depth=min_exc_depth_500)
            #Cables
            for row in db.fetchCable110():
                self.execute_channel_wire(row=row,qty=Feeder_Qty,min_exc_depth=min_exc_depth_110)
            for row in db.fetchCable220():
                self.execute_channel_wire(row=row,qty=Feeder_Qty2,min_exc_depth=min_exc_depth_220)
            for row in db.fetchCable500():
                self.execute_channel_wire(row=row,qty=Feeder_Qty3,min_exc_depth=min_exc_depth_500)

            for work in db.fetchResultsWire():
                results=list(work[0][1:])
                for i in range(0,len(works)):
                    db.update_works(work[0][0],results[i],works[i])

            #SITE WORKS TO works TABLE
            for row in db.fetchSiteWorkDimension("110kv"):
                self.execute_site_works_wire(row=row,qty=Feeder_Qty,min_exc_depth=min_exc_depth_110)
            for row in db.fetchSiteWorkDimension("220kv"):
                self.execute_site_works_wire(row=row,qty=Feeder_Qty2,min_exc_depth=min_exc_depth_220)
            for row in db.fetchSiteWorkDimension("500kv"):
                self.execute_site_works_wire(row=row,qty=Feeder_Qty3,min_exc_depth=min_exc_depth_500)

            for work in db.fetchResultsSitework():
                results=list(work[2:])
                for i in range(0,len(site_works)):
                    db.update_works(work[1],results[i],site_works[i])

            pricesheet.print("wire",sum110,sum220,sum500,project_name)

        elif self.selected.get() == 1:
            print(self.selected.get())

            min_exc_depth_110 = db.fetchMinimumDepthTubular("110kv")[0][0]
            min_exc_depth_220 = db.fetchMinimumDepthTubular("220kv")[0][0]
            min_exc_depth_500 = db.fetchMinimumDepthTubular("500kv")[0][0]


            for row,qty in zip(db.fetchFoundationTubular110(),sum110):
                self.execute_tubular(row=row,qty=qty,min_exc_depth=min_exc_depth_110)
            for row,qty in zip(db.fetchFoundationTubular220(),sum220):
                self.execute_tubular(row=row,qty=qty,min_exc_depth=min_exc_depth_220)
            for row,qty in zip(db.fetchFoundationTubular500(),sum500):
                self.execute_tubular(row=row,qty=qty,min_exc_depth=min_exc_depth_500)
            # Cables
            for row in db.fetchCable110():
                self.execute_channel_tubular(row=row,qty=Feeder_Qty,min_exc_depth=min_exc_depth_110)
            for row in db.fetchCable220():
                self.execute_channel_tubular(row=row,qty=Feeder_Qty2,min_exc_depth=min_exc_depth_220)
            for row in db.fetchCable500():
                self.execute_channel_tubular(row=row,qty=Feeder_Qty3,min_exc_depth=min_exc_depth_500)

            for work in db.fetchResultsTubular():
                results=list(work[0][1:])
                for i in range(0,len(works)):
                    db.update_works(work[0][0],results[i],works[i])

            #SITE WORKS TO works TABLE
            for row in db.fetchSiteWorkDimension("110kv"):
                self.execute_site_works_tubular(row=row,qty=Feeder_Qty,min_exc_depth=min_exc_depth_110)
            for row in db.fetchSiteWorkDimension("220kv"):
                self.execute_site_works_tubular(row=row,qty=Feeder_Qty2,min_exc_depth=min_exc_depth_220)
            for row in db.fetchSiteWorkDimension("500kv"):
                self.execute_site_works_tubular(row=row,qty=Feeder_Qty3,min_exc_depth=min_exc_depth_500)

            for work in db.fetchResultsSitework():
                results=list(work[2:])
                for i in range(0,len(site_works)):
                    db.update_works(work[1],results[i],site_works[i])

            pricesheet.print("tubular",sum110,sum220,sum500,project_name)

        elif self.selected.get() != 1 and self.selected.get() != 2:
            messagebox.showinfo("ERROR", "Please Enter Feeder Quantity and Choose Conductor type")
            return

        print("--- %s seconds ---" % (time.time() - start_time))
        pricesheet.open_output()

    def execute_tubular(self,row,qty,min_exc_depth):
        foundationtype = row[1]
        type = row[2]
        equipment = row[3]
        a = row[4]
        b = row[5]
        c = row[6]
        d = row[7]
        e = row[8]
        f = row[9]
        h = row[10]
        fill = row[11]
        bolt = row[12]
        pedestal = row[13]
        es = row[14]
        steel = row[15]
        itemtype = row[17]
        tubular_found = foundation(a,b,c,d,e,f,h,fill,bolt,pedestal,es,steel)
        db.insert_results_foundation_tubular(foundationtype,
                                             type,
                                             tubular_found.excavation(min_exc_depth)*qty,
                                             tubular_found.strfill()*qty,
                                             0,
                                             tubular_found.leanconc()*qty,
                                             tubular_found.strconcrete()*qty,
                                             tubular_found.secondconcrete()*qty,
                                             tubular_found.formwork()*qty,
                                             tubular_found.rebar()*qty,
                                             tubular_found.embeddedsteel()*qty,
                                             tubular_found.anchor()*qty,
                                             tubular_found.steelqty()*qty,
                                             tubular_found.concreteprot()*qty,
                                            c * d *  pedestal * qty,
                                            0,
                                            0,
                                            0,
                                            0,
                                            itemtype)

    def execute_wire(self,row,qty,min_exc_depth):
        foundationtype = row[1]
        type = row[2]
        equipment = row[3]
        a = row[4]
        b = row[5]
        c = row[6]
        d = row[7]
        e = row[8]
        f = row[9]
        h = row[10]
        fill = row[11]
        bolt = row[12]
        pedestal = row[13]
        es = row[14]
        steel = row[15]
        itemtype = row[17]
        tubular_wire = foundation(a,b,c,d,e,f,h,fill,bolt,pedestal,es,steel)
        db.insert_results_foundation_wire(foundationtype,
                                             type,
                                             tubular_wire.excavation(min_exc_depth)*qty,
                                             tubular_wire.strfill()*qty,
                                             0,
                                             tubular_wire.leanconc()*qty,
                                             tubular_wire.strconcrete()*qty,
                                             tubular_wire.secondconcrete()*qty,
                                             tubular_wire.formwork()*qty,
                                             tubular_wire.rebar()*qty,
                                             tubular_wire.embeddedsteel()*qty,
                                             tubular_wire.anchor()*qty,
                                             tubular_wire.steelqty()*qty,
                                             tubular_wire.concreteprot()*qty,
                                            c * d *  pedestal * qty,
                                            0,
                                            0,
                                            0,
                                            0,
                                            itemtype)

    def execute_channel_tubular(self,row,qty,min_exc_depth):
        channel_type =row[1]
        type = row[2]
        d = row[3]
        e = row[4]
        f = row[5]
        g = row[6]
        fill = row[7]
        division_wall = row[8]
        channel_length = row[9]
        cover_length = row[10]
        itemtype = row[11]
        a = f + division_wall * f + 2 * d + division_wall * d
        b = e + d + 0.1
        c = e + d
        cable_channel = cable(d,e,f,g,fill,division_wall,channel_length,cover_length)
        db.insert_results_cable_tubular(channel_type,
                                             type,
                                             cable_channel.Area() * qty * channel_length,
                                             cable_channel.cablestrfill()*qty * channel_length,
                                             0,
                                             cable_channel.cableleanconc()*qty * channel_length,
                                             cable_channel.cablestrconcrete()*qty * channel_length,
                                             0,
                                             cable_channel.cableformwork()*qty * channel_length,
                                             cable_channel.cablerebar() * qty * channel_length,
                                             cable_channel.cableembeddedsteel() * qty * channel_length,
                                             0,
                                             0,
                                             cable_channel.cableconcreteprot()*qty * channel_length,
                                            0,
                                            cable_channel.cableformworkcover()*qty * channel_length,
                                            cable_channel.cablewaterstopper()*qty * channel_length,
                                            cable_channel.cablejointiso()*qty * channel_length,
                                            cable_channel.cablelength()*qty,
                                            itemtype)

    def execute_channel_wire(self,row,qty,min_exc_depth):
        channel_type =row[1]
        type = row[2]
        d = row[3]
        e = row[4]
        f = row[5]
        g = row[6]
        fill = row[7]
        division_wall = row[8]
        channel_length = row[9]
        cover_length = row[10]
        itemtype = row[11]
        a = f + division_wall * f + 2 * d + division_wall * d
        b = e + d + 0.1
        c = e + d
        cable_channel = cable(d,e,f,g,fill,division_wall,channel_length,cover_length)
        db.insert_results_cable_wire(channel_type,
                                             type,
                                             cable_channel.Area() * qty * channel_length,
                                             cable_channel.cablestrfill()*qty * channel_length,
                                             0,
                                             cable_channel.cableleanconc()*qty * channel_length,
                                             cable_channel.cablestrconcrete()*qty * channel_length,
                                             0,
                                             cable_channel.cableformwork()*qty * channel_length,
                                             cable_channel.cablerebar() * qty * channel_length,
                                             cable_channel.cableembeddedsteel()*qty * channel_length,
                                             0,
                                             0,
                                             cable_channel.cableconcreteprot()*qty * channel_length,
                                            0,
                                            cable_channel.cableformworkcover()*qty * channel_length,
                                            cable_channel.cablewaterstopper()*qty * channel_length,
                                            cable_channel.cablejointiso()*qty * channel_length,
                                            cable_channel.cablelength() * qty,
                                            itemtype)

    def execute_site_works_tubular(self,row,qty,min_exc_depth):
        type = row[1]
        print(f"Feeder Type = {type}")
        fence_length = row[2]
        print(f"fence_length={fence_length*qty}")
        print(f"minimum exc depth= {min_exc_depth}")
        print(f"quantity={qty}")
        road_length = row[3]
        road_width = row[4]
        print(f"road_width = {road_width}")
        extension_road_length = row[6]
        print(f"extension road length = {extension_road_length}")
        excavation_length = extension_road_length / 2 - 2 * road_width - 5
        print(f"excavation length = {excavation_length}")
        site_area = row[5] * qty + self.zero_division(extension_road_length,qty) * qty * 10
        print(f"site area = {site_area} --> {row[5] * qty} + {self.zero_division(extension_road_length,qty) * qty * 10}")
        site_work = fence_road(fence_length,road_length,road_width)
        road_area = site_work.road_length_perfeeder() * road_width * qty + self.zero_division(extension_road_length,qty) * qty * road_width
        print(f"road area = {road_area} --> {site_work.road_length_perfeeder() * road_width * qty} + {self.zero_division(extension_road_length,qty) * qty * road_width}")
        road_length = site_work.road_length_perfeeder() * qty + self.zero_division(extension_road_length,qty) * qty
        total_fence_length = site_work.fence_length_perfeeder() * qty + self.zero_division(extension_road_length,qty) * qty
        total_foundation_area = db.fetchTotalFoundationArea(type)[0][0]
        print(f"total foundation area = {total_foundation_area}")
        min_exc_depth = self.zero_division(min_exc_depth,qty) * qty
        total_excavation = site_work.excavation_site(min_exc_depth,fence_length * qty,excavation_length) + db.fetchResultTubularExcavationFound(type)[0][0]
        print(f"excess excavation total= {db.fetchResultTubularExcavationFound(type)[0][0]}")
        total_backfill = total_excavation - db.fetchResultsBackfillTubular(type)[0][0] - db.fetchResultBackfillTubularChannel(type)[0][0]
        gravel_surfacing = site_area - road_area - total_foundation_area
        pipe_150mm = road_length
        electric_conduit = road_length
        pit_manhole = round(road_length / 25,0)
        road_joint = road_length / 6 * 4 + db.fetchResultTubularJoint(type)[0][0]
        kerbstone = road_length * 2
        db.insert_results_sitework(type,
                                   gravel_surfacing,
                                   total_fence_length,
                                   pipe_150mm,
                                   electric_conduit,
                                   pit_manhole,
                                   road_area,
                                   road_joint,
                                   kerbstone,
                                   total_excavation,
                                   total_backfill)

    def execute_site_works_wire(self,row,qty,min_exc_depth):
        type = row[1]
        print(f"Feeder Type = {type}")
        fence_length = row[2]
        print(f"fence_length={fence_length*qty}")
        print(f"minimum exc depth= {min_exc_depth}")
        print(f"quantity={qty}")
        road_length = row[3]
        road_width = row[4]
        print(f"road_width = {road_width}")
        extension_road_length = row[6]
        print(f"extension road length = {extension_road_length}")
        excavation_length = extension_road_length / 2 - 2 * road_width - 5
        print(f"excavation length = {excavation_length}")
        site_area = row[5] * qty + self.zero_division(extension_road_length,qty) * qty * 10
        print(f"site area = {site_area} --> {row[5] * qty} + {self.zero_division(extension_road_length,qty) * qty * 10}")
        site_work = fence_road(fence_length,road_length,road_width)
        road_area = site_work.road_length_perfeeder() * road_width * qty + self.zero_division(extension_road_length,qty) * qty * road_width
        print(f"road area = {road_area} --> {site_work.road_length_perfeeder() * road_width * qty} + {self.zero_division(extension_road_length,qty) * qty * road_width}")
        road_length = site_work.road_length_perfeeder() * qty + self.zero_division(extension_road_length,qty) * qty
        total_fence_length = site_work.fence_length_perfeeder() * qty + self.zero_division(extension_road_length,qty) * qty
        total_foundation_area = db.fetchTotalFoundationArea(type)[0][0]
        print(f"total foundation area = {total_foundation_area}")
        min_exc_depth = self.zero_division(min_exc_depth,qty) * qty
        total_excavation = site_work.excavation_site(min_exc_depth,fence_length * qty,excavation_length) + db.fetchResultWireExcavationFound(type)[0][0]
        print(f"excess excavation total= {db.fetchResultTubularExcavationFound(type)[0][0]}")
        total_backfill = total_excavation - db.fetchResultsBackfillWire(type)[0][0] - db.fetchResultBackfillWireChannel(type)[0][0]
        gravel_surfacing = site_area - road_area - total_foundation_area
        pipe_150mm = road_length
        electric_conduit = road_length
        pit_manhole = round(road_length / 25,0)
        road_joint = road_length / 6 * 4 + db.fetchResultWireJoint(type)[0][0]
        kerbstone = road_length * 2
        db.insert_results_sitework(type,
                                   gravel_surfacing,
                                   total_fence_length,
                                   pipe_150mm,
                                   electric_conduit,
                                   pit_manhole,
                                   road_area,
                                   road_joint,
                                   kerbstone,
                                   total_excavation,
                                   total_backfill)

    def empty_check(self):
        Textbox_list = [self.txt, self.txt2, self.txt3, self.txt4, self.txt5, self.txt6, self.txt7, self.txt8, self.txt9, self.txt10, self.txt11, self.txt12, self.txt13, self.txt14, self.txt15]
        for text in Textbox_list:
            if len(text.get()) == 0:
                text.insert(0, '0')

    def zero_division(self,x, y):
        try:
            return x / y
        except ZeroDivisionError:
            return 0

    def add_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.submenu = Menu(self.filemenu, tearoff=0)
        self.submenu_type_cd = Menu(self.submenu, tearoff=0)
        self.submenu_type_fdt = Menu(self.submenu, tearoff=0)
        self.submenu_type_fdw = Menu(self.submenu, tearoff=0)
        self.submenu_type_fpf = Menu(self.submenu, tearoff=0)
        self.submenu_type_sw = Menu(self.submenu, tearoff=0)
        self.filemenu.add_cascade(label="Preferences", menu=self.submenu, underline=0)
        self.submenu.add_cascade(label="Foundation Per Feeder", menu=self.submenu_type_fpf, underline=0)
        self.submenu.add_cascade(label="Foundation Dimensions Tubular", menu=self.submenu_type_fdt, underline=0)
        self.submenu.add_cascade(label="Foundation Dimensions Wire", menu=self.submenu_type_fdw, underline=0)
        self.submenu.add_cascade(label="Channel Dimensions", menu=self.submenu_type_cd, underline=0)
        self.submenu.add_cascade(label="Site Work Dimensions", menu=self.submenu_type_sw, underline=0)
        self.submenu_type_fpf.add_command(label="Foundation Per Outgoing Feeder",command=lambda index="fpf",type="outgoing": self.change_attr(index,type))
        self.submenu_type_fpf.add_command(label="Foundation Per Coupling Feeder",command=lambda index="fpf",type="coupling": self.change_attr(index,type))
        self.submenu_type_fpf.add_command(label="Foundation Per Transformer Feeder",command=lambda index="fpf",type="transformer": self.change_attr(index,type))
        self.submenu_type_fpf.add_command(label="Foundation Per Transfer Feeder",command=lambda index="fpf",type="transfer": self.change_attr(index,type))
        self.submenu_type_fpf.add_command(label="Foundation Per Incoming Feeder",command=lambda index="fpf",type="incoming": self.change_attr(index,type))
        self.submenu_type_fdt.add_command(label="110kv",command=lambda index="fdt",type="110kv": self.change_attr(index,type))
        self.submenu_type_fdt.add_command(label="220kv",command=lambda index="fdt",type="220kv": self.change_attr(index,type))
        self.submenu_type_fdt.add_command(label="500kv",command=lambda index="fdt",type="500kv": self.change_attr(index,type))
        self.submenu_type_fdw.add_command(label="110kv",command=lambda index="fdw",type="110kv": self.change_attr(index,type))
        self.submenu_type_fdw.add_command(label="220kv",command=lambda index="fdw",type="220kv": self.change_attr(index,type))
        self.submenu_type_fdw.add_command(label="500kv",command=lambda index="fdw",type="500kv": self.change_attr(index,type))
        self.submenu_type_cd.add_command(label="110kv",command=lambda index="cd",type="110kv": self.change_attr(index,type))
        self.submenu_type_cd.add_command(label="220kv",command=lambda index="cd",type="220kv": self.change_attr(index,type))
        self.submenu_type_cd.add_command(label="500kv",command=lambda index="cd",type="500kv": self.change_attr(index,type))
        self.submenu_type_sw.add_command(label="110kv",command=lambda index="sw",type="110kv": self.change_attr(index,type))
        self.submenu_type_sw.add_command(label="220kv",command=lambda index="sw",type="220kv": self.change_attr(index,type))
        self.submenu_type_sw.add_command(label="500kv",command=lambda index="sw",type="500kv": self.change_attr(index,type))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Reset Foundation Configuration", command=self.resetConfiguration)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Reset Foundation Dimensions", command=self.resetFoundationDimensions)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Reset Channel Dimensions", command=self.resetChannelDimensions)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)

    def resetFoundationDimensions(self):
        db.resetFoundationDimensions()

    def resetConfiguration(self):
        db.resetConfiguration()

    def resetChannelDimensions(self):
        db.resetChannelDimensions()

    def change_attr(self, index,type):
        def edit(event):
            if parameter_list.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list.identify_column(event.x)  # identify column
                print(parameter_list.heading(column, 'text'))

                def ok(event):
                    """Change item value."""
                    parameter_list.set(item, column, entry.get())
                    selected_parameter = parameter_list.item(parameter_list.selection())['values']
                    print(parameter_list.heading(column, 'text'), entry.get(), type)
                    db.updateFoundationPerFeeder(parameter_list.heading(column, 'text'), entry.get(), type)
                    print(type)
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
                    db.updateFoundationPerFeeder(parameter_list2.heading(column, 'text'), entry.get(), type)
                    print(parameter_list2.heading(column, 'text'), entry.get(), type)
                    print(type)
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
                    db.updateFoundationPerFeeder(parameter_list3.heading(column, 'text'), entry.get(), type)
                    print(type)
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

        def edit_dimension_tubular(event):
            if parameter_list.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list.identify_column(event.x)  # identify column
                print(parameter_list.heading(column, 'text'))

                def ok(event):
                    """Change item value."""
                    parameter_list.set(item, column, entry.get())
                    selected_parameter = parameter_list.item(parameter_list.selection())['values']
                    print(selected_parameter)
                    db.updateFoundationTubular(parameter_list.heading(column, 'text'), entry.get(), selected_parameter[0])
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

        def edit_dimension_wire(event):
            if parameter_list.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list.identify_column(event.x)  # identify column
                print(parameter_list.heading(column, 'text'))

                def ok(event):
                    """Change item value."""
                    parameter_list.set(item, column, entry.get())
                    selected_parameter = parameter_list.item(parameter_list.selection())['values']
                    print(selected_parameter)
                    db.updateFoundationWire(parameter_list.heading(column, 'text'), entry.get(), selected_parameter[0])
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

        def edit_dimensionchannel(event):
            if parameter_list.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list.identify_column(event.x)  # identify column
                print(parameter_list.heading(column, 'text'))

                def ok(event):
                    """Change item value."""
                    parameter_list.set(item, column, entry.get())
                    selected_parameter = parameter_list.item(parameter_list.selection())['values']
                    print(selected_parameter)
                    db.updateChannelDimension(parameter_list.heading(column, 'text'), entry.get(), selected_parameter[0],type)
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

        def edit_dimensionsite(event):
            if parameter_list.identify_region(event.x, event.y) == 'cell':
                # the user clicked on a cell
                column = parameter_list.identify_column(event.x)  # identify column
                print(parameter_list.heading(column, 'text'))

                def ok(event):
                    """Change item value."""
                    parameter_list.set(item, column, entry.get())
                    selected_parameter = parameter_list.item(parameter_list.selection())['values']
                    print(selected_parameter)
                    db.updateSiteDimension(parameter_list.heading(column, 'text'), entry.get(), selected_parameter[1])
                    print(index)
                    print(selected_parameter[1])
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

        if index == "fpf":
            top = Toplevel(self)
            top.title(f"{type} FOUNDATION PER FEEDER")
            top.config(background="black")
            column_parameter_fpf110 = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11")
            column_parameter_fpf220 = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11")
            column_parameter_fpf500 = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9")
            w = 750
            h = 360
            top.geometry("{}x{}".format(w, h))

            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_fpf110,
                                          style="Custom.Treeview")
            parameter_list.heading('#1', text='F13', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='F14', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='F15', anchor='center')
            parameter_list.column('#3', width=40, anchor='center', stretch=True)
            parameter_list.heading('#4', text='F16', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='F17', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='F18', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)
            parameter_list.heading('#7', text='F19', anchor='center')
            parameter_list.column('#7', width=40, anchor='center', stretch=True)
            parameter_list.heading('#8', text='F11', anchor='center')
            parameter_list.column('#8', width=40, anchor='center', stretch=True)
            parameter_list.heading('#9', text='F11A', anchor='center')
            parameter_list.column('#9', width=40, anchor='center', stretch=True)
            parameter_list.heading('#10', text='F11C', anchor='center')
            parameter_list.column('#10', width=40, anchor='center', stretch=True)
            parameter_list.heading('#11', text='F12', anchor='center')
            parameter_list.column('#11', width=40, anchor='center', stretch=True)

            parameter_list.place(relx=0, rely=0, relwidth=1, relheight=0.167)
            parameter_list.bind('<1>', edit)

            # parameter_list.delete(0,END)
            for param in db.fetchfeederType110_base(type):
                print(param)
                parameter_list.insert("", tk.END, values=param)
            # SECOND ROW
            parameter_list2 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_fpf220,
                                           style="Custom.Treeview")
            parameter_list2.heading('#1', text='F21', anchor='center')
            parameter_list2.column('#1', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#2', text='F21A', anchor='center')
            parameter_list2.column('#2', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#3', text='F21C', anchor='center')
            parameter_list2.column('#3', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#4', text='F22', anchor='center')
            parameter_list2.column('#4', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#5', text='F23', anchor='center')
            parameter_list2.column('#5', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#6', text='F24', anchor='center')
            parameter_list2.column('#6', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#7', text='F25', anchor='center')
            parameter_list2.column('#7', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#8', text='F26', anchor='center')
            parameter_list2.column('#8', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#9', text='F27', anchor='center')
            parameter_list2.column('#9', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#10', text='F28', anchor='center')
            parameter_list2.column('#10', width=40, anchor='center', stretch=True)
            parameter_list2.heading('#11', text='F29', anchor='center')
            parameter_list2.column('#11', width=40, anchor='center', stretch=True)

            parameter_list2.place(relx=0, rely=0.167, relwidth=1, relheight=0.167)
            parameter_list2.bind('<1>', edit2)

            # parameter_list2.delete(0,END)
            for param in db.fetchfeederType220_base(type):
                print(param)
                parameter_list2.insert("", tk.END, values=param)
            # THIRD ROW
            parameter_list3 = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_fpf500,
                                           style="Custom.Treeview")
            parameter_list3.heading('#1', text='F31', anchor='center')
            parameter_list3.column('#1', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#2', text='F31A', anchor='center')
            parameter_list3.column('#2', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#3', text='F32', anchor='center')
            parameter_list3.column('#3', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#4', text='F33', anchor='center')
            parameter_list3.column('#4', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#5', text='F34', anchor='center')
            parameter_list3.column('#5', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#6', text='F35', anchor='center')
            parameter_list3.column('#6', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#7', text='F36', anchor='center')
            parameter_list3.column('#7', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#8', text='F37', anchor='center')
            parameter_list3.column('#8', width=40, anchor='center', stretch=True)
            parameter_list3.heading('#9', text='F38', anchor='center')
            parameter_list3.column('#9', width=40, anchor='center', stretch=True)


            parameter_list3.place(relx=0, rely=0.334, relwidth=1, relheight=0.167)
            parameter_list3.bind('<1>', edit3)


            param_frame = ttk.Frame(top)
            #param_frame.pack(fill=BOTH,side=BOTTOM)
            param_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
            param_img = parameter_bg(param_frame)
            param_img.param_type = "feedertype"
            param_img.open_image()
            param_img.pack(fill=BOTH, expand=YES)

            # parameter_list3.delete(0,END)
            for param in db.fetchfeederType500_base(type):
                print(param)
                parameter_list3.insert("", tk.END, values=param)
        elif index == "fdt":
            top = Toplevel(self)
            top.title(f"{type} FOUNDATION DIMENSIONS")
            top.config(background="black")
            # w = self.winfo_screenwidth()
            w = 1450
            h = 750
            top.geometry("{}x{}".format(w, h))
            column_parameter_fdt = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11","#12", "#13", "#14", "#15", "#16")
            top.geometry("{}x{}".format(w, h))

            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_fdt,
                                          style="Custom.Treeview")
            parameter_list.heading('#1', text='foundationtype', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='equipment', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='a', anchor='center')
            parameter_list.column('#3', width=40, anchor='center', stretch=True)
            parameter_list.heading('#4', text='b', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='c', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='d', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)
            parameter_list.heading('#7', text='e', anchor='center')
            parameter_list.column('#7', width=40, anchor='center', stretch=True)
            parameter_list.heading('#8', text='f', anchor='center')
            parameter_list.column('#8', width=40, anchor='center', stretch=True)
            parameter_list.heading('#9', text='h', anchor='center')
            parameter_list.column('#9', width=40, anchor='center', stretch=True)
            parameter_list.heading('#10', text='fill', anchor='center')
            parameter_list.column('#10', width=40, anchor='center', stretch=True)
            parameter_list.heading('#11', text='bolt', anchor='center')
            parameter_list.column('#11', width=40, anchor='center', stretch=True)
            parameter_list.heading('#12', text='pedestal', anchor='center')
            parameter_list.column('#12', width=40, anchor='center', stretch=True)
            parameter_list.heading('#13', text='embedded steel', anchor='center')
            parameter_list.column('#13', width=40, anchor='center', stretch=True)
            parameter_list.heading('#14', text='steel', anchor='center')
            parameter_list.column('#14', width=40, anchor='center', stretch=True)
            parameter_list.heading('#15', text='g', anchor='center')
            parameter_list.column('#15', width=40, anchor='center', stretch=True)
            parameter_list.heading('#16', text='itemtype', anchor='center')
            parameter_list.column('#16', width=40, anchor='center', stretch=True)

            parameter_list.pack(fill=BOTH, expand=True)
            parameter_list.bind('<1>', edit_dimension_tubular)

            param_frame = ttk.Frame(top)
            #param_frame.pack(fill=BOTH,side=BOTTOM)
            param_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
            param_img = parameter_bg(param_frame)
            param_img.param_type = "fnddrw"
            param_img.open_image()
            param_img.pack(fill=BOTH, expand=YES)
            # parameter_list.delete(0,END)
            for param in db.fetchFoundationTubular(type):
                print(param)
                parameter_list.insert("", tk.END, values=param)
        elif index == "fdw":
            top = Toplevel(self)
            top.title(f"{type} FOUNDATION DIMENSIONS")
            top.config(background="black")
            # w = self.winfo_screenwidth()
            w = 1450
            h = 750
            top.geometry("{}x{}".format(w, h))
            column_parameter_fdw = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13", "#14", "#15", "#16")
            top.geometry("{}x{}".format(w, h))

            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_fdw,
                                          style="Custom.Treeview")
            parameter_list.heading('#1', text='foundationtype', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='equipment', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='a', anchor='center')
            parameter_list.column('#3', width=40, anchor='center', stretch=True)
            parameter_list.heading('#4', text='b', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='c', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='d', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)
            parameter_list.heading('#7', text='e', anchor='center')
            parameter_list.column('#7', width=40, anchor='center', stretch=True)
            parameter_list.heading('#8', text='f', anchor='center')
            parameter_list.column('#8', width=40, anchor='center', stretch=True)
            parameter_list.heading('#9', text='h', anchor='center')
            parameter_list.column('#9', width=40, anchor='center', stretch=True)
            parameter_list.heading('#10', text='fill', anchor='center')
            parameter_list.column('#10', width=40, anchor='center', stretch=True)
            parameter_list.heading('#11', text='bolt', anchor='center')
            parameter_list.column('#11', width=40, anchor='center', stretch=True)
            parameter_list.heading('#12', text='pedestal', anchor='center')
            parameter_list.column('#12', width=40, anchor='center', stretch=True)
            parameter_list.heading('#13', text='embedded steel', anchor='center')
            parameter_list.column('#13', width=40, anchor='center', stretch=True)
            parameter_list.heading('#14', text='steel', anchor='center')
            parameter_list.column('#14', width=40, anchor='center', stretch=True)
            parameter_list.heading('#15', text='g', anchor='center')
            parameter_list.column('#15', width=40, anchor='center', stretch=True)
            parameter_list.heading('#16', text='itemtype', anchor='center')
            parameter_list.column('#16', width=40, anchor='center', stretch=True)

            parameter_list.pack(fill=BOTH, expand=True)
            parameter_list.bind('<1>', edit_dimension_wire)

            param_frame = ttk.Frame(top)
            #param_frame.pack(fill=BOTH,side=BOTTOM)
            param_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
            param_img = parameter_bg(param_frame)
            param_img.param_type = "fnddrw"
            param_img.open_image()
            param_img.pack(fill=BOTH, expand=YES)
            # parameter_list.delete(0,END)
            for param in db.fetchFoundationWire(type):
                print(param)
                parameter_list.insert("", tk.END, values=param)
        elif index == "cd":
            top = Toplevel(self)
            top.title(f"{type} CHANNEL DIMENSIONS")
            top.config(background="black")
            # w = self.winfo_screenwidth()
            w = 1450
            h = 500
            top.geometry("{}x{}".format(w, h))
            column_parameter_cd = (
            "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10")
            top.geometry("{}x{}".format(w, h))

            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_cd,style="Custom.Treeview")
            parameter_list.heading('#1', text='ChannelType', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='d', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='e', anchor='center')
            parameter_list.column('#3', width=40, anchor='center', stretch=True)
            parameter_list.heading('#4', text='f', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='g', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='fill', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)
            parameter_list.heading('#7', text='DivisionWall', anchor='center')
            parameter_list.column('#7', width=40, anchor='center', stretch=True)
            parameter_list.heading('#8', text='ChannelLengthPerFeeder', anchor='center')
            parameter_list.column('#8', width=40, anchor='center', stretch=True)
            parameter_list.heading('#9', text='PrecastCoverLength', anchor='center')
            parameter_list.column('#9', width=40, anchor='center', stretch=True)
            parameter_list.heading('#10', text='Itemtype', anchor='center')
            parameter_list.column('#10', width=40, anchor='center', stretch=True)

            #parameter_list.pack(side=TOP,fill=BOTH,expand=True)
            parameter_list.place(relx=0, rely=0, relwidth=1, relheight=0.5)
            parameter_list.bind('<1>', edit_dimensionchannel)

            param_frame = ttk.Frame(top)
            #param_frame.pack(fill=BOTH,side=BOTTOM)
            param_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)
            param_img = parameter_bg(param_frame)
            param_img.param_type = "cable_drw"
            param_img.open_image()
            param_img.pack(fill=BOTH, expand=YES)

            # parameter_list.delete(0,END)
            for param in db.fetchCable(type):
                print(param)
                parameter_list.insert("", tk.END, values=param)
        elif index == "sw":
            top = Toplevel(self)
            top.title(f"{type} SITE DIMENSIONS")
            top.config(background="white")
            # w = self.winfo_screenwidth()
            w = 550
            h = 500
            top.geometry("{}x{}".format(w, h))
            column_parameter_cd = ("#1", "#2", "#3", "#4", "#5", "#6","#7")
            top.geometry("{}x{}".format(w, h))

            parameter_list = ttk.Treeview(top, show="headings", height="1", columns=column_parameter_cd,style="Custom.Treeview")
            parameter_list.heading('#1', text='index', anchor='center')
            parameter_list.column('#1', width=20, anchor='center', stretch=True)
            parameter_list.heading('#2', text='feedertype', anchor='center')
            parameter_list.column('#2', width=20, anchor='center', stretch=True)
            parameter_list.heading('#3', text='fence_length', anchor='center')
            parameter_list.column('#3', width=20, anchor='center', stretch=True)
            parameter_list.heading('#4', text='road_length', anchor='center')
            parameter_list.column('#4', width=40, anchor='center', stretch=True)
            parameter_list.heading('#5', text='road_width', anchor='center')
            parameter_list.column('#5', width=40, anchor='center', stretch=True)
            parameter_list.heading('#6', text='site_area', anchor='center')
            parameter_list.column('#6', width=40, anchor='center', stretch=True)
            parameter_list.heading('#7', text='extension_road_length', anchor='center')
            parameter_list.column('#7', width=40, anchor='center', stretch=True)

            #parameter_list.pack(side=TOP,fill=BOTH,expand=True)
            parameter_list.place(relx=0, rely=0, relwidth=1, relheight=0.5)
            parameter_list.bind('<1>', edit_dimensionsite)

            param_frame = ttk.Frame(top)
            #param_frame.pack(fill=BOTH,side=BOTTOM)
            param_frame.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.7)
            param_img = parameter_bg(param_frame)
            param_img.param_type = "sitedimension"
            param_img.open_image()
            param_img.pack(fill=BOTH, expand=YES)

            # parameter_list.delete(0,END)
            for param in db.fetchSiteWorkDimension(type):
                print(param)
                parameter_list.insert("", tk.END, values=param)

    def try_login(self):
        print("Trying to login...")
        #if self.password_guess.get() == password and self.username_guess.get()==username:
            #messagebox.showinfo("-- COMPLETE --", "You Are Now Logging In.", icon="info")
            #w = self.winfo_screenwidth()
            #h = self.winfo_screenheight()
            #self.geometry("%dx%d+0+0" % (w, h))
            #self.attributes("-fullscreen", False)
        for i in range(0, len(self.Widget_List)):
            self.Widget_List[i].place(relx=self.Place_Coordinates[0, i], rely=self.Place_Coordinates[1, i],relwidth=self.Place_Coordinates[2, i], relheight=self.Place_Coordinates[3, i])
        self.username_text.place_forget()
        self.username_guess.place_forget()
        self.password_text.place_forget()
        self.password_guess.place_forget()
        self.attempt_login.place_forget()
        self.txt.focus()
        #else:
        #    messagebox.showinfo("-- ERROR --", "Please enter valid infomation!", icon="warning")



    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


if __name__ == '__main__':
    gui =swy_gui()
    gui.mainloop()