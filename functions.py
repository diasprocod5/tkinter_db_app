from tkinter import *


def update_button(btn, text, command):
    btn.config(text=text,command=command)

def clear_entry(log_entry, pass_entry):
    log_entry.delete(0, END)
    pass_entry.delete(0, END)
