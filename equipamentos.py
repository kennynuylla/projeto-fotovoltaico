import sqlite3

class Equipamentos:

    def __init__(self, tensao):
        conexao = sqlite3.connect("./equipamentos.db")
        cursor = conexao.cursor()
        self.kits = cursor.execute("SELECT * FROM kits where tensao=%f" %(tensao)).fetchall()
        conexao.close()
    