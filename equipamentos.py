import sqlite3

class Equipamentos:

    def __init__(self):
        conexao = sqlite3.connect("./equipamentos.db")
        cursor = conexao.cursor()
        self.placas = cursor.execute("SELECT * FROM placas").fetchall()
        self.inversores = cursor.execute("SELECT * FROM inversores").fetchall()
        conexao.close()
    