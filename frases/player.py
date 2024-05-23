import abc

from .config import Config


class Player(abc.ABC):  # Clase abstracta
    def __init__(self, name: str):
        self.priceMoneyRound = 0
        self.prizeMoney = 0
        self.name = name

    def addMoney(self, amt: float):  # Añadir dinero
        self.prizeMoney += amt

    def applyBankrupt(self):  # Aplicar quiebra
        self.prizeMoney = 0

    def addPrizeRound(self, prize: float):  # Añadir premio de ronda
        self.priceMoneyRound += prize

    def applyWinRound(self):  # Aplicar premio por victoria
        self.priceMoneyRound += Config.premio_panel

    @abc.abstractmethod
    def goMove(self):  # Método abstracto para simular el movimiento del jugador
        pass

    def __str__(self):  # Método para imprimir el objeto
        return f'{self.name}: {self.prizeMoney}'
