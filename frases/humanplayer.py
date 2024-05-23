from .player import Player
from .ruleta import Ruleta
from .constantes import Constantes

class HumanPlayer(Player):  # Clase que representa al jugador humano
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.tipo = 1

    def goMove(self)-> float | str:
        """ Método que simula el movimiento del jugador humano en la ruleta de la fortuna """
        tirada = Ruleta.girar()
        if tirada == -1:
            self.applyBankrupt()
            return "Quiebra"
        elif tirada == 0:
            return "Pierde turno"
        else:
            self.addMoney(tirada)
            print(f'Ha ganado {tirada} €')
            return tirada
