import sqlite3
from tkinter import *
from tkinter import messagebox
import re

### Function and Procedure Area #########################################################

def executeDML(script):
    try:
        print("Executing:" + script)
        conn.execute(script)
    except sqlite3.Error as e:
        print("Database Error:" + e.args[0])
    else:
        conn.commit()
        loadList("select name from addressbook order by name")
        messagebox.showinfo("Saved:", "Saved to Database")
        mode_change("ReadOnly")

def select_data(script):
    cursor = conn.cursor()
    cursor.execute(script)
    return cursor.fetchall()

def displayData(script):
    mode_change("Write")
    #closeNameList()
    if len(select_data(script)) == 0:
        return 0
        
    for row in select_data(script):
        rownum = 0
        for x,y in emp_dict.items():
            emp_dict[x].delete(0, END)
            emp_dict[x].insert(0, str(row[rownum]))
            rownum = rownum + 1
    mode_change("ReadOnly")
    loadList("select name from addressbook order by name")

def onselect(evt):
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        listSelect(value)
    except:
        print("Name List Selection off")
        
def loadList(script):
    rownum=0
    nameList.delete(0,END)
    for row in select_data(script):
        rownum=rownum+1
        nameList.insert(rownum, row[0])
    window.update()
    nameList.config(height=frame.winfo_width())

def listSelect(inName):
    for row in select_data("select * from addressbook where Name='" + inName + "'"):
        rownum = 0
        for x,y in emp_dict.items():
            mode_change("Write")
            emp_dict[x].delete(0, END)
            emp_dict[x].insert(0, str(row[rownum]))
            mode_change("ReadOnly")
            rownum = rownum + 1

def btnSave():
    if DMLFlag == "AddNew":
        inData = "insert into AddressBook values('"
        inData = inData + emp_dict["Name:"].get() + "','" + emp_dict["Mobile:"].get() + "')"
    elif DMLFlag == "Edit":
        inData = "update AddressBook set Name='" + emp_dict["Name:"].get() + "',"
        inData = inData + "Mobile='" + emp_dict["Mobile:"].get() + "' where Name='" + EditKey + "'"
    executeDML(inData)

def btnAddNew():
    global DMLFlag
    global CancelKey
    DMLFlag = "AddNew"
    mode_change("Write")
    CancelKey = emp_dict["Name:"].get()
    for x,y in emp_dict.items():
        emp_dict[x].delete(0, END)
    emp_dict["Name:"].focus_set()

def btnEdit():
    global DMLFlag
    global EditKey
    global CancelKey
    DMLFlag = "Edit"
    CancelKey = emp_dict["Name:"].get()
    EditKey = emp_dict["Name:"].get()
    mode_change("Write")

def btnDelete():
    if messagebox.askokcancel("Delete", "Do you want to Delete this record?"):
        executeDML("delete from AddressBook where Name='" + emp_dict["Name:"].get() + "'")
        if displayData("select * from AddressBook where Name>'" + emp_dict["Name:"].get() + "' order by name LIMIT 1") == 0:
            if displayData("select * from AddressBook where Name<'" + emp_dict["Name:"].get() + "' order by name desc LIMIT 1") == 0:
                mode_change("Empty")

def btnCancel():
    if displayData("select * from AddressBook where Name='" + CancelKey + "'") == 0:
        mode_change("Empty")

def mode_change(inMode):
    if inMode == "ReadOnly":
        for x,y in emp_dict.items():
            emp_dict[x].config(state="disabled")
        btnAddNew.config(state="normal")
        btnDelete.config(state="normal")
        btnSave.config(state="disabled")
        btnEdit.config(state="normal")
        btnCancel.config(state="disabled")
    elif inMode == "Write":
        for x,y in emp_dict.items():
            emp_dict[x].config(state="normal")
        btnAddNew.config(state="disabled")
        btnDelete.config(state="disabled")
        btnSave.config(state="normal")
        btnEdit.config(state="disabled")
        btnCancel.config(state="normal")
    elif inMode == "Empty":
        for x,y in emp_dict.items():
            emp_dict[x].delete(0, END)
            emp_dict[x].config(state="disable")
        btnAddNew.config(state="normal")
        btnDelete.config(state="disabled")
        btnSave.config(state="disable")
        btnEdit.config(state="disabled")
        btnCancel.config(state="disabled")

def keyup(e):
    #print('up', e.char)
    loadList("select name from addressbook where name like '%" + re.sub('[^A-Za-z0-9]+', ' ', searchBox.get()) + "%' order by name")
    
#def keydown(e):
#    print('down', e.char)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        conn.close()
        print("Database closed")
        window.destroy()
        #closeNameList()
        

### Program starts here #################################################################
window = Tk()
window.title("BKV Address Book")
window.geometry('600x400')
window.update()
window.minsize(window.winfo_width(), window.winfo_height())

frame = Frame(window, bd=2, relief=SUNKEN)
searchBox = Entry(frame)
searchBox.pack(fill=X)
scrollbar = Scrollbar(frame)
nameList = Listbox(frame, bd=0, yscrollcommand=scrollbar.set)
scrollbar.config(command=nameList.yview)

scrollbar.pack(side=RIGHT, fill=Y)
frame.pack(side=RIGHT, padx=5, pady=10, fill=Y)
nameList.pack()

nameList.bind('<<ListboxSelect>>', onselect)
searchBox.bind("<KeyRelease>", keyup)
#x.bind("<KeyPress>", keydown)

conn = sqlite3.connect('Database.db')
emp_dict = {
  "Name:": "",
  "Mobile:": ""
}

#### Defining Label, TextBox and Buttons ####
rownum=0
input_data=""
for x,y in emp_dict.items():
    lbl = Label(window, text= x, justify=RIGHT)
    #lbl.grid(column=0, row=rownum)
    lbl.place(x=0, y =rownum)
    emp_dict[x] = Entry(window,width=20)
    #emp_dict[x].grid(column=1, row=rownum)
    emp_dict[x].place(x=50, y = rownum)
    rownum=rownum+20

btnFrame = Frame(window, bd=2, relief=SUNKEN)
btnAddNew = Button(btnFrame, text="Add New", command=btnAddNew, width=8)
btnSave = Button(btnFrame, text="Save", command=btnSave, width=8)
btnEdit = Button(btnFrame, text="Edit", command=btnEdit, width=8)
btnCancel = Button(btnFrame, text="Cancel", command=btnCancel, width=8)
btnDelete = Button(btnFrame, text="Delete", command=btnDelete, width=8)
btnFrame.pack(side=BOTTOM, padx=5, pady=20, fill=X)

btnAddNew.pack(side=LEFT, padx=5)
btnSave.pack(side=LEFT, padx=5)
btnEdit.pack(side=LEFT, padx=5)
btnCancel.pack(side=LEFT, padx=5)
btnDelete.pack(side=LEFT, padx=5)

if displayData("select * from addressbook order by name LIMIT 1") == 0:
    mode_change("Empty")
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
