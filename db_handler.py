import os
import sqlite3 as sql

class DatabaseHandler():
    def __init__(self, database_name: str) -> None:
        self.con = sql.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sql.Row
    
    def add(self, id: str, pseudo: str) -> None:
        cursor = self.con.cursor()
        query = f"INSERT INTO Joueurs (id, pseudo) VALUES (?, ?);"
        cursor.execute(query, (id, pseudo,))
        cursor.close()
        self.con.commit()
    
    def is_in(self, id: str) -> bool:
        cursor = self.con.cursor()
        query = f"SELECT id FROM Joueurs WHERE id = ?;"
        cursor.execute(query, (id,))
        rep = cursor.fetchall()
        cursor.close()

        return len(rep) == 1
    
    def get_power(self, id):
        cursor = self.con.cursor()
        query = f"SELECT power FROM Joueurs WHERE id = ?"
        cursor.execute(query, (id,))

        power = cursor.fetchall()
        cursor.close()
        return dict(power[0])["power"]
    
    def get_power_max(self, id):
        cursor = self.con.cursor()
        query = f"SELECT power_max FROM Joueurs WHERE id = ?"
        cursor.execute(query, (id,))

        power_max = cursor.fetchall()
        cursor.close()
        return dict(power_max[0])["power_max"]

    def set_power(self, id, p):
        cursor = self.con.cursor()
        query = f"UPDATE Joueurs SET power = ? WHERE id = ?"
        cursor.execute(query, (p, id,))
        self.update_max(id)

        cursor.close()
        self.con.commit()

    def update_max(self, id):
        power = self.get_power(id)
        power_max = self.get_power_max(id)

        cursor = self.con.cursor()
        if power > power_max:
            query = f"UPDATE Joueurs SET power_max = ? WHERE id = ?"
            cursor.execute(query, (power, id,))
        
        cursor.close()
        self.con.commit()
    
    def add_game(self, id):
        cursor = self.con.cursor()
        query = f"UPDATE Joueurs SET played_games = played_games + 1 WHERE id = ?"
        cursor.execute(query, (id,))
        cursor.close()
        self.con.commit()
    
    def add_win(self, id):        
        cursor = self.con.cursor()
        query = f"UPDATE Joueurs SET wins = wins + 1 WHERE id = ?"
        cursor.execute(query, (id,))
        cursor.close()
        self.con.commit()

        self.add_game(id)