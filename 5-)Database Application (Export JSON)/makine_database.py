from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
from tkcalendar import DateEntry
import json

root = Tk()
root.title("Makine Ver,tabanı")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 900
height = 500
root.wm_state('zoomed')

#==================================VARIABLES==========================================
MAKINE_ADI = StringVar()
MODEL = StringVar()
FIYAT= DoubleVar()
URETIM_TARIHI = StringVar()
SEARCH=StringVar()
temp=StringVar()

#==================================METHODS============================================
def Database():
    global conn, cursor
    conn = sqlite3.connect('makine_db.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `makineler` (mak_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, MAKINE_ADI TEXT, MODEL TEXT, FIYAT DOUBLE,URETIM_TARIHI TEXT)")

def Create():
    if  MAKINE_ADI.get() == "" or MODEL.get() == "":
        txt_result.config(text="Lütfen eksik alanları doldurun!", fg="red")
    else:
        Database()
        cursor.execute("INSERT INTO `makineler` (MAKINE_ADI, MODEL,FIYAT,URETIM_TARIHI) VALUES(?, ?, ?, ?)", (str(MAKINE_ADI.get()), str(MODEL.get()),str(FIYAT.get()) ,str(URETIM_TARIHI.get())))
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM `makineler` ORDER BY `MAKINE_ADI` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3],data[4]))
        conn.commit()
        MAKINE_ADI.set("")
        MODEL.set("")
        FIYAT.set("")
        URETIM_TARIHI.set("")
        cursor.close()
        conn.close()
        txt_result.config(text="Makine Eklendi!", fg="green")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `makineler` ORDER BY `MAKINE_ADI` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3],data[4]))
    cursor.close()
    conn.close()
    txt_result.config(text="Kayıtlar başarıyla okundu!", fg="black")

