import process
import db_manager
import datetime
import tkinter as tk
#import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
#from TkinterDnD2 import *


def StartWindow():

    start = tk.Tk() #Megcsinálom az ablakot
    start.resizable(False, False)


    #gui.geometry("1280x720")
    #gui.config(background="#bbbbbb")
    start.title("Matrica ellenőrző rendszer")
    label = tk.Label(start, text="Adjon hozzá egy videót!", font=('Arial',16))
    label.pack(padx=20,pady=20)

    # Tallózás Button
    tallozas = tk.Button(start, text="Tallózás", font=('Arial',16), command=open_file_dialog, fg="green", bg="green", borderwidth=2)
    #tallozas.pack(padx=20,pady=20)

    settings = tk.Button(start, text="Beállítások", font=('Arial',16), command=OpenSettingsWindow, fg="green", bg="green", borderwidth=2)
    #settings.grid(row=1, column=0, padx=0, pady=0)
    settings.pack(side=tk.LEFT, padx=(35,2), pady=20)
    tallozas.pack(side=tk.RIGHT, padx=(2,35), pady=20)


    start.mainloop()

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        process.OpenCV(file_path)


def OpenSettingsWindow():
    settings = tk.Tk()
    settings.title("Beállítások - Matrica ellenőrző rendszer")
    settings.geometry("630x390")
    settings.resizable(False, False)

    title = tk.Label(settings, text="Adatbázis és kezelése", font=('Arial',16))
    title.grid(row=0, column=0, padx=10, pady=10)


    label1 = tk.Label(settings, text="Adatbázis adatainak módosítása:", font=('Arial',12))
    label1.grid(row=1, column=0, padx=10, pady=(10,2))
    bp_label = tk.Label(settings, text="Adja meg a rendszámot!", font=('Arial',12))
    bp_label.grid(row=2, column=1, padx=10, pady=(5,2))
    bd_label = tk.Label(settings, text="Adja meg a lejárati dátumot!", font=('Arial',12))
    bd_label.grid(row=2, column=2, padx=10, pady=(5,2))
    beszuras = tk.Button(settings, text="Rendszám hozzáadása", command=lambda: AddPlate(bp_input.get(), bd_input.get(), b_error_label), font=('Arial',12))
    beszuras.grid(row=3, column=0, padx=(10,2),pady=2)
    bp_input = tk.Entry(settings)
    bp_input.grid(row=3, column=1, padx=(10,2),pady=2)
    bd_input = tk.Entry(settings)
    bd_input.grid(row=3, column=2, padx=(10,2),pady=2)
    b_error_label = tk.Label(settings, font=('Arial',12),fg="red")
    b_error_label.grid(row=4, column=0, padx=10, pady=(5,2), columnspan=2)

    t_label = tk.Label(settings, text="Adja meg a rendszámot!", font=('Arial',12))
    t_label.grid(row=5, column=1, padx=10, pady=(5,2))
    torles = tk.Button(settings, text="Rendszám törlése", command=lambda: RemovePlate(tp_input.get(), t_error_label), font=('Arial',12))
    torles.grid(row=6, column=0, padx=(10,2),pady=2)
    tp_input = tk.Entry(settings)
    tp_input.grid(row=6, column=1, padx=(10,2),pady=2)
    t_error_label = tk.Label(settings, font=('Arial',12),fg="red")
    t_error_label.grid(row=7, column=0, padx=10, pady=(5,2), columnspan=2)

    
    label2 = tk.Label(settings, text="Adatbázis kiíratása a képernyőre:", font=('Arial',12), justify="left")
    label2.grid(row=9, column=0, padx=10, pady=(20,2))
    listazas = tk.Button(settings, text="Listázás", font=('Arial',12), command=DisplayDatabase, justify="left")
    listazas.grid(row=10, column=0, padx=10,pady=10)


def AddPlate(plate, end_of_validity, error):
    print(end_of_validity)
    if plate is None or plate.strip() == "":
        error.config(text="Adja meg az értékeket!")
    elif end_of_validity is None or end_of_validity.strip() == "":
        error.config(text="Adja meg az értékeket!")
    elif len(plate) < 4:
        error.config(text="A rendszám legalább 4 karakterből kell álljon!")
    elif not end_of_validity or len(end_of_validity) != 10 or end_of_validity[4] != "-" or end_of_validity[7] != "-":
        error.config(text="Helytelen dátum formátum! Használja az ÉÉÉÉ-HH-NN formátumot!")
    else:
        try:
            datetime.datetime.strptime(end_of_validity, "%Y-%m-%d")
            plate = plate.upper()
            print("Rendszám:", plate)
            print("Lejárati dátum:", end_of_validity)
            db_manager.add_row(plate, end_of_validity)
        except ValueError:
            error.config(text="Helytelen dátum formátum! Használja az ÉÉÉÉ-HH-NN formátumot!")



def RemovePlate(plate, error):
    if plate is None or plate.strip() == "":
        error.config(text="Adja meg az értékeket!")
    elif len(plate) < 4:
        error.config(text="A rendszám legalább 4 karakterből kell álljon!")
    else:
        plate = plate.upper()
        print("Törlendő rendszám:", plate)
        db_manager.delete_row(plate)

def DisplayDatabase():
    conn = db_manager.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tickets")
    rows = c.fetchall()
    conn.close()

    if rows:
        # Létrehozunk egy új ablakot a listázáshoz
        listazas_window = tk.Toplevel()
        listazas_window.title("Adatok listázása")

        # Létrehozunk egy Treeview widget-et a táblázathoz
        tree = ttk.Treeview(listazas_window)
        tree["columns"] = ("Plate", "Date", "End of Validity")
        tree.heading("#0", text="ID")
        tree.heading("Plate", text="Rendszám")
        tree.heading("Date", text="Kezdő dátum")
        tree.heading("End of Validity", text="Lejárati dátum")
        tree.pack(expand=True, fill="both")

        # Betöltjük az adatokat a Treeview-be
        for row in rows:
            tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))
        
    else:
        print("Nincsenek adatok az adatbázisban.")