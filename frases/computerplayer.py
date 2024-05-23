from .player import Player
from .ruleta import Ruleta
import random


class ComputerPlayer(Player): # Clase que representa al jugador computadora
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.tipo = 2

    def goMove(self) -> float | str:
        """ Método que simula el movimiento del jugador computadora en la ruleta de la fortuna """
        tirada = Ruleta.girar()
        if tirada == -1:
            return "Quiebra"
        elif tirada == 0:
            return "Pierde turno"
        else:
            self.addMoney(tirada)
            print(f'Ha ganado {tirada} €')
            return tirada

    @staticmethod
    def consonanteAleatoria():
        """ Método que devuelve una consonante aleatoria """
        consonantes = random.choice("bcdfghjklmnñpqrstvwxyz")
        return random.choice(consonantes)

    @staticmethod
    def compraVocal():
        """ Método que simula la compra de una vocal """
        vocal = random.choice("aeiou")
        return vocal
