import csv
from datetime import datetime

class LeaderBoard:
    def __init__(self):
        with open('CSV/scores.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            self.data = list(csv_reader)
    def loadTenFirst(self):
        #fonction qui renvoie les 10 meilleurs score sous forme de tableau de tableau ou chaque sous tableau contient la date de la partie,
        #le nom et le score du joueur
        with open('CSV/scores.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            lines = list(csv_reader)
            sorted_lines = sorted(lines[1:], key= lambda x: int(x[2]), reverse=True)
            firstTen = sorted_lines[:10]
        return firstTen
        
    def addAndSave(self,  player_name, score):
        #fonction qui ajoute et une ligne dans le csv a partir d'un nom et d'un score. 
        with open('CSV/scores.csv', mode='a', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([datetime.now(), player_name, score])
        with open('CSVscores.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            self.data = list(csv_reader)

