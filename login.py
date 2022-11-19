from tkinter import *
from tkinter import messagebox
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox

root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)

def signin():
    username=user.get()
    password=code.get()
    if username=='admin' and password=='1234':
        exec(open('AttendanceProject.py').read())
    else:
        messagebox.showerror("Invalid","Invalid data!")
def signin1():
    username=user.get()
    password=code.get()
    if username=='admin' and password=='1234':
        screen=Toplevel(root)
        screen.title("App")
        screen.geometry('925x500+300+200')
        screen.config(bg="white")
        Label(screen,text='Hello Student!',bg='#fff',font=('Calibri(Body)',50,'bold')).pack(expand=True)
        Button(screen, width=39, pady=10, text='Access to Home', bg='#57a1f8', fg='white', border=0, ).place(x=320,
                                                                                                            y=340)
        screen.mainloop()
    else:
        messagebox.showerror("Invalid","Invalid data!")


def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')


img = PhotoImage(file='login.png')
Label(root,image=img, bg='white').place(x=50,y=50)

frame=Frame(root,width=350, height=350, bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

user=Entry(frame,width=25, fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)


code=Entry(frame,width=25, fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)


Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

Button(frame,width=19,pady=7,text='Sign in as Student',bg='#57a1f8',fg='white',border=0,command=signin1).place(x=30,y=204)
label=Label(frame,text="Don't have an account?", fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

Button(frame,width=19,pady=7,text='Sign in as Administrator',bg='#57a1f8',fg='white',border=0,command=signin).place(x=195,y=204)

sign_up=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8')
sign_up.place(x=215,y=270)


root.mainloop()