from tkinter import *
from tkinter import ttk
from manageri import conectare_bd
from tkinter import messagebox

def treeview_date():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        treeview.delete(*treeview.get_children())
        cursor.execute('SELECT * FROM Livratori')
        livratori_records = cursor.fetchall()
        for record in livratori_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()

def add_livrator(livratorID, numeLivrator, prenume, telefon, email):
    if (livratorID == '' or numeLivrator == '' or prenume == '' or telefon == '' or email == ''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT LivratorID FROM Livratori WHERE LivratorID=?', (livratorID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Livratori VALUES (?,?,?,?,?)', (livratorID, numeLivrator, prenume, telefon, email))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(livratorID, numeLivrator, prenume, telefon, email):
    livratorID.delete(0,END)
    numeLivrator.delete(0, END)
    prenume.delete(0, END)
    telefon.delete(0,END)
    email.delete(0,END)

def select_livrator(event, livratorID, numeLivrator, prenume, telefon, email):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(livratorID, numeLivrator, prenume, telefon, email)
    livratorID.insert(0, row[0])
    numeLivrator.insert(0, row[1])
    prenume.insert(0, row[2])
    telefon.insert(0, row[3])
    email.insert(0, row[4])

def update_livrator(livratorID, numeLivrator, prenume, telefon, email):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Livratori WHERE LivratorID=?', (livratorID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            print(current_data)
            new_data = (numeLivrator, prenume, telefon, email)
            print(new_data)
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Livratori SET numeLivrator=?, prenumeLivrator=?, telefon=?, email=?'
                        'WHERE LivratorID = ?', (numeLivrator, prenume, telefon, email, livratorID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()
    
def delete_livrator(livratorID):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        result = messagebox.askyesno('Confirm', 'Sunteti sigur ca vreti sa stergeti acest manager?')
        if result:
            cursor, conn = conectare_bd()
            if not cursor or not conn:
                return
            try:
                cursor.execute('DELETE FROM Livratori WHERE LivratorID=?', (livratorID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def livratori_sedii():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        interogare_treeview.delete(*interogare_treeview.get_children())
        query = """SELECT L.NumeLivrator, L.PrenumeLivrator
                    FROM Livratori L
                    WHERE NOT EXISTS (
                        SELECT S.SediuID
                        FROM Sedii S
                        WHERE NOT EXISTS (
                            SELECT * FROM Livrari
                            WHERE Livrari.SediuID = S.SediuID AND Livrari.LivratorID = L.LivratorID
                        )
                    )"""
        cursor.execute(query)
        stoc_records = cursor.fetchall()
        for record in stoc_records:
            interogare_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la: {e}')
    finally:
        cursor.close()
        conn.close()

def afiseaza_livratori():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    
    try:
        query = """
            SELECT LV.LivratorId, LV.NumeLivrator, LV.PrenumeLivrator, S.NumeSediu, S.Locatie, COUNT(L.LivrareId) AS NumarLivrari
            FROM Livrari L
            JOIN Livratori LV ON L.LivratorId = LV.LivratorId
            JOIN Sedii S ON L.SediuId = S.SediuId
            GROUP BY LV.LivratorId, LV.NumeLivrator, LV.PrenumeLivrator, S.NumeSediu, S.Locatie
            ORDER BY NumarLivrari DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        treeview.delete(*treeview.get_children())

        for row in results:
            treeview.insert('', END, values=row)

    except Exception as e:
        messagebox.showerror('Error', f'Eroare la interogare: {e}')
    finally:
        cursor.close()
        conn.close()

def form_livratori(root):

    global back_image, treeview, interogare_treeview
        
    frame_livratori = Frame(root,width=1070, height=567)
    frame_livratori.place(x=200, y=100)

    headingLabel = Label(frame_livratori, text='Detalii Livratori', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_livratori, image=back_image, bd=0, cursor='hand2', command=lambda: frame_livratori.place_forget())
    buton_back.place(x=10, y=30)

    livratori_buton = Button(frame_livratori, text='AfisareLivratori', font=('times new roman', 12), width=10, cursor='hand2',
                           command=lambda: afiseaza_livratori())
    livratori_buton.place(x = 200, y=30)

    livrator_buton = Button(frame_livratori, text='LivratoriSedii', font=('times new roman', 12), width=10, cursor='hand2',
                        command=lambda: livratori_sedii())
    livrator_buton.place(x=500, y=30)

    top_frame = Frame(frame_livratori)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('LivratorID','NumeLivrator', 'Prenume', 'Telefon', 'Email'), show='headings')

    treeview.pack()
    treeview.heading('LivratorID', text='LivratorID')
    treeview.heading('NumeLivrator', text='NumeLivrator')
    treeview.heading('Prenume', text='Prenume')
    treeview.heading('Telefon', text='Telefon')
    treeview.heading('Email', text='Email')

    detail_frame = Frame(frame_livratori)
    detail_frame.place(x = 0, y = 300)

    LivratorID_label = Label(detail_frame, text='LivratorID', font=('times new roman', 12))
    LivratorID_label.grid(row=0, column=0)
    LivratorID_entry = Entry(detail_frame)
    LivratorID_entry.grid(row=0, column=1)

    NumeLivrator_label = Label(detail_frame, text='NumeLivrator', font=('times new roman', 12))
    NumeLivrator_label.grid(row=1, column=0)
    NumeLivrator_entry = Entry(detail_frame)
    NumeLivrator_entry.grid(row=1, column=1)

    Prenume_label = Label(detail_frame, text='Prenume', font=('times new roman', 12))
    Prenume_label.grid(row=2, column=0)
    Prenume_entry = Entry(detail_frame)
    Prenume_entry.grid(row=2, column=1)

    Telefon_label = Label(detail_frame, text='Telefon', font=('times new roman', 12))
    Telefon_label.grid(row=3, column=0)
    Telefon_entry = Entry(detail_frame)
    Telefon_entry.grid(row=3, column=1)

    Email_label = Label(detail_frame, text='Email', font=('times new roman', 12))
    Email_label.grid(row=4, column=0)
    Email_entry = Entry(detail_frame)
    Email_entry.grid(row=4, column=1)
        
    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_livrator(LivratorID_entry.get(), NumeLivrator_entry.get(), Prenume_entry.get(),
                                                                                                                                       Telefon_entry.get(), Email_entry.get()))
    add_button.grid(row=6, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: update_livrator(LivratorID_entry.get(), NumeLivrator_entry.get(), Prenume_entry.get(),
                                                                                                                                       Telefon_entry.get(), Email_entry.get()))
    update_button.grid(row=6, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_livrator(LivratorID_entry.get()))
    delete_button.grid(row=6, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_livrator(event, LivratorID_entry, NumeLivrator_entry, Prenume_entry,
                                                                Telefon_entry, Email_entry))

    treeview_date()

    frame_interogare = Frame(frame_livratori)
    frame_interogare.place(x=500, y=300, width=500, height=200)
    Label(frame_interogare, text='Livratori care au livrat in toate sediile', font=('times new roman', 12, 'bold')).pack()

    interogare_treeview = ttk.Treeview(frame_interogare, columns=('NumeLivrator', 'PrenumeLivrator'),
                                       show='headings')
    interogare_treeview.pack()

    interogare_treeview.heading('NumeLivrator', text='NumeLivrator')
    interogare_treeview.heading('PrenumeLivrator', text='PrenumeLivrator')