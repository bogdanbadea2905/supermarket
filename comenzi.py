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
        cursor.execute('SELECT * FROM Comenzi')
        comenzi_records = cursor.fetchall()
        for record in comenzi_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()

def add_comanda(comandaID, dataComanda, pret, adresaFacturare, furnizorID, managerID):
    if (comandaID == '' or dataComanda == '' or pret == '' or adresaFacturare == '' or furnizorID == '' or managerID == ''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT ComandaID FROM Comenzi WHERE ComandaID=?', (comandaID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Comenzi VALUES (?,?,?,?,?,?)', (comandaID, dataComanda, pret, adresaFacturare, furnizorID, managerID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(comandaID, dataComanda, pret, adresaFacturare, furnizorID, managerID):
    comandaID.delete(0,END)
    dataComanda.delete(0, END)
    pret.delete(0, END)
    adresaFacturare.delete(0,END)
    furnizorID.delete(0,END)
    managerID.delete(0,END)

def select_comanda(event, comandaID, dataComanda, pret, adresaFacturare, furnizorID, managerID):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(comandaID, dataComanda, pret, adresaFacturare, furnizorID, managerID)
    comandaID.insert(0, row[0])
    dataComanda.insert(0, row[1])
    pret.insert(0, row[2])
    adresaFacturare.insert(0, row[3])
    furnizorID.insert(0, row[4])
    managerID.insert(0, row[5])

def update_comanda(comandaID, dataComanda, pret, adresaFacturare, furnizorID, managerID):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Comenzi WHERE ComandaID=?', (comandaID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (dataComanda, float(pret), adresaFacturare, int(furnizorID), int(managerID))
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Comenzi SET dataComanda=?, pret=?, adresaFacturare=?, furnizorID=?, managerID=?'
                        'WHERE comandaID = ?', (dataComanda, pret, adresaFacturare, furnizorID, managerID, comandaID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def delete_comanda(comandaID):
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
                cursor.execute('DELETE FROM Comenzi WHERE ComandaID=?', (comandaID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def calcul_cost():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        interogare_treeview.delete(*interogare_treeview.get_children())
        query = """SELECT strftime('%Y-%m', C.DataComanda) AS Luna, SUM(P.PretUnitar * PC.Cantitate) AS Costuri
                    FROM Comenzi C
                    JOIN ProduseComenzi PC ON C.ComandaID = PC.ComandaID
                    JOIN Produse P ON PC.ProdusID = P.ProdusID
                    GROUP BY strftime('%Y-%m', C.DataComanda)"""
        cursor.execute(query)
        cost_records = cursor.fetchall()
        for record in cost_records:
            interogare_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la: {e}')
    finally:
        cursor.close()
        conn.close()

def afiseaza_comenzi():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    
    try:
        query = """
            SELECT C.ComandaId, P.NumeProdus, F.NumeFurnizor
            FROM Comenzi C
            JOIN ProduseComenzi PC ON C.ComandaId = PC.ComandaId
            JOIN Produse P ON PC.ProdusId = P.ProdusId
            JOIN Furnizori F ON C.FurnizorId = F.FurnizorId
            ORDER BY C.ComandaId;
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

def form_comenzi(root):

    global back_image, treeview, interogare_treeview
        
    frame_comenzi = Frame(root,width=1070, height=567)
    frame_comenzi.place(x=200, y=100)

    headingLabel = Label(frame_comenzi, text='Detalii Comenzi', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_comenzi, image=back_image, bd=0, cursor='hand2', command=lambda: frame_comenzi.place_forget())
    buton_back.place(x=10, y=30)

    comenzi_buton = Button(frame_comenzi, text='AfisareComenzi', font=('times new roman', 12), width=10, cursor='hand2',
                           command=lambda: afiseaza_comenzi())
    comenzi_buton.place(x = 200, y=30)

    cost_buton = Button(frame_comenzi, text='Calcul Cost', font=('times new roman', 12), width=10, cursor='hand2',
                        command=lambda: calcul_cost())
    cost_buton.place(x=500, y=30)

    top_frame = Frame(frame_comenzi)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('ComandaID','DataComanda', 'Pret', 'AdresaFacturare', 'FurnizorID', 'ManagerID'), show='headings')

    treeview.pack()
    treeview.heading('ComandaID', text='ComandaID')
    treeview.heading('DataComanda', text='DataComanda')
    treeview.heading('Pret', text='Pret')
    treeview.heading('AdresaFacturare', text='AdresaFacturare')
    treeview.heading('FurnizorID', text='FurnizorID')
    treeview.heading('ManagerID', text='ManagerID')

    detail_frame = Frame(frame_comenzi)
    detail_frame.place(x = 0, y = 300)

    ComandaID_label = Label(detail_frame, text='ComandaID', font=('times new roman', 12))
    ComandaID_label.grid(row=0, column=0)
    ComandaID_entry = Entry(detail_frame)
    ComandaID_entry.grid(row=0, column=1)

    DataComanda_label = Label(detail_frame, text='DataComanda', font=('times new roman', 12))
    DataComanda_label.grid(row=1, column=0)
    DataComanda_entry = Entry(detail_frame)
    DataComanda_entry.grid(row=1, column=1)

    Pret_label = Label(detail_frame, text='Pret', font=('times new roman', 12))
    Pret_label.grid(row=2, column=0)
    Pret_entry = Entry(detail_frame)
    Pret_entry.grid(row=2, column=1)

    AdresaFacturare_label = Label(detail_frame, text='AdresaFacturare', font=('times new roman', 12))
    AdresaFacturare_label.grid(row=3, column=0)
    AdresaFacturare_entry = Entry(detail_frame)
    AdresaFacturare_entry.grid(row=3, column=1)

    FurnizorId_label = Label(detail_frame, text='FurnizorID', font=('times new roman', 12))
    FurnizorId_label.grid(row=4, column=0)
    FurnizorId_entry = Entry(detail_frame)
    FurnizorId_entry.grid(row=4, column=1)
        
    ManagerId_label = Label(detail_frame, text='ManagerID', font=('times new roman', 12))
    ManagerId_label.grid(row=5, column=0)
    ManagerId_entry = Entry(detail_frame)
    ManagerId_entry.grid(row=5, column=1)

    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_comanda(ComandaID_entry.get(), DataComanda_entry.get(), Pret_entry.get(), AdresaFacturare_entry.get(), 
                                                                                                                                      FurnizorId_entry.get(), ManagerId_entry.get()))
    add_button.grid(row=6, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: update_comanda(ComandaID_entry.get(), DataComanda_entry.get(), Pret_entry.get(), AdresaFacturare_entry.get(), 
                                                                                                                                            FurnizorId_entry.get(), ManagerId_entry.get()))
    update_button.grid(row=6, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_comanda(ComandaID_entry.get()))
    delete_button.grid(row=6, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_comanda(event, ComandaID_entry, DataComanda_entry, Pret_entry,
                                                                AdresaFacturare_entry, FurnizorId_entry, ManagerId_entry))

    treeview_date()

    frame_interogare = Frame(frame_comenzi)
    frame_interogare.place(x=500, y=300, width=500, height=200)
    Label(frame_interogare, text='Costuri Lunare', font=('times new roman', 12, 'bold')).pack()

    interogare_treeview = ttk.Treeview(frame_interogare, columns=('Luna', 'Cost'),
                                       show='headings')
    interogare_treeview.pack()

    interogare_treeview.heading('Luna', text='Luna')
    interogare_treeview.heading('Cost', text='Cost')
