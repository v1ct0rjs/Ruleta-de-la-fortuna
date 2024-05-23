from .database import *
from peewee import *
import datetime


class PlayerModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    gamesPlayed = IntegerField(default=0)
    gamesWon = IntegerField(default=0)
    gamesLost = IntegerField(default=0)

    class Meta:
        database = metricadb
        table_name = 'Jugador'


class GameModel(Model):
    id = AutoField(primary_key=True)
    startDate = DateTimeField()
    endDate = DateTimeField(null=True)
    winnerPrice = IntegerField(default=0)

    class Meta:
        database = metricadb
        table_name = 'Partida'


class GamePlayerModel(Model):
    player = ForeignKeyField(PlayerModel, backref='games')
    game = ForeignKeyField(GameModel, backref='players')
    playerGamePrize = IntegerField(default=0)

    class Meta:
        database = metricadb
        table_name = 'JugadorPartida'


class RoundModel(Model):
    id = AutoField(primary_key=True)
    category = CharField(max_length=50)
    pista = CharField(max_length=50)
    frase = CharField(max_length=500)

    class Meta:
        database = metricadb
        table_name = 'Ronda'


class PhraseModel(Model):
    id = AutoField(primary_key=True)
    category = CharField(max_length=50)
    pista = CharField(max_length=50)
    frase = CharField(max_length=500)

    class Meta:
        database = metricadb
        table_name = 'Frase'


class DatabaseUtils:

    @staticmethod
    def createTables():
        metricadb.connect()
        metricadb.create_tables([PlayerModel, GameModel, GamePlayerModel, RoundModel, PhraseModel])
