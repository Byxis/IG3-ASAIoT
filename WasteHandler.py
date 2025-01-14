import csv
import Waste
import ComposedWaste
def createWasteCatalog():
    with open('Wastes.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        l = list(csv_reader)
        wasteCatalog = []
        for line in l:
            if line[5] == 'None':
                wasteCatalog.append(Waste(line[0], line[1], line[4], line[2], line[4]))