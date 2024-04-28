#!/usr/bin/env python3
import sys
sys.path.append('..')
from BattleFieldShips.BattleShip import BattleShip

class Commander():

    def __init__(self, commanderName,commanderTurn=False):
        self.commanderName = commanderName
        self._commanderAction = None
        self.commanderTurn=commanderTurn
        self._intel = {}

    def placeShip(self,shipsCell):
        shipCharacter = BattleShip().shipChar
        shipsCell['text'] = shipCharacter

    def gatherIntel(self,intel):
        self._intel=intel
        
    def returnIntel(self):
        return self._intel

    def Attack(self,shipsCell):
        if shipsCell['text'] == '\U0001F6A2':
            return 'ship hit!'
        elif shipsCell['text'] != '\U0001F6A2':
            return 'ship missed!'
        return 'you messed up.'

    def assessDamage(self,oAction,shipsCell):
        if oAction == 'ship hit!':
            self._intel= BattleShip().shipHit(shipsCell)
            return self._intel
        elif 'ship missed!':
            self._intel= BattleShip().shipMissed(shipsCell)
            return self._intel
            
