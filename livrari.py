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
        cursor.execute('SELECT * FROM Livrari')
        livrari_records = cursor.fetchall()
        for record in livrari_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()


def add_livrare(livrareID, dataLivrare, adresaLivrareLivrare, sediuID, comandaID, livratorID):
    if (livrareID == '' or dataLivrare == '' or adresaLivrareLivrare == '' or sediuID == '' or comandaID == '' or livratorID ==''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT livrareID FROM Livrari WHERE livrareID=?', (livrareID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Livrari VALUES (?,?,?,?,?,?)', (livrareID, dataLivrare, adresaLivrareLivrare, sediuID, comandaID, livratorID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(livrareID, dataLivrare, adresaLivrareLivrare, sediuID, comandaID, livratorID):
    livrareID.delete(0,END)
    dataLivrare.delete(0, END)
    adresaLivrareLivrare.delete(0, END)
    sediuID.delete(0,END)
    comandaID.delete(0,END)
    livratorID.delete(0,END)

def select_livrare(event, livrareID, dataLivrare, adresaLivrareLivrare, sediuID, comandaID, livratorID):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(livrareID, dataLivrare, adresaLivrareLivrare, sediuID, comandaID, livratorID)
    livrareID.insert(0, row[0])
    dataLivrare.insert(0, row[1])
    adresaLivrareLivrare.insert(0, row[2])
    sediuID.insert(0, row[3])
    comandaID.insert(0, row[4])
    livratorID.insert(0, row[5])

def update_livrare(livrareID, dataLivrare, adresaLivrare, sediuID, comandaID, livratorID):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Livrari WHERE LivrareID=?', (livrareID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            print(current_data)
            new_data = (dataLivrare, adresaLivrare, int(sediuID), int(comandaID), int(livratorID))
            print(new_data)
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Livrari SET dataLivrare=?, adresaLivrare=?, sediuID=?, comandaID=?, livratorID=?'
                        'WHERE livrareID = ?', (dataLivrare, adresaLivrare, sediuID, comandaID, livratorID, livrareID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def delete_livrare(livrareID):
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
                cursor.execute('DELETE FROM Livrari WHERE LivrareID=?', (livrareID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def select_livrator(button):
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return

    try:
        cursor.execute("SELECT DISTINCT L.LivratorID, LV.NumeLivrator FROM Livrari L JOIN Livratori LV ON L.LivratorID = LV.LivratorID")
        livratori = cursor.fetchall()
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la incarcarea livratorilor: {e}')
        return
    finally:
        cursor.close()
        conn.close()

    top = Toplevel()
    top.title("Alege Livrator")
    top.geometry("300x400")
    
    frame = Frame(top)
    frame.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    listbox = Listbox(frame, font=('times new roman', 12), yscrollcommand=scrollbar.set)

    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)

    for livrator in livratori:
        listbox.insert(END, f"{livrator[0]} - {livrator[1]}")

    def on_select(event):
        selected = listbox.get(ACTIVE)
        button.config(text=selected)
        top.destroy()

    listbox.bind("<Double-Button-1>", on_select)

    top.mainloop()

def filtru_livrari(selected_value):
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        filtered_treeview.delete(*filtered_treeview.get_children())

        if selected_value:
            livratorID = selected_value.split(' - ')[0]  

            query = """SELECT L.LivrareID, L.DataLivrare, L.adresaLivrare, L.SediuID, C.Pret, LI.NumeLivrator 
                       FROM Livrari L
                       JOIN Livratori LI ON L.LivratorID = LI.LivratorID
                       JOIN Comenzi C ON C.ComandaID = L.ComandaID
                       WHERE L.LivratorID = ?"""
            cursor.execute(query, (livratorID,))
            filtered_records = cursor.fetchall()
            for record in filtered_records:
                filtered_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la filtrare: {e}')
    finally:
        cursor.close()
        conn.close()

def form_livrari(root):

    global back_image, treeview, filtered_treeview
        
    frame_livrari = Frame(root,width=1070, height=567)
    frame_livrari.place(x=200, y=100)

    headingLabel = Label(frame_livrari, text='Detalii Livrari', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_livrari, image=back_image, bd=0, cursor='hand2', command=lambda: frame_livrari.place_forget())
    buton_back.place(x=10, y=30)

    filtru_frame = Frame(frame_livrari)
    filtru_frame.place(x=80,y=40)

    filtru_label = Label(filtru_frame, text='Selecteaza Livrator:', font=('times new roman', 12))
    filtru_label.grid(row=0,column=0)

    livrator_buton = Button(filtru_frame, text='Alege Livratorul', font=('times new roman', 12),
                            command=lambda: select_livrator(livrator_buton))
    livrator_buton.grid(row=0, column=1, padx=10)

    filtru_buton = Button(filtru_frame, text='Filtreaza', font=('times new roman', 12), cursor='hand2',
                          command=lambda: filtru_livrari(livrator_buton.cget("text").split(' - ')[0] if ' - ' in livrator_buton.cget("text") else None))
    filtru_buton.grid(row=0, column=2, padx=10)

    top_frame = Frame(frame_livrari)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('LivrareID','DataLivrare', 'adresaLivrare', 'SediuID', 'ComandaID', 'LivratorID'), show='headings')

    treeview.pack()
    treeview.heading('LivrareID', text='LivrareID')
    treeview.heading('DataLivrare', text='DataLivrare')
    treeview.heading('adresaLivrare', text='adresaLivrare')
    treeview.heading('SediuID', text='SediuID')
    treeview.heading('ComandaID', text='ComandaID')
    treeview.heading('LivratorID', text='LivratorID')

    detail_frame = Frame(frame_livrari)
    detail_frame.place(x = 0, y = 300)

    LivrareID_label = Label(detail_frame, text='LivrareID', font=('times new roman', 12))
    LivrareID_label.grid(row=0, column=0)
    LivrareID_entry = Entry(detail_frame)
    LivrareID_entry.grid(row=0, column=1)

    DataLivrare_label = Label(detail_frame, text='DataLivrare', font=('times new roman', 12))
    DataLivrare_label.grid(row=1, column=0)
    DataLivrare_entry = Entry(detail_frame)
    DataLivrare_entry.grid(row=1, column=1)

    adresaLivrare_label = Label(detail_frame, text='adresaLivrare', font=('times new roman', 12))
    adresaLivrare_label.grid(row=2, column=0)
    adresaLivrare_entry = Entry(detail_frame)
    adresaLivrare_entry.grid(row=2, column=1)

    SediuID_label = Label(detail_frame, text='SediuID', font=('times new roman', 12))
    SediuID_label.grid(row=3, column=0)
    SediuID_entry = Entry(detail_frame)
    SediuID_entry.grid(row=3, column=1)

    ComandaID_label = Label(detail_frame, text='ComandaID', font=('times new roman', 12))
    ComandaID_label.grid(row=4, column=0)
    ComandaID_entry = Entry(detail_frame)
    ComandaID_entry.grid(row=4, column=1)
        
    LivratorID_label = Label(detail_frame, text='LivratorID', font=('times new roman', 12))
    LivratorID_label.grid(row=5, column=0)
    LivratorID_entry = Entry(detail_frame)
    LivratorID_entry.grid(row=5, column=1)

    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_livrare(LivrareID_entry.get(), DataLivrare_entry.get(), adresaLivrare_entry.get(),
                                                                                                                                      SediuID_entry.get(), ComandaID_entry.get(), LivratorID_entry.get() ))
    add_button.grid(row=6, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: update_livrare(LivrareID_entry.get(), DataLivrare_entry.get(), adresaLivrare_entry.get(),
                                                                                                                                      SediuID_entry.get(), ComandaID_entry.get(), LivratorID_entry.get()))
    update_button.grid(row=6, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_livrare(LivrareID_entry.get()))
    delete_button.grid(row=6, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_livrare(event, LivrareID_entry, DataLivrare_entry, adresaLivrare_entry,
                                                                SediuID_entry, ComandaID_entry, LivratorID_entry))

    treeview_date()

    filtered_frame = Frame(frame_livrari)
    filtered_frame.place(x=500,y=300, width=500, height=200)

    Label(filtered_frame, text='Rezultat Filtru', font=('times new roman', 12, 'bold')).pack()

    filtered_treeview = ttk.Treeview(filtered_frame, columns=('LivrareID', 'DataLivrare', 'AdresaLivrare', 'SediuID', 'Pret', 'NumeLivrator'),
                                     show='headings')
    filtered_treeview.pack()
    filtered_treeview.heading('LivrareID', text='LivrareID')
    filtered_treeview.heading('DataLivrare', text='DataLivrare')
    filtered_treeview.heading('AdresaLivrare', text='AdresaLivrare')
    filtered_treeview.heading('SediuID', text='SediuID')
    filtered_treeview.heading('Pret', text='PretComanda')
    filtered_treeview.heading('NumeLivrator', text='NumeLivrator')
