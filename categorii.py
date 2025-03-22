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
        cursor.execute('SELECT * FROM Categorii')
        categorii_records = cursor.fetchall()
        for record in categorii_records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare {e}')
    finally:
        cursor.close()
        conn.close()


def add_categorie(categorieID, numeCategorie, descriere):
    if (categorieID == '' or numeCategorie == ''):
        messagebox.showerror('Error', 'Campurile ID si Nume sunt obligatorii')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return 
        try:
            cursor.execute('SELECT CategorieID FROM Categorii WHERE CategorieID=?', (categorieID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id-ul deja exista')
                return
            cursor.execute('INSERT INTO Categorii VALUES (?,?,?)', (categorieID, numeCategorie, descriere))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()

def clear_fields(categorieID, numeCategorie, descriere):
    categorieID.delete(0,END)
    numeCategorie.delete(0, END)
    descriere.delete(1.0, END)

def select_categorie(event, categorieID, numeCategorie, descriere):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    clear_fields(categorieID, numeCategorie, descriere)
    categorieID.insert(0, row[0])
    numeCategorie.insert(0, row[1])
    descriere.insert(1.0, row[2])

def update_categorie(categorieID, numeCategorie, descriere):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Nu a fost selectat niciun rand')
    else:
        cursor, conn = conectare_bd()
        if not cursor or not conn:
            return
        try:
            cursor.execute('SELECT * FROM Categorii WHERE categorieID=?', (categorieID, ))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (numeCategorie, descriere)
            if current_data == new_data:
                messagebox.showinfo('Information', 'Nu a fost facuta nicio modificare')
                return
            cursor.execute('UPDATE Categorii SET numeCategorie=?, descriere=?'
                        'WHERE categorieID = ?', (numeCategorie, descriere, categorieID))
            conn.commit()
            treeview_date()
            messagebox.showinfo('Success', 'Datele au fost actualizate cu succes!')
        except Exception as e:
            messagebox.showerror('Error', f'Eroare {e}')
        finally:
            cursor.close()
            conn.close()
    
def delete_categorie(categorieID):
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
                cursor.execute('DELETE FROM Categorii WHERE CategorieID=?', (categorieID, ))
                conn.commit()
                treeview_date()
                messagebox.showinfo('Succes', 'Datele au fost sterse cu succes!')
            except Exception as e:
                messagebox.showerror('Error', f'Eroare {e}')
            finally:
                cursor.close()
                conn.close()

def categorii_produs():
    cursor, conn = conectare_bd()
    if not cursor or not conn:
        return
    try:
        interogare_treeview.delete(*interogare_treeview.get_children())
        query = """SELECT C.NumeCategorie, P.NumeProdus, P.PretUnitar
                    FROM Produse P
                    JOIN Categorii C ON P.CategorieID = C.CategorieID
                    WHERE P.PretUnitar = (
                        SELECT MAX(P2.PretUnitar)
                        FROM Produse P2
                        WHERE P2.CategorieID = P.CategorieID)"""
        cursor.execute(query)
        stoc_records = cursor.fetchall()
        for record in stoc_records:
            interogare_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Eroare la: {e}')
    finally:
        cursor.close()
        conn.close()

def form_categorii(root):

    global back_image, treeview, interogare_treeview
        
    frame_categorii = Frame(root,width=1070, height=567)
    frame_categorii.place(x=200, y=100)

    headingLabel = Label(frame_categorii, text='Detalii Categorii', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    buton_back=Button(frame_categorii, image=back_image, bd=0, cursor='hand2', command=lambda: frame_categorii.place_forget())
    buton_back.place(x=10, y=30)

    categorii_buton = Button(frame_categorii, text='ProdusScump', font=('times new roman', 12), width=10, cursor='hand2',
                        command=lambda: categorii_produs())
    categorii_buton.place(x=500, y=30)

    top_frame = Frame(frame_categorii)
    top_frame.place(x=0,y=70, relwidth=1, height=235)

    treeview = ttk.Treeview(top_frame, columns=('CategorieID','NumeCategorie', 'Descriere'), show='headings')

    treeview.pack()
    treeview.heading('CategorieID', text='CategorieID')
    treeview.heading('NumeCategorie', text='NumeCategorie')
    treeview.heading('Descriere', text='Descriere')


    detail_frame = Frame(frame_categorii)
    detail_frame.place(x = 0, y = 300)

    CategorieID_label = Label(detail_frame, text='CategorieID', font=('times new roman', 12))
    CategorieID_label.grid(row=0, column=0)
    CategorieID_entry = Entry(detail_frame)
    CategorieID_entry.grid(row=0, column=1)

    NumeCategorie_label = Label(detail_frame, text='NumeCategorie', font=('times new roman', 12))
    NumeCategorie_label.grid(row=1, column=0)
    NumeCategorie_entry = Entry(detail_frame)
    NumeCategorie_entry.grid(row=1, column=1)

    Descriere_label = Label(detail_frame, text='Descriere', font=('times new roman', 12))
    Descriere_label.grid(row=2, column=0)
    Descriere_entry = Text(detail_frame, width=20, height=4)
    Descriere_entry.grid(row=2, column=1)
    
    add_button = Button(detail_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: add_categorie(CategorieID_entry.get(), NumeCategorie_entry.get(), Descriere_entry.get()))
    add_button.grid(row=5, column=0, padx=20)

    update_button = Button(detail_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: update_categorie(CategorieID_entry.get(), NumeCategorie_entry.get(), Descriere_entry.get(1.0, END)))
    update_button.grid(row=5, column=1, padx=20)

    delete_button = Button(detail_frame, text='Sterge', font=('times new roman', 14), width=10, cursor='hand2', command=lambda: delete_categorie(CategorieID_entry.get()))
    delete_button.grid(row=5, column=2, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_categorie(event, CategorieID_entry, NumeCategorie_entry, Descriere_entry))

    treeview_date()

    frame_interogare = Frame(frame_categorii)
    frame_interogare.place(x=500, y=300, width=500, height=200)
    Label(frame_interogare, text='Categoriile impreuna cu cel mai scump produs', font=('times new roman', 12, 'bold')).pack()

    interogare_treeview = ttk.Treeview(frame_interogare, columns=('NumeCategorie', 'NumeProdus', 'PretUnitar'),
                                       show='headings')
    interogare_treeview.pack()

    interogare_treeview.heading('NumeCategorie', text='NumeCategorie')
    interogare_treeview.heading('NumeProdus', text='NumeProdus')
    interogare_treeview.heading('PretUnitar', text='PretUnitar')
