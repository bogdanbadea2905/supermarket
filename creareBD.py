import sqlite3

conn = sqlite3.connect('Supermarket.db')

c = conn.cursor()
"""
c.execute('''CREATE TABLE Furnizori 
          (
          FurnizorId INT IDENTITY(1,1) NOT NULL,
          NumeFurnizor NVARCHAR(50) NOT NULL,
          Adresa NVARCHAR(100) NOT NULL,
          Email NVARCHAR(100),
          TelefonFurnizor CHAR(10),

          CONSTRAINT PK_Furnizori PRIMARY KEY (FurnizorId) 
          )''')


c.execute('''CREATE TABLE Categorii
          (
          CategorieId INT IDENTITY(1,1) NOT NULL,
          NumeCategorie NVARCHAR(50) NOT NULL,
          Descriere NVARCHAR(100), 

          CONSTRAINT PK_Categorii PRIMARY KEY(CategorieId)
          )''')


c.execute('''CREATE TABLE Produse
          (
          ProdusId INT IDENTITY(1,1) NOT NULL,
          NumeProdus NVARCHAR(50) NOT NULL,
          PretUnitar DECIMAL NOT NULL,
          DataValabilitate SMALLDATETIME,
          CategorieId INT NOT NULL,
          
          CONSTRAINT PK_Produse PRIMARY KEY (ProdusId),
          CONSTRAINT FK_Produse_Categorii FOREIGN KEY(CategorieId) REFERENCES Categorii(CategorieId) 
          )''')


c.execute('''CREATE TABLE Manageri
          (
          ManagerId INT IDENTITY(1,1) NOT NULL,
          Nume NVARCHAR(50) NOT NULL,
          Prenume NVARCHAR(50) NOT NULL,
          Email NVARCHAR(100) NOT NULL,
          Parola NVARCHAR(50) NOT NULL,

          CONSTRAINT PK_Manager PRIMARY KEY(ManagerId)
          )''')


c.execute('''CREATE TABLE Livratori
          (
          LivratorId INT IDENTITY(1,1) NOT NULL,
          NumeLivrator NVARCHAR(50) NOT NULL,
          PrenumeLivrator NVARCHAR(50) NOT NULL,
          Telefon CHAR(10) NOT NULL,
          Email NVARCHAR(100) NOT NULL,

          CONSTRAINT PK_Livratori PRIMARY KEY (LivratorId)
          )''')


c.execute('''CREATE TABLE Comenzi
          (
          ComandaId INT IDENTITY(1,1) NOT NULL,
          DataComanda SMALLDATETIME NOT NULL,
          Pret DECIMAL NOT NULL,
          AdresaFacturare NVARCHAR(100) NOT NULL,
          FurnizorId INT NOT NULL,
          ManagerId INT NOT NULL,

          CONSTRAINT PK_Comenzi PRIMARY KEY (ComandaId),
          CONSTRAINT FK_ComenziFurnizori FOREIGN KEY(FurnizorId) REFERENCES Furnizori(FurnizorId),
          CONSTRAINT FK_ComenziManager FOREIGN KEY (ManagerId) REFERENCES Manageri(ManagerId) 
          )''')


c.execute('''CREATE TABLE Sedii
        (
        SediuId INT IDENTITY(1,1) NOT NULL,
        NumeSediu NVARCHAR(50) NOT NULL,
        Locatie NVARCHAR(100) NOT NULL,
        Capacitate INT NOT NULL,
        
        CONSTRAINT PK_Sedii PRIMARY KEY (SediuId)  
        )''')


c.execute('''CREATE TABLE Livrari
        (
        LivrareId INT IDENTITY(1,1) NOT NULL,
        DataLivrare SMALLDATETIME NOT NULL,
        AdresaLivrare NVARCHAR(100) NOT NULL,
        SediuId INT NOT NULL,
        ComandaId INT NOT NULL,
        LivratorId INT NOT NULL,
        
        CONSTRAINT PK_Livrari PRIMARY KEY(LivrareId),
        CONSTRAINT FK_LivrariSedii FOREIGN KEY(SediuId) REFERENCES Sedii(SediuId),
        CONSTRAINT FK_LivrariComenzi FOREIGN KEY(ComandaId) REFERENCES Comenzi(ComandaId),
        CONSTRAINT FK_LivrareLivrator FOREIGN KEY (LivrareId) REFERENCES Livrari(LivrareId)
        )''')


c.execute('''CREATE TABLE FurnizoriCategorii
        (
          FurnizorId INT NOT NULL,
          CategorieId INT NOT NULL,
          NumarProduse INT NOT NULL,

          CONSTRAINT PK_FurnizoriCategorii PRIMARY KEY(FurnizorId, CategorieId),
          CONSTRAINT FK_Furnizor FOREIGN KEY (FurnizorId) REFERENCES Furnizori(FurnizorId),
          CONSTRAINT FK_Categorii FOREIGN KEY (CategorieId) REFERENCES Categorii(CategorieId)
        )''')


c.execute('''CREATE TABLE ProduseComenzi
          (
          ProdusId INT NOT NULL,
          ComandaId INT NOT NULL,
          Cantitate INT NOT NULL,

          CONSTRAINT PK_ProduseComenzi PRIMARY KEY(ProdusId,ComandaId),
          CONSTRAINT FK_Produs FOREIGN KEY (ProdusId) REFERENCES Produse(ProdusId),
          CONSTRAINT FK_Comenzi FOREIGN KEY(ComandaId) REFERENCES Comenzi(ComandaId)
          )''')


c.execute('''CREATE TABLE ProduseSedii 
          (
          ProdusId INT NOT NULL,
          SediuId INT NOT NULL,
          NumarStoc INT NULL,

          CONSTRAINT PK_ProduseSedii PRIMARY KEY (ProdusId, SediuId),
          CONSTRAINT FK_Produse FOREIGN KEY (ProdusId) REFERENCES Produse(ProdusId),
          CONSTRAINT FK_Sedii FOREIGN KEY(SediuId) REFERENCES Sedii(SediuId)
          )''')
"""


