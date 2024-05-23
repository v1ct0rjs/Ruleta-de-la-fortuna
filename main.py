from frases import Game, Config
from frases.models import *


def initGame():
    """ Método que inicia el juego"""
    Config.loadConfig()
    DatabaseUtils.createTables()  # Crear las tablas en la base de datos
    metricadb.create_tables([PlayerModel, GamePlayerModel, GameModel, RoundModel, PhraseModel])
    juego = Game(0, '')
    juego.start()


if __name__ == '__main__':
    initGame()
