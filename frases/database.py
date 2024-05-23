import os
from peewee import *
from .constantes import Constantes

folderdb = os.path.expanduser(Constantes.PATH) # Path: ~/.ruleta_fortuna
metricadb = SqliteDatabase(os.path.join(folderdb, Constantes.DBNAME)) # Path: ~/.ruleta_fortuna/metrica.db