from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def conectare_bd():
    try:
        conn = sqlite3.connect('Supermarket.db')
        cursor = conn.cursor()
    except:
        messagebox.showerror('Eroare', 'Probleme la conectarea la baza de date!')
        return None, None
    
    return cursor, conn

def treeview_date():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        manageri_treeview.delete(*manageri_treeview.get_children())
        cursor.execute('SELECT * FROM Manageri')
        manageri_records = cursor.fetchall()
        for record in manageri_records:
            manageri_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()

def add_manager(managerID, nume, prenume, email, parola):
    if (managerID == '' or nume == '' or prenume == '' or email == '' or parola == ''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT ManagerID FROM Manageri WHERE ManagerID=?', (managerID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('SELECT Email FROM Manageri WHERE Email=?', (email,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Email-ul deja exista')
                return
            cursor.execute('INSERT INTO Manageri VALUES (?,?,?,?,?)', (managerID, nume, prenume, email, parola))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()


def clear_fields(managerID, nume, prenume, email, parola):
    managerID.delete(0,END)
    nume.delete(0, END)
    prenume.delete(0, END)
    email.delete(0,END)
    parola.delete(0,END)


def select_manager(event, managerID, nume, prenume, email, parola):
    index = manageri_treeview.selection()
    content = manageri_treeview.item(index)
    row = content['values']
    clear_fields(managerID, nume, prenume, email, parola)
    managerID.insert(0, row[0])
    nume.insert(0, row[1])
    prenume.insert(0, row[2])
    email.insert(0, row[3])
    parola.insert(0, row[4])

def update_manager(managerID, nume, prenume, email, parola):
    selected = manageri_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Manageri WHERE ManagerID=?', (managerID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (nume, prenume, email, parola)
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Manageri SET nume=?, prenume=?, email=?, parola=?'
                        'WHERE managerID = ?', (nume, prenume, email, parola, managerID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def delete_manager(managerID):
    selected = manageri_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        result = messagebox.askyesno('Confirm', 'Sunteti sigur ca vreti sa stergeti acest manager?')
        if result:
            cursor, conn = conectare_bd()
            if not cursor or not conn:
                return
            try:
                cursor.execute('DELETE FROM Manageri WHERE ManagerID=?', (managerID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def top3_manageri():

    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        interogare_treeview.delete(*interogare_treeview.get_children())
        query = """SELECT M.Nume, M.Prenume, COUNT(C.ComandaID) AS NrComenzi, F.NumeFurnizor
                    FROM Manageri M
                    JOIN Comenzi C ON C.ManagerID = M.ManagerID
                    JOIN Furnizori F ON F.FurnizorID = C.FurnizorID
                    GROUP BY M.Nume, M.Prenume, F.NumeFurnizor
                    ORDER BY COUNT(C.ComandaID) DESC
                    LIMIT 3"""
        cursor.execute(query)
        top3_records = cursor.fetchall()
        for record in top3_records:
            interogare_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la: {e}')
    finally:
        cursor.close()
        conn.close()


def form_manageri(root):
    global back_image, manageri_treeview, interogare_treeview
    frame_manageri = Frame(root,width=1070, height=567)
    frame_manageri.place(x=200, y=100)

    headingLabel = Label(frame_manageri, text='Detalii Manageri', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_manageri, image=back_image, bd=0, cursor='hand2', command=lambda: frame_manageri.place_forget())
    buton_back.place(x=10, y=30)

    top3_buton = Button(frame_manageri, text='Top3', font=('times new roman', 12), width=10, cursor='hand2',
                        command=lambda: top3_manageri())
    top3_buton.place(x=500, y=30)

    top_frame = Frame(frame_manageri)
    top_frame.place(x=0, y=70, relwidth=1, height=235)

    manageri_treeview = ttk.Treeview(top_frame, columns=('ManagerID', 'Nume', 'Prenume', 'Email', 'Parola'), show='headings')
    manageri_treeview.pack(pady=10)

    manageri_treeview.heading('ManagerID', text='ManagerID')
    manageri_treeview.heading('Nume', text='Nume')
    manageri_treeview.heading('Prenume', text='Prenume')
    manageri_treeview.heading('Email', text='Email')
    manageri_treeview.heading('Parola', text='Parola')

    detail_frame = Frame(frame_manageri)
    detail_frame.place(x=0, y=300)
    
    ManagerID_label = Label(detail_frame, text='ManagerID', font=('times new roman', 12))
    ManagerID_label.grid(row=0, column=0)
    ManagerID_entry = Entry(detail_frame)
    ManagerID_entry.grid(row=0, column=1)

    Nume_label = Label(detail_frame, text='Nume', font=('times new roman', 12))
    Nume_label.grid(row=1, column=0)
    Nume_entry = Entry(detail_frame)
    Nume_entry.grid(row=1, column=1)

    Prenume_label = Label(detail_frame, text='Prenume', font=('times new roman', 12))
    Prenume_label.grid(row=2, column=0)
    Prenume_entry = Entry(detail_frame)
    Prenume_entry.grid(row=2, column=1)

    Email_label = Label(detail_frame, text='Email', font=('times new roman', 12))
    Email_label.grid(row=3, column=0)
    Email_entry = Entry(detail_frame)
    Email_entry.grid(row=3, column=1)

    Parola_label = Label(detail_frame, text='Parola', font=('times new roman', 12))
    Parola_label.grid(row=4, column=0)
    Parola_entry = Entry(detail_frame)
    Parola_entry.grid(row=4, column=1)


    add_button = Button(detail_frame, text='Salveaza', font=('times new roman', 12), width=10, cursor='hand2', 
                        command=lambda: add_manager(ManagerID_entry.get(), Nume_entry.get(), Prenume_entry.get(),
                                            Email_entry.get(), Parola_entry.get()))
    add_button.grid(row=5, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 12), width=10, cursor='hand2', command=lambda: update_manager(ManagerID_entry.get(), Nume_entry.get(), Prenume_entry.get(),
                                                                                                                                Email_entry.get(), Parola_entry.get()))
    update_button.grid(row=5, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 12), width=10, cursor='hand2', command=lambda: delete_manager(ManagerID_entry.get()))
    delete_button.grid(row=5, column=2, padx=20)

    manageri_treeview.bind('<ButtonRelease-1>',lambda event: select_manager(event, ManagerID_entry, Nume_entry, Prenume_entry,
                                                                Email_entry, Parola_entry))
    
    treeview_date()

    frame_interogare = Frame(frame_manageri)
    frame_interogare.place(x=500, y=300, width=500, height=200)
    Label(frame_interogare, text='TOP3 Manageri', font=('times new roman', 12, 'bold')).pack()

    interogare_treeview = ttk.Treeview(frame_interogare, columns=('Nume', 'Prenume', 'NrComenzi', 'NumeFurnizor'),
                                       show='headings')
    interogare_treeview.pack()

    interogare_treeview.heading('Nume', text='Nume')
    interogare_treeview.heading('Prenume', text='Prenume')
    interogare_treeview.heading('NrComenzi', text='NrComenzi')
    interogare_treeview.heading('NumeFurnizor', text='NumeFurnizor')
    