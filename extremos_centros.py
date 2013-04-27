#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from sys import argv, exit

if len(argv) != 3 or (argv[2] != 'capriles' and argv[2] != 'maduro'):
    print 'uso: extremos PORCENTAJE CANDIDATO'
    print '\nej. PORCENTAJE = 90, CANDIDATO=maduro reporta los centros en donde Maduro obtuvo 90% o mas de los votos.'
    exit(1)

PORCENTAJE = int(argv[1])
CANDIDATO = argv[2]

class Resultados(object):
    def __init__(self):
        self.maduro = 0
        self.capriles = 0
        self.url13 = 'about:blank'

    def __str__(self):
        return ' Maduro: ' + str(self.maduro) +\
               ' Capriles: ' + str(self.capriles)

centros = {}
# cada clave de este diccionario es una centro, representada por el cne_new_id
# del centro electoral
# cada uno de los centros en este diccionario está asociada a un objeto de tipo
# Resultados.

with open('raw/data_2013_raw.csv', 'rb') as csvfile:
    header = None
    cnt = 0
    for fila in csv.reader(csvfile):
        if header is None:
            header = fila
        else:
            id_centro = fila[6]
            if not centros.has_key(id_centro):
                centros[id_centro] = Resultados()
                centros[id_centro].url13 = fila[22]
            centros[id_centro].maduro += int(fila[8])
            centros[id_centro].capriles += int(fila[9])

votos_maduro, votos_capriles, centros_afectadas = 0, 0, 0
for id_centro, resultados in centros.items():
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
            centros_afectadas += 1
            print id_centro, resultados, resultados.url13
print ('\nHubo %d centros donde %s tuvo al menos el %d%% de los votos.'
% (centros_afectadas, CANDIDATO.capitalize(), PORCENTAJE))
print ('\nEn estas centros hubo %d votos para Maduro y %d votos para Capriles.'
% (votos_maduro, votos_capriles))
