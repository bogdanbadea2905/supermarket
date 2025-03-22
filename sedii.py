from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from manageri import conectare_bd

def treeview_date():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        treeview.delete(*treeview.get_children())
        cursor.execute('SELECT * FROM Sedii')
        sedii_records = cursor.fetchall()
        for record in sedii_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()

def add_sediu(sediuID, numeSediu, locatie, capacitate):
    if (sediuID == '' or numeSediu == '' or locatie == '' or capacitate == ''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT SediuID FROM Sedii WHERE SediuID=?', (sediuID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Sedii VALUES (?,?,?,?)', (sediuID, numeSediu, locatie, capacitate))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(sediuID, numeSediu, locatie, capacitate):
    sediuID.delete(0,END)
    numeSediu.delete(0, END)
    locatie.delete(0, END)
    capacitate.delete(0,END)

def select_sediu(event, sediuID, numeSediu, locatie, capacitate):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(sediuID, numeSediu, locatie, capacitate)
    sediuID.insert(0, row[0])
    numeSediu.insert(0, row[1])
    locatie.insert(0, row[2])
    capacitate.insert(0, row[3])

def update_sediu(sediuID, numeSediu, locatie, capacitate):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Sedii WHERE SediuID=?', (sediuID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (numeSediu, locatie, int(capacitate))
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Sedii SET numeSediu=?, locatie=?, capacitate=?'
                        'WHERE SediuID = ?', (numeSediu, locatie, capacitate, sediuID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def delete_sediu(sediuID):
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
                cursor.execute('DELETE FROM Sedii WHERE SediuID=?', (sediuID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def stoc_sedii():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        interogare_treeview.delete(*interogare_treeview.get_children())
        query = """SELECT S.NumeSediu, P.NumeProdus, PS.NumarStoc
                    FROM Sedii S
                    JOIN ProduseSedii PS ON PS.SediuID = S.SediuID
                    JOIN Produse P ON P.ProdusID = PS.ProdusID"""
        cursor.execute(query)
        stoc_records = cursor.fetchall()
        for record in stoc_records:
            interogare_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la: {e}')
    finally:
        cursor.close()
        conn.close()

def form_sedii(root):

    global back_image, treeview, interogare_treeview
        
    frame_sedii = Frame(root,width=1070, height=567)
    frame_sedii.place(x=200, y=100)

    headingLabel = Label(frame_sedii, text='Detalii Sedii', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_sedii, image=back_image, bd=0, cursor='hand2', command=lambda: frame_sedii.place_forget())
    buton_back.place(x=10, y=30)

    stoc_buton = Button(frame_sedii, text='Disponibilitate', font=('times new roman', 12), width=10, cursor='hand2',
                        command=lambda: stoc_sedii())
    stoc_buton.place(x=500, y=30)

    top_frame = Frame(frame_sedii)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('SediuID','NumeSediu', 'Locatie', 'Capacitate'), show='headings')

    treeview.pack()
    treeview.heading('SediuID', text='SediuID')
    treeview.heading('NumeSediu', text='NumeSediu')
    treeview.heading('Locatie', text='Locatie')
    treeview.heading('Capacitate', text='Capacitate')

    detail_frame = Frame(frame_sedii)
    detail_frame.place(x = 0, y = 300)

    SediuID_label = Label(detail_frame, text='SediuID', font=('times new roman', 12))
    SediuID_label.grid(row=0, column=0)
    SediuID_entry = Entry(detail_frame)
    SediuID_entry.grid(row=0, column=1)

    NumeSediu_label = Label(detail_frame, text='NumeSediu', font=('times new roman', 12))
    NumeSediu_label.grid(row=1, column=0)
    NumeSediu_entry = Entry(detail_frame)
    NumeSediu_entry.grid(row=1, column=1)

    Locatie_label = Label(detail_frame, text='Locatie', font=('times new roman', 12))
    Locatie_label.grid(row=2, column=0)
    Locatie_entry = Entry(detail_frame)
    Locatie_entry.grid(row=2, column=1)

    Capacitate_label = Label(detail_frame, text='Capacitate', font=('times new roman', 12))
    Capacitate_label.grid(row=3, column=0)
    Capacitate_entry = Entry(detail_frame)
    Capacitate_entry.grid(row=3, column=1)
    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_sediu(SediuID_entry.get(), NumeSediu_entry.get(), Locatie_entry.get(), Capacitate_entry.get()))
    add_button.grid(row=6, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: update_sediu(SediuID_entry.get(), NumeSediu_entry.get(), Locatie_entry.get(), Capacitate_entry.get()))
    update_button.grid(row=6, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_sediu(SediuID_entry.get()))
    delete_button.grid(row=6, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_sediu(event, SediuID_entry, NumeSediu_entry, Locatie_entry,
                                                                Capacitate_entry))

    treeview_date()

    frame_interogare = Frame(frame_sedii)
    frame_interogare.place(x=500, y=300, width=500, height=200)
    Label(frame_interogare, text='Disponibilitate Sedii', font=('times new roman', 12, 'bold')).pack()

    interogare_treeview = ttk.Treeview(frame_interogare, columns=('NumeSediu', 'NumeProdus', 'NrStoc'),
                                       show='headings')
    interogare_treeview.pack()

    interogare_treeview.heading('NumeSediu', text='NumeSediu')
    interogare_treeview.heading('NumeProdus', text='NumeProdus')
    interogare_treeview.heading('NrStoc', text='NrStoc')