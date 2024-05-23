from .constantes import Constantes
import os
import yaml


class Config:
    max_round = Constantes.TOTAL_ROUNDS
    vocal_precio = Constantes.VOCAL_PRECIO
    premio_panel = Constantes.RECOMPENSA_PANEL
    premio_letra = Constantes.RECOMPENSA_LETRA
    format = Constantes.PARTIDA_SAVE_FORMAT
    configFile = 'config.yml'

    @staticmethod
    def loadConfig():
        save_dir = os.path.expanduser(Constantes.PATH)
        configuracion = os.path.join(save_dir, Config.configFile)

        if not os.path.exists(configuracion):
            Config.saveConfig(configuracion)

        with open(configuracion, 'r') as file:
            config_data = yaml.safe_load(file)
            Config.max_round = Config.getValue(config_data, 'general.max_round', default=Constantes.TOTAL_ROUNDS)
            Config.format = Config.getValue(config_data, 'general.format', default=Constantes.PARTIDA_SAVE_FORMAT)
            Config.premio_panel = Config.getValue(config_data, 'premios.premio_panel',
                                                  default=Constantes.RECOMPENSA_PANEL)
            Config.premio_letra = Config.getValue(config_data, 'premios.premio_letra',
                                                  default=Constantes.RECOMPENSA_LETRA)
            Config.vocal_precio = Config.getValue(config_data, 'premios.vocal_precio', default=Constantes.VOCAL_PRECIO)

    @staticmethod
    def getValue(values, key, default):
        keys = key.split('.')
        val = values
        for k in keys:
            if k in val:
                val = val[k]
            else:
                return default
        return val

    @staticmethod
    def saveConfig(filename):
        data = {
            "general": {
                "max_round": Constantes.TOTAL_ROUNDS,
                "format": Constantes.PARTIDA_SAVE_FORMAT
            },
            "premios": {
                "premio_panel": Constantes.RECOMPENSA_PANEL,
                "premio_letra": Constantes.RECOMPENSA_LETRA,
                "vocal_precio": Constantes.VOCAL_PRECIO
            }
        }

        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(filename, 'w') as file:
            yaml.dump(data, file)
