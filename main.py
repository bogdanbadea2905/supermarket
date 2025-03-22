from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from manageri import form_manageri, conectare_bd, add_manager
from furnizori import form_furnizori
from produse import form_produse
from categorii import form_categorii
from comenzi import form_comenzi
from livrari import form_livrari
from livratori import form_livratori
from sedii import form_sedii
import datetime

def login():
    email = email_entry.get()
    password = parola_entry.get()

    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return

    cursor.execute('SELECT * FROM Manageri WHERE Email = ? AND Parola = ?', (email, password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo('Succes', 'Autentificare reusita!')
        login_window.destroy()
        main_window()
    else:
        messagebox.showerror('Eroare', 'Email sau parola incorecte!')

    cursor.close()
    conn.close()

def update_time():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%d-%m-%Y \t\t Time: %I:%M:%S %p")
    subtitleLabel.config(text=f"Bine ati venit! \t\t Date: {formatted_time}")
    root.after(1000, update_time)

def logout():
    global root
    root.destroy()
    open_login_window()

def register():
    register_window = Toplevel(login_window)
    register_window.title('Inregistrare')
    register_window.geometry('400x400')
    register_window.resizable(0, 0)

    Label(register_window, text='ID', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    id_entry = Entry(register_window, font=('Times New Roman', 12))
    id_entry.pack(pady=5)

    Label(register_window, text='Nume', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    nume_entry = Entry(register_window, font=('Times New Roman', 12))
    nume_entry.pack(pady=5)

    Label(register_window, text='Prenume', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    prenume_entry = Entry(register_window, font=('Times New Roman', 12))
    prenume_entry.pack(pady=5)

    Label(register_window, text='Email', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    email_entry_reg = Entry(register_window, font=('Times New Roman', 12))
    email_entry_reg.pack(pady=5)

    Label(register_window, text='Parola', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    parola_entry_reg = Entry(register_window, font=('Times New Roman', 12), show='*')
    parola_entry_reg.pack(pady=5)

    def save_user():
        id = id_entry.get()
        nume = nume_entry.get()
        prenume = prenume_entry.get()
        email = email_entry_reg.get()
        parola = parola_entry_reg.get()

        if id=='' or nume == '' or prenume == '' or email == '' or parola == '':
            messagebox.showerror('Eroare', 'Toate campurile sunt obligatorii!')
            return

        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return

        cursor.execute('SELECT * FROM Manageri WHERE Email = ?', (email,))
        if cursor.fetchone():
            messagebox.showerror('Eroare', 'Email-ul exista deja!')
            cursor.close()
            conn.close()
            return
        cursor.execute('SELECT ManagerID FROM Manageri WHERE ManagerID=?', (id,))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Id-ul exista deja')
            cursor.close()
            conn.close()
            return

        cursor.execute('INSERT INTO Manageri (ManagerId, Nume, Prenume, Email, Parola) VALUES (?, ?, ?, ?, ?)', (id, nume, prenume, email, parola))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo('Succes', 'Inregistrare reusita!')
        register_window.destroy()

    register_button = Button(register_window, text='Register', font=('Times New Roman', 14, 'bold'), command=save_user)
    register_button.pack(pady=10)

def main_window():
    global root, subtitleLabel
    root = Tk()

    root.title('Supermarket')
    root.geometry('1440x900+0+0')
    root.resizable(0,0)

    bg_image = PhotoImage(file='inventory.png')
    titleLabel = Label(root,image=bg_image, compound=LEFT,text='Evidenta Marfurilor', font=('times new roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
    titleLabel.place(x=0,y=0, relwidth=1)

    logoutButton = Button(root, text='Logout', font=('times new roman', 20, 'bold'), fg='#010c48', command=lambda: logout())
    logoutButton.place(x=1100, y=10)

    subtitleLabel = Label(root, text='Welcome Admin \t\t', font=('times new roman', 15), bg='#4d636d', fg='white')
    subtitleLabel.place(x=0, y=70, relwidth=1)

    leftFrame = Frame(root)
    leftFrame.place(x=0, y=102, width=200, height=600)

    logoImage = PhotoImage(file='checklist.png')
    imageLabel = Label(leftFrame, image=logoImage)
    imageLabel.pack()

    menuLabel = Label(leftFrame, text='Meniu', font=('times new roman', 20), bg='#009688')
    menuLabel.pack(fill=X)

    buton_manageri = Button(leftFrame, text='Manageri', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command= lambda: form_manageri(root))
    buton_manageri.pack(fill=X)

    buton_furnizori = Button(leftFrame, text='Furnizori', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_furnizori(root))
    buton_furnizori.pack(fill=X)

    buton_produse = Button(leftFrame, text='Produse', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_produse(root))
    buton_produse.pack(fill=X)

    buton_categorii = Button(leftFrame, text='Categorii', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_categorii(root))
    buton_categorii.pack(fill=X)

    buton_comenzi= Button(leftFrame, text='Comenzi', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_comenzi(root))
    buton_comenzi.pack(fill=X)

    buton_livrari = Button(leftFrame, text='Livrari', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_livrari(root))
    buton_livrari.pack(fill=X)

    buton_livratori = Button(leftFrame, text='Livratori', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_livratori(root))
    buton_livratori.pack(fill=X)

    buton_sedii = Button(leftFrame, text='Sedii', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=lambda: form_sedii(root))
    buton_sedii.pack(fill=X)

    buton_exit = Button(leftFrame, text='Exit', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command=root.destroy)
    buton_exit.pack(fill=X)

    right_frame = Frame(root)
    right_frame.place(x=500,y=100)

    supermarket_img = PhotoImage(file='supermarket.png')
    supermarket_label = Label(right_frame, image=supermarket_img)
    supermarket_label.pack()

    update_time()

    root.mainloop()


def open_login_window():

    global login_window, email_entry, parola_entry

    login_window = Tk()
    login_window.title('Autentificare')
    login_window.geometry('400x300')
    login_window.resizable(0, 0)

    Label(login_window, text='Email', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    email_entry = Entry(login_window, font=('Times New Roman', 12))
    email_entry.pack(pady=5)

    Label(login_window, text='Parola', font=('Times New Roman', 14, 'bold')).pack(pady=5)
    parola_entry = Entry(login_window, font=('Times New Roman', 12), show='*')
    parola_entry.pack(pady=5)

    button_frame = Frame(login_window)
    button_frame.pack(pady=10)

    login_button = Button(button_frame, text='Login', font=('Times New Roman', 14, 'bold'), command=login)
    login_button.pack(side='left', padx=10)

    register_button = Button(button_frame, text='Register', font=('Times New Roman', 14, 'bold'), command=register)
    register_button.pack(side='right', padx=10)

    exit_button = Button(button_frame, text='Exit', font=('Times New Roman', 14, 'bold'), command=login_window.destroy)
    exit_button.pack(side='right', padx=10)

    login_window.mainloop()

open_login_window()
