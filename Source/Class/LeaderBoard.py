import csv
from datetime import datetime

class LeaderBoard:
    def __init__(self):
        """
        Create a LeaderBoard instance, load the data from the csv file
        """
        with open('../Ressources/CSV/scores.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            self.data = list(csv_reader)

    def loadTenFirst(self):
        """
        Load and return the ten first scores from the csv file

        Returns:
        - [str]
            the ten first scores
        """
        with open('CSV/scores.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            lines = list(csv_reader)
            sorted_lines = sorted(lines[1:], key= lambda x: int(x[2]), reverse=True)
            firstTen = sorted_lines[:10]
        return firstTen
        
    def addAndSave(self,  player_name, score):
        """
        Allow to add a new (date, player_name, score) to the csv file

        Params:
        - player_name : str
            the name of the player
        - score : int
            the score of the player
        """
        with open('CSV/scores.csv', mode='a', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([datetime.now(), player_name, score])
        with open('CSVscores.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            self.data = list(csv_reader)