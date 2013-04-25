#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict

class Resultados(object):
    def __init__(self):
        self.chavez = -1
        self.capriles12 = -1
        self.maduro = -1
        self.capriles13 = -1
        self.url12 = 'about:blank'
        self.url13 = 'about:blank'

    def __str__(self):
        return 'Chavez: ' + str(self.chavez) +\
               ' Capriles 2012: ' + str(self.capriles12) +\
               ' Maduro: ' + str(self.maduro) +\
               ' Capriles 2013: ' + str(self.capriles13)

mesas = {}
# cada clave de este diccionario es una mesa, representada por el cne_new_id
# del centro electoral, un guión, y el número de mesa en el centro.
# cada una de las mesas en este diccionario está asociada a un objeto de tipo
# Resultados.

with open('raw/data_2012_raw.csv', 'rb') as csvfile:
    header = None
    for fila in csv.reader(csvfile):
        if header is None:
            header = fila
        else:
            id_mesa = fila[9] + '-' + fila[10]
            if not mesas.has_key(id_mesa):
                mesas[id_mesa] = Resultados()
            mesas[id_mesa].chavez = int(fila[11])
            mesas[id_mesa].capriles12 = int(fila[12])

with open('raw/data_2013_raw.csv', 'rb') as csvfile:
    header = None
    cnt = 0
    for fila in csv.reader(csvfile):
        if header is None:
            header = fila
        else:
            id_mesa = fila[6] + '-' + fila[7]
            if not mesas.has_key(id_mesa):
                mesas[id_mesa] = Resultados()
            mesas[id_mesa].maduro = int(fila[8])
            mesas[id_mesa].capriles13 = int(fila[9])
            mesas[id_mesa].url13 = fila[22]
            mesas[id_mesa].url12 = fila[22].replace('2013', '2012')

for id_mesa, resultados in mesas.items():
    if resultados.maduro > resultados.chavez and resultados.chavez != -1:
        print id_mesa, resultados, resultados.url13
