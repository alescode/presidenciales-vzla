#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from sys import argv, exit

if len(argv) != 3 or (argv[2] != 'capriles' and argv[2] != 'maduro'):
    print 'uso: extremos PORCENTAJE CANDIDATO'
    print '\nej. PORCENTAJE = 90, CANDIDATO=maduro reporta las mesas en donde Maduro obtuvo 90% o mas de los votos.'
    exit(1)

PORCENTAJE = int(argv[1])
CANDIDATO = argv[2]

class Resultados(object):
    def __init__(self):
        self.chavez = -1
        self.capriles = -1
        self.url13 = 'about:blank'

    def __str__(self):
        return ' Maduro: ' + str(self.maduro) +\
               ' Capriles: ' + str(self.capriles)

mesas = {}
# cada clave de este diccionario es una mesa, representada por el cne_new_id
# del centro electoral, un guión, y el número de mesa en el centro.
# cada una de las mesas en este diccionario está asociada a un objeto de tipo
# Resultados.

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
            mesas[id_mesa].capriles = int(fila[9])
            mesas[id_mesa].url13 = fila[22]

votos_maduro, votos_capriles, mesas_afectadas = 0, 0, 0
for id_mesa, resultados in mesas.items():
    ganador = max(resultados.maduro, resultados.capriles)
    es_ganador = False
    if CANDIDATO == 'maduro' and ganador == resultados.maduro:
        es_ganador = True
    elif CANDIDATO == 'capriles' and ganador == resultados.capriles:
        es_ganador = True
    total = resultados.maduro + resultados.capriles
    if es_ganador and ganador > (PORCENTAJE/100.0) * total:
            votos_maduro += resultados.maduro
            votos_capriles += resultados.capriles
            mesas_afectadas += 1
            print id_mesa, resultados, resultados.url13
print ('\nHubo %d mesas donde %s tuvo al menos el %d%% de los votos.'
% (mesas_afectadas, CANDIDATO.capitalize(), PORCENTAJE))
print ('\nEn estas mesas hubo %d votos para Maduro y %d votos para Capriles.'
% (votos_maduro, votos_capriles))
