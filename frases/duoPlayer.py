from .player import Player
from .ruleta import Ruleta


class DuoPlayer(Player):  # Clase que representa al jugador humano
    def __init__(self, name: str, jugadores: list):
        super().__init__(name)
        self.name = name
        self.jugadores = jugadores
        self.tipo = 3

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

    def __str__(self):
        return f'Equipo {self.name}: {self.jugadores} con {self.prizeMoney} €'
