from .constantes import Constantes
from .player import Player
from .humanplayer import HumanPlayer
from .computerplayer import ComputerPlayer
from .duoPlayer import DuoPlayer
from .roundgame import RoundGame
from .frase import Phrase
from .config import Config
from .models import PlayerModel, GameModel, GamePlayerModel, RoundModel, PhraseModel
from datetime import datetime
import os
import json
import csv


class Game:

    def __init__(self, jugadores: int, nombre: str):
        self.jugadores = jugadores
        self.nombre = nombre
        # self.tipo: list[tipo] = [1, 2, 3]
        self.rondas = Config.max_round
        self.players: list[Player] = []
        self.game_model = None

    def start(self):
        """ Método que inicia el juego """
        # 1. Inicializar el juego (construir jugadores,...)
        self.__initGame()
        self.game_model = GameModel.create(startDate=datetime.now(), winnerPrice=0)
        # 2. Lógica principal (Llamar a la ronda, ....)

        # 2. Lógica principal (Llamar a la ronda, ....)
        while self.rondas > 0:  # Mientras queden rondas
            categoriaName = Phrase.requestCategory()
            frase = Phrase.getPhrase(category=categoriaName)
            roundResult = self.__playRound(frase)
            if roundResult:  # Si playRound retorna True, se decrementan las rondas
                self.rondas -= 1
                self.__saveGame()

        # 3. Finalizan las rondas --> Mostrar Ganador
        self.showWinner()
        self.game_model.endDate = datetime.now()
        self.game_model.winnerPrice = max([player.prizeMoney for player in self.players])
        self.game_model.save()

    def __initGame(self):
        """ Método que inicializa el juego """
        os.system('clear')

        print("""
        =====================================================================================================
                                        BIENVENIDO A LA RULETA DE LA FORTUNA
                                        Creado por: Víctor Manuel Jiménez Sánchez
                                        CE_Python IES Suarez de Figueroa
        =====================================================================================================
        """)
        input('Pulsa ENTER para comenzar el juego...')

        os.system('clear')
        if not self.__loadGame():
            num = 1
            while True:
                try:
                    self.jugadores = int(input('Indica el número de jugadores (2-4): '))
                    if self.jugadores < 2 or self.jugadores > 4:
                        print('El número de jugadores debe estar entre 2 y 4')
                    else:
                        break
                except ValueError:
                    print('El número de jugadores debe ser un número entero')

            for i in range(self.jugadores):  # Iterar por cada jugador
                while True:
                    tipo = input(
                        f'¿Es un jugador HUMANO - COMPUTADORA - EQUIPO? (h/c/e): ')  # Preguntar si es humano o computadora
                    tipo = tipo.lower()
                    if tipo in ['h', 'c', 'e']:
                        self.__createPlayer(tipo, num, i)
                        num += 1
                        break
                    else:
                        print('Tipo de jugador no reconocido. Por favor, introduce h, c o e.')

    def showWinner(self):
        """ Método que muestra el ganador del juego """
        winner = None
        maxPrize = 0
        for player in self.players:
            if player.priceMoneyRound > maxPrize:
                winner = player
                maxPrize = player.priceMoneyRound
        os.system('clear')
        print(f'El ganador es {winner.name} con {winner.priceMoneyRound} €')
        print('''
        Gracias por jugar a la Ruleta de la Fortuna
        ''')
        print('Pulse ENTER para continuar...')
        input()

    def __playRound(self, frase: Phrase) -> bool:
        """ Función que juega una ronda """
        round = RoundGame(self.players, frase)
        round_model = RoundModel.create(category=frase.categoria, pista=frase.pista, frase=frase.frase)
        result = round.playRound()
        round_model.winner = round.winner.name if round.winner else None
        round_model.save()
        return result

    def __createPlayer(self, tipo: str, num: int, i: int):
        if tipo == 'h':
            nombre = input(f'Nombre del jugador {i + 1}: ')
            player = HumanPlayer(nombre)
            player_model = PlayerModel.create(name=nombre, prizeMoney=0, priceMoneyRound=0)
        elif tipo == 'e':
            jugadores = []
            nombreEquipo = input(f'Nombre del equipo: ')
            while len(jugadores) < 2:
                nombreJugador = input(f'Nombre del jugador {len(jugadores) + 1}: ')
                jugadores.append(nombreJugador)
            player = DuoPlayer(nombreEquipo, jugadores)
            player_model = PlayerModel.create(name=nombreEquipo, prizeMoney=0, priceMoneyRound=0)
        else:
            computadora = 'Computer ' + str(num)
            player = ComputerPlayer(computadora)
            player_model = PlayerModel.create(name=computadora, prizeMoney=0, priceMoneyRound=0)
        self.players.append(player)
        GamePlayerModel.create(game=self.game_model, player=player_model)

    def __loadGame(self):
        """ Método que comprueba si existe una partida guardada """
        while True:
            os.system('clear')
            valor = input('¿Desea cargar una partida existente o craar una nueva? (s/n): ')
            if valor.lower() in ['s', 'n']:
                if valor.lower() == 's':
                    if Config.format == 'json':
                        self.__loadGameJSON()
                        return True
                    else:
                        self.__loadGameCSV()
                        return True
                else:
                    return False
            else:
                print('No se reconoce el caracter. Por favor, introduce "S" o "N".')

    def __loadGameCSV(self):
        """ Método que carga una partida guardada en formato CSV """
        try:
            save_dir = os.path.expanduser('~/.ruleta_fortuna')
            save_file = os.path.join(save_dir, f'{Constantes.PARTIDA_SAVE_FILENAME}.csv')
            if os.path.exists(save_file):
                with open(save_file, 'r') as file:
                    reader = csv.reader(file)
                    self.players = []
                    for fila in reader:
                        if len(fila) == 4:  # Esto es una fila de jugador
                            nombre, prizeMoney, priceMoneyRound, tipo = fila
                            player_created = self.__createPlayerFromSaved(nombre, float(prizeMoney),
                                                                          float(priceMoneyRound), int(tipo))
                            self.players.append(player_created)

                        else:  # Esto es la última fila
                            self.rondas = int(fila[0])
                    return None
            else:
                raise FileNotFoundError
        except FileNotFoundError as e:
            print('No se ha encontrado ninguna partida guardada', e)

    def __loadGameJSON(self):
        """ Método que carga una partida guardada en formato JSON """
        try:
            save_dir = os.path.expanduser(Constantes.PATH)
            save_file = os.path.join(save_dir, f'{Constantes.PARTIDA_SAVE_FILENAME}.json')
            if os.path.exists(save_file):
                save_dir = os.path.expanduser('~/.ruleta_fortuna')
                save_file = os.path.join(save_dir, f'{Constantes.PARTIDA_SAVE_FILENAME}.json')
                with open(save_file, 'r') as file:
                    datos = json.load(file)
                    self.rondas = datos['rondas']
                    for jugador in datos['players']:
                        player_create = self.__createPlayerFromSaved(jugador['name'], jugador['prizeMoney'],
                                                                     jugador['priceMoneyRound'], jugador['tipo'])
                        self.players.append(player_create)
            else:
                raise FileNotFoundError
        except FileNotFoundError as e:
            print('No se ha encontrado ninguna partida guardada', e)

    def __saveGame(self):
        """ Método que guarda la partida actual """
        while True:
            try:
                os.system('clear')
                opcion = input("¿Desea guardar la partida actual? (s/n): ")
                match opcion.lower():
                    case 's':
                        save_dir = os.path.expanduser('~/.ruleta_fortuna')
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        save_file = os.path.join(save_dir, f'{Constantes.PARTIDA_SAVE_FILENAME}.{Config.format}')
                        with open(save_file, 'w') as file:
                            if Config.format == 'json':
                                game_state = {
                                    "rondas": self.rondas,
                                    "players": [
                                        {
                                            "name": player.name,
                                            "prizeMoney": player.prizeMoney,
                                            "priceMoneyRound": player.priceMoneyRound,
                                            "tipo": player.tipo
                                        } for player in self.players
                                    ]
                                }
                                json.dump(game_state, file, indent=4)
                                return None
                            else:
                                writer = csv.writer(file)
                                for player in self.players:
                                    player_data = [player.name, player.prizeMoney, player.priceMoneyRound, player.tipo]
                                    writer.writerow('hombre,prizeMoney,priceMoneyRound,tipo')
                                    writer.writerow(player_data)
                                writer.writerow([self.rondas])
                                return None
                    case 'n':
                        break
                    case _:
                        raise TypeError
            except TypeError as e:
                print('No se reconoce el caracter', e)

    def __createPlayerFromSaved(self, name: str, prizeMoney: float, priceMoneyRound: float, tipo: int):
        match tipo:
            case 1:
                player = HumanPlayer(name)
                player.prizeMoney = prizeMoney
                player.priceMoneyRound = priceMoneyRound
                return player
            case 2:
                player = ComputerPlayer(name)
                player.prizeMoney = prizeMoney
                player.priceMoneyRound = priceMoneyRound
                return player
            case 3:
                player = DuoPlayer(name)
                player.prizeMoney = prizeMoney
                player.priceMoneyRound = priceMoneyRound
                return player
