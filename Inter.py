from tkinter import *
import pyodbc
import tkinter.ttk as ttk

from tkinter import messagebox
from PIL import ImageTk, Image

database = 'Dev'

t = []

def get_attributes(table_name):
    cursor = connection.cursor()
    cursor.execute(f"""SELECT COLUMN_NAME
                       FROM INFORMATION_SCHEMA.COLUMNS
                       WHERE TABLE_CATALOG = 'Dev'
                             AND TABLE_NAME = '{table_name}';""")
    row = cursor.fetchone()
    attr_list = []
    while row:
        in_text = str(row[0])
        attr_list.append(in_text)
        row = cursor.fetchone()
    c = connection.cursor()
    c.execute(f"""SELECT TOP(20) * FROM {table_name};""")
    row = c.fetchone()
    lst = []
    while row:
        for i in range(len(row)):
            in_text = str(row[i])
            lst.append(in_text)
        row = c.fetchone()
    return attr_list, lst


def check_attr_type(conn, table_name, attr, type):
    cursor = conn.cursor()
    cursor.execute(f""" SELECT DATA_TYPE
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{attr}'""")
    data_type = cursor.fetchone()
    print(data_type[0])
    return data_type[0] == type


def closing(window):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        welcome()


def welcome():
    window = Tk()
    window.title("YuyDev database")
    window.geometry('700x600')
    lbl = Label(window, text="Login", font=("Times New Roman", 30))
    lbl.place(relx=.4, rely=.2)
    lbll = Label(window, text="login :", font=("Times New Roman", 20))
    lbll.place(relx=.25, rely=.35)
    lblp = Label(window, text="password :", font=("Times New Roman", 20))
    lblp.place(relx=.18, rely=.5)
    txtl = Entry(window, width=30)
    txtl.place(relx=.38, rely=.37)
    txtp = Entry(window, width=30)
    txtp.place(relx=.38, rely=.52)
    btn = Button(window, text="Enter", bg="blue", fg="red", height=3, width=15, command=lambda: login(txtl.get(), txtp.get(), window))
    btn.place(relx=.4, rely=.7)
    window.mainloop()


def login(log, p, window):
    global connection
    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-PJJGVVN\SQLEXPRESS;DATABASE=Dev;UID=' + str(log) + ';PWD=' + str(p))

        dbCursor = connection.cursor()

        requestString = """SELECT table_name FROM information_schema.tables"""
        dbCursor.execute(requestString)
        for row in dbCursor:
            if row.table_name != 'sysdiagrams':
                t.append(row.table_name)
        print(t)
        window.destroy()
        database()
    except pyodbc.Error as err:
        messagebox.showinfo("Error", "Wrong username or password")


def database():
    window = Tk()
    window.title("YuyDev database")
    window.geometry('400x400')
    window.protocol("WM_DELETE_WINDOW", lambda: closing(window))
    btnt = Button(window, text="Work with Tables", height=3, width=15, command=tables)
    btnt.place(relx=.35, rely=.1)
    btnv = Button(window, text="Show Views", height=3, width=15, command=view)
    btnv.place(relx=.35, rely=.3)
    btnv = Button(window, text="Get report", height=3, width=15, command=report)
    btnv.place(relx=.35, rely=.5)

    window.mainloop()


def report():
    window = Tk()
    window.title("Report")
    window.geometry('400x200')
    combo = ttk.Combobox(window, height=30, width=40)
    combo['values'] = ['Get employee tasks', 'Get employees of the required specialization',
                       'Get the number of tasks for the employee']
    combo.place(relx=.1, rely=.05)
    combo.bind("<<ComboboxSelected>>", lambda x: take_report(combo.get(), window))
    window.mainloop()


def take_report(s, window):
    if s == 'Get employee tasks' or s == 'Get the number of tasks for the employee':
        lbl = Label(window, text='Enter Employee Id: ', font=("Times New Roman", 12))
        lbl.place(relx=.1, rely=.4)
        txtp = Entry(window, width=30)
        txtp.place(relx=.5, rely=.4)
    else:
        lbl = Label(window, text='Enter Specialization Id: ', font=("Times New Roman", 12))
        lbl.place(relx=.1, rely=.4)
        txtp = Entry(window, width=30)
        txtp.place(relx=.5, rely=.4)
    btnt = Button(window, text="Enter", height=3, width=15, command=lambda : fun(txtp.get(), s))
    btnt.place(relx=.35, rely=.7)


