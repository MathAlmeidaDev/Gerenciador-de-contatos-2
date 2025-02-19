import tkinter as tk #Biblioteca para interfaces gráficas
from tkinter import messagebox #Exibe mensagens de alerta, aviso ou informações ao usuário
import sqlite3 #biblioteca para interagir com o banco de dados SQLite


conn = sqlite3.connect('agenda.db') # cria ou abre o banco "agenda.db"
cursor = conn.cursor() # cria um cursor para interagir com o banco

cursor.execute('''
               Create TABLE)