furnizori_data = [

    (6, 'Furnizor 6', 'Strada 6, Craiova', 'furnizor6@example.com', '0762345711')
]

categorii_data = [
    (1,'Fructe', 'Categorii de fructe proaspete'),
    (2,'Legume', 'Categorii de legume proaspete'),
    (3,'Produse lactate', 'Categorii de produse lactate'),
    (4,'Electrocasnice', 'Produse pentru casa'),
    (5,'Mezeluri', 'Carne procesata'),
    (6,'Produse igiena', 'Igiena corpului')
]

produse_data = [
    (1,'Mere', 3.5, '2024-12-31', 1),
    (2,'Castraveti', 2.8, '2024-11-30', 2),
    (3,'Branza', 15.0, '2024-12-15', 3),
    (4,'Air-fryer', 100.0, '', 4),
    (5,'Sunca praga', 4.0, '2024-11-29', 5),
    (6,'Sampon', 20.0, '2026-11-17', 6)
]

manageri_data = [
    (1, 'Popescu', 'Ion', 'ion.popescu@example.com', 'parola123'),
    (2, 'Ionescu', 'Maria', 'maria.ionescu@example.com', 'parola456'),
    (3, 'Dumitrescu', 'Rares', 'rares.dumitrescu@example.com', 'parola789'),
    (4, 'Petrescu', 'Adina', 'adina.petrescu@example.com', 'parola135'),
    (5, 'Dragota', 'Florin', 'florin.dragota@example.com', 'parol246'),
    (6, 'Marinovici', 'Mihaela', 'mihaela.marinovici@example.com', 'parola579')
]

sedii_data = [
    (6, 'Sediu 6', 'Strada Panduri, Craiova', 175)

]

livratori_data = [
    (1,'Gheorghe', 'Vasile', '0745678901', 'vasile.gheorghe@example.com'),
    (2,'Dumitru', 'Mihai', '0756789012', 'mihai.dumitru@example.com'),
    (3,'Badea', 'Razvan', '0746728321', 'razvan.badea@example.com'),
    (4,'Arhip', 'Ana', '0723456221', 'ana.arhip@example.com'),
    (5,'Avram', 'Andrei', '0765890113', 'andrei.avram@example.com'),
    (6,'Ungureanu','Roxana','0721335098', 'ana.ungureanu@example.com')
]

comenzi_data = [

    (6,'2024-10-17', 170.0, 'Strada Panduri, Craiova', 6, 5)
]

livrari_data = [

    (6,'2024-10-20', 'Strada Pandrui, Craiova', 6, 6, 6)
]

furnizori_categorii_data = [
   
    (3, 4, 15),
    (4, 5, 25),
    (5, 6, 60)
]

produse_comenzi_data = [
   
    (5,6,10)
]

produse_sedii_data = [
    
    (4, 3, 15),
    (5, 4, 10),
    (6, 5, 30)
]


#c.executemany('INSERT INTO Furnizori (FurnizorId, NumeFurnizor, Adresa, Email, TelefonFurnizor) VALUES (?, ?, ?, ?, ?)', furnizori_data)
#c.executemany('INSERT INTO Categorii (CategorieId,NumeCategorie, Descriere) VALUES (?, ?, ?)', categorii_data)
#c.executemany('INSERT INTO Produse (ProdusId, NumeProdus, PretUnitar, DataValabilitate, CategorieId) VALUES (?,?, ?, ?, ?)', produse_data)
#c.executemany('INSERT INTO Manageri (ManagerId, Nume, Prenume, Email, Parola) VALUES (?, ?, ?, ?, ?)', manageri_data)
#c.executemany('INSERT INTO Sedii (SediuId, NumeSediu, Locatie, Capacitate) VALUES (?, ?, ?, ?)', sedii_data)
#c.executemany('INSERT INTO Livratori (LivratorId, NumeLivrator, PrenumeLivrator, Telefon, Email) VALUES (?, ?, ?, ?, ?)', livratori_data)
#c.executemany('INSERT INTO Comenzi (ComandaId, DataComanda, Pret, AdresaFacturare, FurnizorId, ManagerId) VALUES (?, ?, ?, ?, ?, ?)', comenzi_data)
#c.executemany('INSERT INTO Livrari (LivrareId, DataLivrare, AdresaLivrare, SediuId, ComandaId, LivratorId) VALUES (?, ?, ?, ?, ?, ?)', livrari_data)
#c.executemany('INSERT INTO FurnizoriCategorii (FurnizorId, CategorieId, NumarProduse) VALUES (?, ?, ?)', furnizori_categorii_data)
c.executemany('INSERT INTO ProduseComenzi (ProdusId, ComandaId, Cantitate) VALUES (?, ?, ?)', produse_comenzi_data)
#c.executemany('INSERT INTO ProduseSedii (ProdusId, SediuId, NumarStoc) VALUES (?, ?, ?)', produse_sedii_data)


conn.commit()



conn.close()