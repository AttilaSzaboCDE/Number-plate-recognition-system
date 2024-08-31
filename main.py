import cv2
import pytesseract
import db_manager
import gui

#Adatbázis elkészítése
#   csatlakozás és feltöltés nem kell, hogy mindig lefusson, mert csak beszúr ugyanolyan sorokat
connection = db_manager.connect('database.db')
#   törlése:
#db_manager.drop_table('database.db','tickets')
#db_manager.create_tables(connection)

#GUI felület
gui.StartWindow()
