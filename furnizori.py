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
        cursor.execute('SELECT * FROM Furnizori')
        furnizori_records = cursor.fetchall()
        for record in furnizori_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()


def add_furnizor(furnizorID, numeFurnizor, adresa, email, telefonFurnizor):
    if (furnizorID == '' or numeFurnizor == '' or adresa == '' or email == '' or telefonFurnizor == ''):
        messagebox.showerror('Error', 'Toate campurile sunt obligatorii!')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT FurnizorID FROM Furnizori WHERE FurnizorID=?', (furnizorID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Furnizori VALUES (?,?,?,?,?)', (furnizorID, numeFurnizor, adresa, email, telefonFurnizor))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(furnizorID, numeFurnizor, adresa, email, telefonFurnizor):
    furnizorID.delete(0,END)
    numeFurnizor.delete(0, END)
    adresa.delete(0, END)
    email.delete(0,END)
    telefonFurnizor.delete(0,END)

def select_furnizor(event, furnizorID, numeFurnizor, adresa, email, telefonFurnizor):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(furnizorID, numeFurnizor, adresa, email, telefonFurnizor)
    furnizorID.insert(0, row[0])
    numeFurnizor.insert(0, row[1])
    adresa.insert(0, row[2])
    email.insert(0, row[3])
    telefonFurnizor.insert(0, f'{row[4]}')

