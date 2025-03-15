from tkinter import *
from functions import clear_entry

from database import connect_to_db, close_db_connection



connection = None

def connect():
    global connection
    login = log_entry.get()
    password = pass_entry.get()
    if login and password:
        connection = connect_to_db(login,password)
        if connection:
            clear_entry(log_entry, pass_entry)
    else:
        print("Введите логин и пароль")

def disconnect():
    global connection
    close_db_connection(connection)
    connection = None





root = Tk()
root.title("Application")
root.geometry("550x700")
root.config(bg='lightgrey')



log_entry = Entry(root)
pass_entry = Entry(root)
log_btn = Button(root, text='Вход', command=connect)
logout_btn = Button(root,text='Выход', command=disconnect)

log_entry.place(x=20, y=20, width=100)
pass_entry.place(x=130, y=20,width=100)
log_btn.place(x=240, y=20,width=50, height=20)
logout_btn.place(x=300, y=20, width=50, height=20)











root.mainloop()







