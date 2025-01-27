import subprocess
from Enums.WasteType import WasteType

from Utils.FPSCounter import FPSCounter
from Utils.Graphics import Graphic, SceneRender
from Utils.API_Raspberry import *

from Class.ComposedWaste import ComposedWaste
from Class.Waste import Waste

from random import randint
from copy import copy
import csv
import os
import asyncio

def getRandomPosition(WIDTH, wasteList):
    """
    Return a random available position for a waste

    Params:
    - WIDTH : int
        the width of the window
    - wasteList : [Waste]
        the list of all the current wastes

    Returns:
    - [int]
        the position of the waste
    """
    positions = []
    # Check of all the possible positions
    for i in range(0, WIDTH, 70):
        if(not isSpawnPositionOccupied([i, -75], wasteList)):
            positions.append([i, -75])
    
    # If no position is available, return a random position
    if(len(positions) == 0):
        return [randint(0, WIDTH), -75]
    
    # If only one position is available, return it
    elif len(positions) == 1:
        return positions[0]
    
    # If multiple positions are available, return a random one
    return positions[randint(0, len(positions)-1)]

def isSpawnPositionOccupied(position, wasteList):
    """
    Check if a position is already occupied by a waste

    Params:
    - position : [int]
        the position to check
    - wasteList : [Waste]
        the list of all the current wastes

    Returns:
    - bool
        True if the position is occupied, False otherwise
    """
    for elt in wasteList:
        if (elt.position[0] - position[0])**2  <= 50**2 and (elt.position[1] - position[1]) <= (75*3)**2:
            return True
    return False

def wasteSpawn(WIDTH, wasteList, wasteCatalog):
    """
    Add a waste to the current waste list

    Params:
    - WIDTH : int
        the width of the window
    - wasteList : [Waste]
        the list of all the current wastes
    - wasteCatalog : [Waste]
        the list of all the possible wastes
    """
    position = getRandomPosition(WIDTH, wasteList)

    # Choose a random waste from the catalog and copy it to prevent modification of the original waste
    a = copy(wasteCatalog[randint(0, len(wasteCatalog)-1)])

    wasteList.append(a)
    wasteList[-1].move(position)

def checkCollision(x, y, waste):
    """
    Check if a point is colliding with a waste

    Params:
    - x : int
        the x position of the point
    - y : int
        the y position of the point
    - waste : Waste
        the waste to check

    Returns:
    - bool
        True if the point is colliding with the waste, False otherwise
    """
    if waste.position[0] - waste.radius <= x <= waste.position[0] + waste.radius and waste.position[1] - waste.radius <= y <= waste.position[1] + waste.radius:
        return True
    return False

def createWastesFromSlice(WIDTH, wasteList, compWaste, wasteCatalog):
    """
    Create the wastes from a composed waste, and remove the composed waste from the list

    Params:
    - WIDTH : int
        the width of the window
    - wasteList : [Waste]
        the list of all the current wastes
    - compWaste : ComposedWaste
        the composed waste to slice
    - wasteCatalog : [Waste]
        the list of all the possible wastes
    """
    components = compWaste.slice()
    wasteList.remove(compWaste)
    for elt in components:
        for i in range(len(wasteCatalog)):
            if elt == wasteCatalog[i].name:
                waste = copy(wasteCatalog[i])
                position = getRandomPosition(WIDTH, wasteList)
                waste.move([position[0], position[1]])
                wasteList.append(waste)
                break

def updateAllWaste(render, wasteList, HEIGHT, WIDTH, wasteCatalog, wasteCurrentDelay, indexPos, player, raspberryApi, bins):
    """
    Update all the wastes in the list, and handle the collision with the hands

    Params:
    - render : SceneRender
        the render to display the wastes
    - wasteList : [Waste]
        the list of all the current wastes
    - HEIGHT : int
        the height of the window
    - WIDTH : int
        the width of the window
    - wasteCatalog : [Waste]
        the list of all the possible wastes
    - wasteCurrentDelay : float
        the delay between two waste spawns
    - indexPos : [int]
        the position of the index
    - player : Player
        the player to update the score

    Returns:
    - SceneRender
        the updated render
    """

    # Spawn a waste if there are less than 4 wastes and the delay is over
    if(len(wasteList) < 4 and wasteCurrentDelay <= 0):
        wasteSpawn(WIDTH, wasteList, wasteCatalog)
    for w in wasteList:
        # Add the waste to the render, and update it
        render.add_layer(w.get_graphic(), (w.position[0], w.position[1]))
        w.update()
        # Remove the waste if it's out of the screen
        if w.position[1] > HEIGHT - w.radius:
            remScore(player, w, raspberryApi)
            wasteList.remove(w)
            player.score -= 1
            player.lives -= 1
            bins["Floor"].addWasteToBin(w)
        if type(w) == Waste:
            if player.leftHand != None:
                # Check if the waste is compatible with the hand, and if the hand is close enough to the waste
                if player.leftHand.isCompatible(w) and (player.leftHand.pos[0] - w.position[0])**2  <= 30**2 :
                    #Boost speed
                    w.update()
                    w.update()
                    w.update()
                    w.update()

                if checkCollision(player.leftHand.pos[0], player.leftHand.pos[1], w) and w in wasteList:
                    if(player.leftHand.isCompatible(w)):
                        addScore(player, w, raspberryApi)
                    else:
                        remScore(player, w, raspberryApi)
                        player.lives -= 1
                    wasteList.remove(w)
                    player.leftHand.addWasteToBin(w)
            
            if player.rightHand != None:
                if player.rightHand.isCompatible(w) and (player.rightHand.pos[0] - w.position[0])**2  <= 30**2 :
                    #Boost speed
                    w.update()
                    w.update()
                    w.update()
                    w.update()

                if checkCollision(player.rightHand.pos[0], player.rightHand.pos[1], w) and w in wasteList:
                    if(player.rightHand.isCompatible(w)):
                        addScore(player, w, raspberryApi)
                    else:
                        remScore(player, w, raspberryApi)
                        player.lives -= 1
                    wasteList.remove(w)
                    player.rightHand.addWasteToBin(w)
        if type(w) == ComposedWaste:
            # Check if the hand is colliding with the waste
            if checkCollision(indexPos[0], indexPos[1], w):
                addScore(player, w, raspberryApi)
                createWastesFromSlice(WIDTH, wasteList, w, wasteCatalog)
    return render, player.lives

def addScore(player, waste, raspberryApi):
    player.score += waste.score
    if raspberryApi.isLoaded:
        raspberryApi.publishAddScore(player.score, waste.score)

def remScore(player, waste, raspberryApi):
    player.score -= waste.score // 2
    if raspberryApi.isLoaded:
        raspberryApi.publishRemScore(player.score, waste.score)

def createWasteCatalog():
    """
    Create the waste catalog from the CSV file

    Returns:
    - [Waste]
        the list of all the possible wastes
    """
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Ressources', 'CSV', 'wastes.csv'))
        
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        l = list(csv_reader)
        wasteCatalog = []
        for line in l[1:]:
            if(len(line) > 0):
                if line[5] == 'None':
                    wasteCatalog.append(Waste(line[0], WasteType[line[1]], line[4], line[2], float(line[3])))
                else:
                    if line[7] != 'None':     
                        wasteCatalog.append(ComposedWaste(line[0], [line[5], line[6], line[7]], line[4], line[2], float(line[3])))
                    elif line[7] == 'None' and line[6] != 'None':
                        wasteCatalog.append(ComposedWaste(line[0], [line[5], line[6]], line[4], line[2], float(line[3])))
    return wasteCatalog