def fun(s, ss):
    if ss == 'Get employee tasks':
        c = connection.cursor()
        c.execute(f"""EXEC get_tasks @nm = {int(s)};""")
        row = c.fetchone()
        lst = []
        while row:
            for i in range(len(row)):
                in_text = str(row[i])
                lst.append(in_text)
            row = c.fetchone()
        print(lst)
        window = Tk()
        window.title("Task report")
        window.geometry('700x700')
        lbl = Label(window, text=f'Name: {lst[0]} {lst[1]}', font=("Times New Roman", 12))
        lbl.place(relx=.1, rely=.05)
        btnt = Button(window, text="TaskId", height=3, width=30)
        btnt.place(relx=.05, rely=.15)
        btnt = Button(window, text="TaskName", height=3, width=30)
        btnt.place(relx=.35, rely=.15)
        btnt = Button(window, text="DeadlineTask", height=3, width=30)
        btnt.place(relx=.65, rely=.15)
        cnt = 0
        h = .25
        for txt in lst:
            if txt != lst[0] and txt != lst[1]:
                lbl = Label(window, text=txt, font=("Times New Roman", 11))
                lbl.place(relx=cnt * .3 + .05, rely=h)
                if cnt % 2 == 0 and cnt != 0:
                    cnt = 0
                    h += .05
                else:
                    cnt += 1
    elif ss == 'Get the number of tasks for the employee':
        c = connection.cursor()
        c.execute(f"""DECLARE @a INT; EXEC count_tasks @nm = {s}, @ans = @a Output; SELECT @a;""")
        row = c.fetchone()
        lst = []
        while row:
            for i in range(len(row)):
                in_text = str(row[i])
                lst.append(in_text)
            row = c.fetchone()
        window = Tk()
        window.title("Task report")
        window.geometry('300x300')
        if int(lst[0]) > 3:
            t = 'bfu.jpg'
        else:
            t = 'bfd.jpg'
        img = ImageTk.PhotoImage(Image.open(t).resize((150, 150), Image.ANTIALIAS), master=window)
        panel = Label(window, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        lbl = Label(window, text=f"Total tasks: {lst[0]}", font=("Times New Roman", 20))
        lbl.place(relx=.25, rely=.8)
        c = connection.cursor()
        c.execute(f"""SELECT Name, Surname FROM Employees WHERE EmployeeId = {s};""")
        row = c.fetchone()
        lst = []
        while row:
            for i in range(len(row)):
                in_text = str(row[i])
                lst.append(in_text)
            row = c.fetchone()
        lbl = Label(window, text=f"Name: {lst[0]} {lst[1]}", font=("Times New Roman", 16))
        lbl.place(relx=.1, rely=.1)
    else:
        c = connection.cursor()
        c.execute(f"""EXEC get_specialization @nm = {int(s)};;""")
        row = c.fetchone()
        lst = []
        while row:
            for i in range(len(row)):
                in_text = str(row[i])
                lst.append(in_text)
            row = c.fetchone()
        window = Tk()
        window.title("Task report")
        window.geometry('700x700')
        lbl = Button(window, text='TeamId', height=3, width=25)
        lbl.place(relx=.0, rely=.0)
        btnt = Button(window, text="Name", height=3, width=25)
        btnt.place(relx=.25, rely=.0)
        btnt = Button(window, text="SpecializationName", height=3, width=25)
        btnt.place(relx=.5, rely=.0)
        btnt = Button(window, text="TeamPrice", height=3, width=25)
        btnt.place(relx=.75, rely=.0)
        cnt = 1
        h = .1
        b = False
        for txt in lst:
            if cnt % 3 != 0:
                if b:
                    cnt -=1
                    b = False
                lbl = Label(window, text=txt, font=("Times New Roman", 11))
                lbl.place(relx=(cnt - 1) * .25, rely=h)
                if cnt % 4 == 0 and cnt != 0:
                    cnt = 1
                    h += .05
                else:
                    cnt += 1
            else:
                cnt += 1
                b = True
    window.mainloop()


def gen(window):
    for widget in window.winfo_children():
        widget.destroy()
    nb = ttk.Notebook(window)
    nb.pack(fill='both', expand='yes')
    l = []
    for f in t:
        if not ('view' in f or '1' in f):
            l.append(f)
            f1 = Frame(window)
            nb.add(f1, text=f)
            atr, data = get_attributes(f)
            for i in range(len(atr)):
                lbl = Button(f1, text=atr[i], height=1, width=13, font=("Times New Roman", 12))
                lbl.place(relx=i * .1, rely=.01)
                cnt = 0
                for j in range(i, len(data), len(atr)):
                    lbl = Label(f1, text=data[j], font=("Times New Roman", 12))
                    lbl.place(relx=i * .1, rely=.05 + cnt * .05)
                    cnt += 1
    mainmenu = Menu(window)
    window.config(menu=mainmenu)
    mainmenu.add_command(label='Add an entry', command=lambda: insert(l))
    mainmenu.add_command(label='Delete an entry', command=lambda: delet(l))
    mainmenu.add_command(label='Update an entry', command=lambda: update(l))
    mainmenu.add_command(label='Refresh', command=lambda: gen(window))


def tables():
    window = Tk()
    window.title("Tables")
    window.geometry('1240x900')
    gen(window)
    window.mainloop()


def view():
    window = Tk()
    window.title("Views")
    window.geometry('1240x900')
    nb = ttk.Notebook(window)
    nb.pack(fill='both', expand='yes')
    for f in t:
        if 'view' in f and not('emp' in f):
            f1 = Frame(window)
            nb.add(f1, text=f)
            atr, data = get_attributes(f)
            for i in range(len(atr)):
                lbl = Button(f1, text=atr[i], height=1, width=13, font=("Times New Roman", 12))
                lbl.place(relx=i * .1, rely=.01)
                cnt = 0
                for j in range(i, len(data), len(atr)):
                    lbl = Label(f1, text=data[j], font=("Times New Roman", 12))
                    lbl.place(relx=i * .1, rely=.05 + cnt * .05)
                    cnt += 1
    window.mainloop()


def insert(l):
    window = Tk()
    window.title("Add an entry")
    window.geometry('900x500')
    combo = ttk.Combobox(window, height=30, width=30)
    combo['values'] = l
    combo.place(relx=.1, rely=.05)
    combo.bind("<<ComboboxSelected>>", lambda x: add(combo.get(), window))
    window.mainloop()


def delet(l):
    window = Tk()
    window.title("Delete an entry")
    window.geometry('300x300')
    combo = ttk.Combobox(window, height=30, width=30)
    combo['values'] = l
    combo.place(relx=.15, rely=.05)
    txt = Entry(window, width=40)
    txt.place(relx=.05, rely=.5)
    b = Button(window, text='Enter', height=1, width=13, font=("Times New Roman", 12), command=lambda: d(combo.get(), txt.get()))
    b.place(relx=.25, rely=.8)
    lbl = Label(window, text='Enter the deletion condition', font=("Times New Roman", 12))
    lbl.place(relx=.2, rely=.35)
    window.mainloop()


def update(l):
    window = Tk()
    window.title("Delete an entry")
    window.geometry('300x300')
    combo = ttk.Combobox(window, height=30, width=30)
    combo['values'] = l
    combo.place(relx=.15, rely=.05)
    txt = Entry(window, width=40)
    txt.place(relx=.05, rely=.6)
    lbl = Label(window, text='Enter the update condition', font=("Times New Roman", 12))
    lbl.place(relx=.2, rely=.5)
    lbl = Label(window, text='Enter what you want to update', font=("Times New Roman", 12))
    lbl.place(relx=.2, rely=.2)
    txtu = Entry(window, width=40)
    txtu.place(relx=.05, rely=.3)
    b = Button(window, text='Enter', height=1, width=13, font=("Times New Roman", 12),
               command=lambda: u(combo.get(), txt.get(), txtu.get()))
    b.place(relx=.25, rely=.8)
    window.mainloop()


def u(s, cond, set):
    cursor = connection.cursor()
    cursor.execute(f"""UPDATE {s} SET {set} WHERE {cond};""").fetchone()
    cursor.close()


def d(s, cond):
    cursor = connection.cursor()
    cursor.execute(f"""DELETE FROM {s} WHERE {cond};""").fetchone()
    cursor.close()


def add(s, window):
    print(s)
    if s != '':
        text = []
        b = False
        for widget in window.winfo_children():
            if b:
                widget.destroy()
            b = True
        atr, data = get_attributes(s)
        for i in range(len(atr)):
            lbl = Button(window, text=atr[i], height=1, width=13, font=("Times New Roman", 12))
            lbl.place(relx=i * .123, rely=.15)
            txt = Entry(window, width=20)
            txt.place(relx=i * .123, rely=.25)
            text.append(txt)
        lbl = Button(window, text='Enter', height=1, width=13, font=("Times New Roman", 12), command=lambda:ins(s, text, atr))
        lbl.place(relx=.4, rely=.35)


def ins(s, text, atr):
    t = []
    n = "("
    for i in range(len(text)):
        arg = text[i].get()
        if not(check_attr_type(connection, s, atr[i], "date") or check_attr_type(connection, s, atr[i], "varchar")):
            arg = int(arg)
        if i != (len(text) - 1):
            n += ' ' + atr[i] + ','
        else:
            n += ' ' + atr[i]
        t.append(arg)
    n += ')'
    print(str(tuple(t)))
    cursor = connection.cursor()
    print(f"""INSERT INTO {s} {n} VALUES {str(tuple(t))};""")
    if not(s == 'TeamSpecialization' or s == 'CompositionOfTeam' or s=='TeamProjects' or s == 'TaskEmployees'):
        cursor.execute(f"""SET IDENTITY_INSERT {s} ON; INSERT INTO {s} {n} VALUES {str(tuple(t))}; SET IDENTITY_INSERT {s} OFF;""").fetchone()
    else:
        cursor.execute(f"""INSERT INTO {s} {n} VALUES {str(tuple(t))};""").fetchone()
    cursor.close()


if __name__ == "__main__":
    welcome()