def update_furnizor(furnizorID, numeFurnizor, adresa, email, telefonFurnizor):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Furnizori WHERE FurnizorID=?', (furnizorID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (numeFurnizor, adresa, email, telefonFurnizor)
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Furnizori SET numeFurnizor=?, adresa=?, email=?, telefonFurnizor=?'
                        'WHERE furnizorID = ?', (numeFurnizor, adresa, email, telefonFurnizor, furnizorID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()


def delete_furnizor(furnizorID):
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
                cursor.execute('DELETE FROM Furnizori WHERE FurnizorID=?', (furnizorID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def select_furnizor(button):
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return

    try:
        cursor.execute("SELECT DISTINCT C.FurnizorID, F.NumeFurnizor FROM Comenzi C JOIN Furnizori F ON C.FurnizorID = F.FurnizorID")
        furnizori = cursor.fetchall()
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la incarcarea furnizorilor: {e}')
        return
    finally:
        cursor.close()
        conn.close()

    top = Toplevel()
    top.title("Alege Furnizor")
    top.geometry("300x400")
    
    frame = Frame(top)
    frame.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    listbox = Listbox(frame, font=('times new roman', 12), yscrollcommand=scrollbar.set)

    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)

    for furnizor in furnizori:
        listbox.insert(END, f"{furnizor[0]} - {furnizor[1]}")

    def on_select(event):
        selected = listbox.get(ACTIVE)
        button.config(text=selected)
        top.destroy()

    listbox.bind("<Double-Button-1>", on_select)

    top.mainloop()

def filtru_furnizori(selected_value):
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        filtered_treeview.delete(*filtered_treeview.get_children())

        if selected_value:
            furnizorID = selected_value.split(' - ')[0]  

            query = """SELECT P.NumeProdus, P.PretUnitar, C.NumeCategorie
                        FROM Produse P
                        JOIN Categorii C ON P.CategorieID = C.CategorieID
                        WHERE ProdusID IN (
                            SELECT PC.ProdusID
                            FROM ProduseComenzi PC
                            JOIN Comenzi C ON PC.ComandaID = C.ComandaID
                            WHERE C.FurnizorID = ?)"""
            cursor.execute(query, (furnizorID,))
            filtered_records = cursor.fetchall()
            for record in filtered_records:
                filtered_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la filtrare: {e}')
    finally:
        cursor.close()
        conn.close()

def form_furnizori(root):

    global back_image, treeview, filtered_treeview
        
    frame_furnizori = Frame(root,width=1070, height=567)
    frame_furnizori.place(x=200, y=100)

    headingLabel = Label(frame_furnizori, text='Detalii Furnizori', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_furnizori, image=back_image, bd=0, cursor='hand2', command=lambda: frame_furnizori.place_forget())
    buton_back.place(x=10, y=30)

    filtru_frame = Frame(frame_furnizori)
    filtru_frame.place(x=80,y=40)

    filtru_label = Label(filtru_frame, text='Selecteaza Furnizor:', font=('times new roman', 12))
    filtru_label.grid(row=0,column=0)

    furnizor_buton = Button(filtru_frame, text='Alege Furnizor', font=('times new roman', 12),
                            command=lambda: select_furnizor(furnizor_buton))
    furnizor_buton.grid(row=0, column=1, padx=10)


    filtru_buton = Button(filtru_frame, text='Filtreaza', font=('times new roman', 12), cursor='hand2',
                          command=lambda: filtru_furnizori(furnizor_buton.cget("text").split(' - ')[0] if ' - ' in furnizor_buton.cget("text") else None))
    filtru_buton.grid(row=0, column=2, padx=10)

    top_frame = Frame(frame_furnizori)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('FurnizorID','NumeFurnizor', 'Adresa', 'Email', 'TelefonFurnizor'), show='headings')

    treeview.pack()
    treeview.heading('FurnizorID', text='FurnizorID')
    treeview.heading('NumeFurnizor', text='NumeFurnizor')
    treeview.heading('Adresa', text='Adresa')
    treeview.heading('Email', text='Email')
    treeview.heading('TelefonFurnizor', text='TelefonFurnizor')


    detail_frame = Frame(frame_furnizori)
    detail_frame.place(x = 0, y = 300)

    FurnizorID_label = Label(detail_frame, text='FurnizorID', font=('times new roman', 12))
    FurnizorID_label.grid(row=0, column=0)
    FurnizorID_entry = Entry(detail_frame)
    FurnizorID_entry.grid(row=0, column=1)

    NumeFurnizor_label = Label(detail_frame, text='NumeFurnizor', font=('times new roman', 12))
    NumeFurnizor_label.grid(row=1, column=0)
    NumeFurnizor_entry = Entry(detail_frame)
    NumeFurnizor_entry.grid(row=1, column=1)

    Adresa_label = Label(detail_frame, text='Adresa', font=('times new roman', 12))
    Adresa_label.grid(row=2, column=0)
    Adresa_entry = Entry(detail_frame)
    Adresa_entry.grid(row=2, column=1)

    Email_label = Label(detail_frame, text='Email', font=('times new roman', 12))
    Email_label.grid(row=3, column=0)
    Email_entry = Entry(detail_frame)
    Email_entry.grid(row=3, column=1)

    TelefonFurnizor_label = Label(detail_frame, text='TelefonFurnizor', font=('times new roman', 12))
    TelefonFurnizor_label.grid(row=4, column=0)
    TelefonFurnizor_entry = Entry(detail_frame)
    TelefonFurnizor_entry.grid(row=4, column=1)
    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_furnizor(FurnizorID_entry.get(), NumeFurnizor_entry.get(), Adresa_entry.get(),
                                                                                                                                       Email_entry.get(), TelefonFurnizor_entry.get()))
    add_button.grid(row=5, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command= lambda: update_furnizor(FurnizorID_entry.get(), NumeFurnizor_entry.get(), Adresa_entry.get(),
                                                                                                                                       Email_entry.get(), TelefonFurnizor_entry.get()))
    update_button.grid(row=5, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_furnizor(FurnizorID_entry.get()))
    delete_button.grid(row=5, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_furnizor(event, FurnizorID_entry, NumeFurnizor_entry, Adresa_entry,
                                                                Email_entry, TelefonFurnizor_entry))

    treeview_date()

    filtered_frame = Frame(frame_furnizori)
    filtered_frame.place(x=500,y=300, width=500, height=200)

    Label(filtered_frame, text='Produse comandate de la fiecare furnizor', font=('times new roman', 12, 'bold')).pack()

    filtered_treeview = ttk.Treeview(filtered_frame, columns=('NumeProdus', 'PretUnitar', 'NumeCategorie'),
                                     show='headings')
    filtered_treeview.pack()
    filtered_treeview.heading('NumeProdus', text='NumeProdus')
    filtered_treeview.heading('PretUnitar', text='PretUnitar')
    filtered_treeview.heading('NumeCategorie', text='NumeCategorie')
 