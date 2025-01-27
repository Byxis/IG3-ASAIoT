import csv
import os
from datetime import datetime

class LeaderBoard:
    def __init__(self):
        """
        Create a LeaderBoard instance, load the data from the csv file
        """
        self.scores_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Ressources', 'CSV', 'scores.csv'))

    def loadTenFirst(self):
        """
        Load and return the ten first scores from the csv file

        Returns:
        - [str]
            the ten first scores
        """
        with open(self.scores_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            lines = list(csv_reader)
            print(lines)
            print(lines[1:])
            print(lines[1:][2])
            sorted_lines = sorted(lines[1:], key= lambda x: int(x[2]), reverse=True)
            firstTen = sorted_lines[:min(10,len(sorted_lines)-1)]
            for elt in firstTen:
                elt[0] = elt[0][0:10]
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
        with open(self.scores_path, mode='a', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([datetime.now(), player_name, score])