def Update():
    Database()
    if MAKINE_ADI.get() == "":
        txt_result.config(text="Makine adı seçin", fg="red")
    else:
        tree.delete(*tree.get_children())
        cursor.execute("UPDATE `makineler` SET `MAKINE_ADI` = ?, 'MODEL' = ?,'FIYAT'=? ,`URETIM_TARIHI` =? WHERE `mak_id` = ?", (MAKINE_ADI.get(), MODEL.get(),FIYAT.get() ,URETIM_TARIHI.get(),mak_id))
        conn.commit()
        cursor.execute("SELECT * FROM `makineler` ORDER BY `MAKINE_ADI` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3],data[4]))
        cursor.close()
        conn.close()
        MAKINE_ADI.set("")
        MODEL.set("")
        FIYAT.set("")
        URETIM_TARIHI.set("")
        txt_result.config(text="Vertabanı Güncellendi!", fg="black")

def searchdb():
    tree.delete(*tree.get_children())
    Database()
    if(temp.get()=="MAKINE_ADI"):
      cursor.execute("SELECT * FROM 'makineler' WHERE MAKINE_ADI LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    elif(temp.get()=="MODEL"):
      cursor.execute("SELECT * FROM 'makineler' WHERE MODEL LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    elif(temp.get()=="FIYAT"):
      cursor.execute("SELECT * FROM 'makineler' WHERE FIYAT LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    elif(temp.get()=="URETIM TARIHI"):
      cursor.execute("SELECT * FROM 'makineler' WHERE URETIM_TARIHI LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    else:
      cursor.execute("SELECT * FROM 'makineler' WHERE FIYAT LIKE '%s' ORDER BY '' ASC" %SEARCH.get())
    fetch=cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3],data[4]))
    cursor.close()
    conn.close()
    txt_result.config(text="Database araması tamamlandı!",fg="black")


def OnSelected(event):
    global mak_id;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mak_id = selecteditem[0]
    MAKINE_ADI.set("")
    MODEL.set("")
    FIYAT.set("")
    URETIM_TARIHI.set("")
    MAKINE_ADI.set(selecteditem[1])
    MODEL.set(selecteditem[2])
    FIYAT.set(selecteditem[3])
    URETIM_TARIHI.set(selecteditem[4])

def Delete():
    if not tree.selection():
       txt_result.config(text="Lütfen silmek istediğiniz kaydı seçin", fg="red")
    else:
        result = tkMessageBox.askquestion('Makineler', 'Bu veri kaydını silmek istediğinize emin misiniz?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `makineler` WHERE `mak_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            txt_result.config(text="Veri kaydı başarıyla silindi", fg="black")


def Json():
    Database()
    makineleri_bul = cursor.execute("SELECT * FROM makineler")
    #print([item[4] for item in makineleri_bul])
    makine_adları = []
    makine_modelleri = []
    makine_fiyatları = []
    makine_tarihleri = []
    for item in makineleri_bul:
        makine_adları.append(item[1])
        makine_modelleri.append(item[2])
        makine_fiyatları.append(item[3])
        makine_tarihleri.append(item[4])
    makine_dict = {"makine_adları":makine_adları,
            "makine_modelleri":makine_modelleri,
            "makine_fiyatları":makine_fiyatları,
            "makine_tarihleri":makine_tarihleri}
    print(makine_dict)
    makine_json = json.dumps(makine_dict)
    with open("makine_list.json", "w") as outfile:
        outfile.write(makine_json)




#================================FRAME=========================
title=Frame(root,height=60,width=1300,bd=8,relief="raise")
title.pack(side=TOP)
left=Frame(root,width=400,height=1240,bd=1,relief="raise")
left.pack(side=LEFT)
right=Frame(root,width=900,height=1232)
right.pack(side=LEFT)
searchframe=Frame(left,bd=8,width=392,height=150,relief="raise")
searchframe.pack(side=TOP)
form=Frame(left,height=400,width=392,bd=8)
form.pack(side=TOP)
buttonf=Frame(left,bd=8,relief="raise",width=100,height=250)
buttonf.pack(side=BOTTOM)
RadioGroup = Frame(form)


#==================================LABEL WIDGET=======================================
temp.set("MAKINE_ADI")
searchoptions=OptionMenu(searchframe,temp,"MAKINE_ADI","MODEL","FIYAT","URETIM TARIHI")
searchoptions.pack(side=LEFT)
txt_Search=Label(searchframe,text="Arama",font=('arial',12))
txt_Search.pack(side=TOP)
txt_title = Label(title, width=900, font=('arial', 24), text = "MAKİNE VERİTABANI")
txt_title.pack()
txt_Makine_Adı = Label(form, text="MAKINE_ADI:", font=('arial', 12), bd=8)
txt_Makine_Adı.grid(row=0, sticky="e")
txt_model = Label(form, text="MODEL:", font=('arial', 12), bd=8)
txt_model.grid(row=1, sticky="e")
txt_fiyat=Label(form, text="FIYAT:", font=('arial', 12), bd=8)
txt_fiyat.grid(row=2,sticky='e')
txt_tarih = Label(form, text="URETIM_TARIHI:", font=('arial', 12), bd=8)
txt_tarih.grid(row=3, sticky="e")
txt_result = Label(buttonf)
txt_result.pack(side=TOP)
#==================================ENTRY WIDGET=======================================
Searchtext=Entry(searchframe,textvariable=SEARCH,width=40)
Searchtext.pack(side=TOP)
makine_adı = Entry(form, textvariable=MAKINE_ADI, width=40)
makine_adı.grid(row=0, column=1)
model = Entry(form, textvariable=MODEL, width=40)
model.grid(row=1, column=1)
fiyat = Entry(form,textvariable=FIYAT,width=40)
fiyat.grid(row=2,column=1)
üretim_tarihi = DateEntry(form,selectmode='day' ,textvariable=URETIM_TARIHI, width=40)
üretim_tarihi.grid(row=3, column=1)

#==================================BUTTONS WIDGET=====================================
btn_create = Button(buttonf, width=20, text="Yeni Makine", command=Create)
btn_create.pack(side=LEFT)
btn_read = Button(buttonf, width=20, text="Veritabanından Oku", command=Read )
btn_read.pack(side=LEFT)
btn_update = Button(buttonf, width=20, text="Kaydı Güncelle", command=Update)
btn_update.pack(side=LEFT)
btn_delete = Button(buttonf, width=20, text="Kaydı Sil", command=Delete)
btn_delete.pack(side=LEFT)
btn_exit = Button(buttonf, width=20, text="JSON Oluştur", command=Json)
btn_exit.pack(side=LEFT)
btn_search = Button(searchframe,width=20,text="Ara",command=searchdb)
btn_search.pack(side=BOTTOM)


#==================================LIST WIDGET========================================
scrollbary = Scrollbar(right, orient=VERTICAL)
scrollbarx = Scrollbar(right, orient=HORIZONTAL)
tree = ttk.Treeview(right, columns=("Makine ID", "Makine Adı", "Model","Fiyat" ,"Üretim Tarihi"), selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Makine ID', text="Makine ID", anchor=W)
tree.heading('Makine Adı', text="Makine Adı", anchor=W)
tree.heading('Model', text="Model", anchor=W)
tree.heading('Fiyat',text="Fiyat",anchor=W)
tree.heading('Üretim Tarihi', text="Üretim Tarihi", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=90)
tree.column('#3', stretch=NO, minwidth=0, width=100)
tree.column('#4',stretch=NO,minwidth=0,width=50)
tree.column('#4', stretch=NO, minwidth=0, width=60)
tree.pack()
tree.bind('<<TreeviewSelect>>', OnSelected)
#==================================INITIALIZATION=====================================
if __name__ == '__main__':
    root.mainloop()
