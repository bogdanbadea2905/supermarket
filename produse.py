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
        cursor.execute('SELECT * FROM Produse')
        produse_records = cursor.fetchall()
        for record in produse_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()

def add_produs(produsID, numeProdus, pretUnitar, dataValabilitate, categorieID):
    if (produsID == '' or numeProdus == '' or pretUnitar == '' or categorieID == ''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii (mai putin dataValabilitate)!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT ProdusID FROM Produse WHERE ProdusID=?', (produsID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Produse VALUES (?,?,?,?,?)', (produsID, numeProdus, pretUnitar, dataValabilitate, categorieID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(produsID, numeProdus, pretUnitar, dataValabilitate, categorieID):
    produsID.delete(0,END)
    numeProdus.delete(0, END)
    pretUnitar.delete(0, END)
    dataValabilitate.delete(0,END)
    categorieID.delete(0,END)

def select_produs(event, produsID, numeProdus, pretUnitar, dataValabilitate, categorieID):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(produsID, numeProdus, pretUnitar, dataValabilitate, categorieID)
    produsID.insert(0, row[0])
    numeProdus.insert(0, row[1])
    pretUnitar.insert(0, row[2])
    dataValabilitate.insert(0, row[3])
    categorieID.insert(0, row[4])

def update_produs(produsID, numeProdus, pretUnitar, dataValabilitate, categorieID):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Produse WHERE ProdusID=?', (produsID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            print(current_data)
            new_data = (numeProdus, float(pretUnitar), dataValabilitate, int(categorieID))
            print(new_data)
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Produse SET numeProdus=?, pretUnitar=?, dataValabilitate=?, categorieID=?'
                        'WHERE produsID = ?', (numeProdus, pretUnitar, dataValabilitate, categorieID, produsID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def delete_produs(produsID):
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
                cursor.execute('DELETE FROM Produse WHERE produsID=?', (produsID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def produse_medie():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        interogare_treeview.delete(*interogare_treeview.get_children())
        query = """SELECT P.NumeProdus, P.PretUnitar, C.NumeCategorie
                    FROM Produse P, Categorii C
                    WHERE P.CategorieID = C.CategorieID AND
                    P.PretUnitar > 
                        (SELECT AVG(PretUnitar)
                        FROM Produse
                        WHERE C.CategorieID = Produse.CategorieID)"""
        cursor.execute(query)
        stoc_records = cursor.fetchall()
        for record in stoc_records:
            interogare_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la: {e}')
    finally:
        cursor.close()
        conn.close()

def form_produse(root):

    global back_image, treeview, interogare_treeview
        
    frame_produse = Frame(root,width=1070, height=567)
    frame_produse.place(x=200, y=100)

    headingLabel = Label(frame_produse, text='Detalii Produse', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_produse, image=back_image, bd=0, cursor='hand2', command=lambda: frame_produse.place_forget())
    buton_back.place(x=10, y=30)

    stoc_buton = Button(frame_produse, text='Produse Medie', font=('times new roman', 12), width=10, cursor='hand2',
                        command=lambda: produse_medie())
    stoc_buton.place(x=500, y=30)

    top_frame = Frame(frame_produse)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('ProdusID','NumeProdus', 'Pret_Unitar', 'Data_Valabilitate', 'CategorieID'), show='headings')

    treeview.pack()
    treeview.heading('ProdusID', text='ProdusID')
    treeview.heading('NumeProdus', text='NumeProdus')
    treeview.heading('Pret_Unitar', text='Pret_Unitar')
    treeview.heading('Data_Valabilitate', text='Data_Valabilitate')
    treeview.heading('CategorieID', text='CategorieID')

    detail_frame = Frame(frame_produse)
    detail_frame.place(x = 0, y = 300)

    ProdusID_label = Label(detail_frame, text='ProdusID', font=('times new roman', 12))
    ProdusID_label.grid(row=0, column=0)
    ProdusID_entry = Entry(detail_frame)
    ProdusID_entry.grid(row=0, column=1)

    NumeProdus_label = Label(detail_frame, text='NumeProdus', font=('times new roman', 12))
    NumeProdus_label.grid(row=1, column=0)
    NumeProdus_entry = Entry(detail_frame)
    NumeProdus_entry.grid(row=1, column=1)

    Pret_Unitar_label = Label(detail_frame, text='Pret_Unitar', font=('times new roman', 12))
    Pret_Unitar_label.grid(row=2, column=0)
    Pret_Unitar_entry = Entry(detail_frame)
    Pret_Unitar_entry.grid(row=2, column=1)

    Data_Valabilitate_label = Label(detail_frame, text='Data_Valabilitate', font=('times new roman', 12))
    Data_Valabilitate_label.grid(row=3, column=0)
    Data_Valabilitate_entry = Entry(detail_frame)
    Data_Valabilitate_entry.grid(row=3, column=1)

    CategorieID_label = Label(detail_frame, text='CategorieID', font=('times new roman', 12))
    CategorieID_label.grid(row=4, column=0)
    CategorieID_entry = Entry(detail_frame)
    CategorieID_entry.grid(row=4, column=1)
    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_produs(ProdusID_entry.get(), NumeProdus_entry.get(),
                                                                                                                                      Pret_Unitar_entry.get(), Data_Valabilitate_entry.get(), CategorieID_entry.get()))
    add_button.grid(row=5, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: update_produs(ProdusID_entry.get(), NumeProdus_entry.get(),Pret_Unitar_entry.get(), Data_Valabilitate_entry.get(), CategorieID_entry.get()))
    update_button.grid(row=5, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_produs(ProdusID_entry.get()))
    delete_button.grid(row=5, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_produs(event, ProdusID_entry, NumeProdus_entry, Pret_Unitar_entry,
                                                                Data_Valabilitate_entry, CategorieID_entry))
    treeview_date()

    frame_interogare = Frame(frame_produse)
    frame_interogare.place(x=500, y=300, width=500, height=200)
    Label(frame_interogare, text='Produse mai scumpe decat medie', font=('times new roman', 12, 'bold')).pack()

    interogare_treeview = ttk.Treeview(frame_interogare, columns=('NumeProdus', 'PretUnitar', 'NumeCategorie'),
                                       show='headings')
    interogare_treeview.pack()

    interogare_treeview.heading('NumeProdus', text='NumeProdus')
    interogare_treeview.heading('PretUnitar', text='PretUnitar')
    interogare_treeview.heading('NumeCategorie', text='NumeCategorie')