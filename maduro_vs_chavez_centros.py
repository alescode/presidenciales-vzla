#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
from sys import argv, exit

if len(argv) != 3:
    print 'uso: maduro_vs_chavez DIFERENCIA_CON_CHAVEZ DIFERENCIA_PARTICIPACION'
    print '\nej. DIFERENCIA_CON_CHAVEZ = 10 reporta los centros en donde Maduro obtuvo 10% o mas de votos que Chavez.'
    print 'ej. DIFERENCIA_PARTICIPACION = 300 filtra todos aquellos centros donde la diferencia de participacion en ambas elecciones haya sido mayor a 300% (tres veces la cantidad de electores).'
    exit(1)

DIF_CON_CHAVEZ = int(argv[1])
DIF_PARTICIPACION = int(argv[2])

class Resultados(object):
    def __init__(self):
        self.chavez = 0
        self.capriles12 = 0
        self.maduro = 0
        self.capriles13 = 0
        self.url12 = 'about:blank'
        self.url13 = 'about:blank'

    def __str__(self):
        return 'Chavez: ' + str(self.chavez) +\
               ' Capriles 2012: ' + str(self.capriles12) +\
               ' Maduro: ' + str(self.maduro) +\
               ' Capriles 2013: ' + str(self.capriles13)

centros = {}
# cada clave de este diccionario es una mesa, representada por el cne_new_id
# del centro electoral
# cada una de los centros en este diccionario está asociada a un objeto de tipo
# Resultados.

with open('raw/data_2012_raw.csv', 'rb') as csvfile:
    header = None
    for fila in csv.reader(csvfile):
        if header is None:
            header = fila
        else:
            id_centro = fila[9]
            if not centros.has_key(id_centro):
                centros[id_centro] = Resultados()
            centros[id_centro].chavez += int(fila[11])
            centros[id_centro].capriles12 += int(fila[12])

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
            centros[id_centro].capriles13 += int(fila[9])

votos_chavez, votos_maduro, votos_capriles12, votos_capriles13, centros_afectados = 0, 0, 0, 0, 0
for id_centro, resultados in centros.items():
    total12 = resultados.chavez + resultados.capriles12
    total13 = resultados.maduro + resultados.capriles13
    distancia = float(max(total12, total13)) / max(min(total12, total13), 1)
    if (resultados.chavez != 0 and
       resultados.maduro > (1 + (DIF_CON_CHAVEZ/100.0)) * resultados.chavez and
       distancia < (DIF_PARTICIPACION/100.0)):
        votos_chavez += resultados.chavez
        votos_maduro += resultados.maduro
        votos_capriles12 += resultados.capriles12
        votos_capriles13 += resultados.capriles13
        centros_afectados += 1
        print id_centro, resultados, resultados.url13
print ('\nHubo %d centros donde Maduro tuvo %d%% mas votos que Chavez, solo contando centros en donde los votos por ambas opciones variaron en menos del %d%%.'
% (centros_afectados, DIF_CON_CHAVEZ, DIF_PARTICIPACION))
print ('\nEn estos centros hubo %d votos para Maduro en 2013 y %d votos para Chavez en 2012, diferencia: %d'
% (votos_maduro, votos_chavez, votos_maduro - votos_chavez))
print ('\nEn estos centros hubo %d votos para Capriles en 2013 y %d votos para Capriles en 2012, diferencia: %d'
% (votos_capriles13, votos_capriles12, votos_capriles13 - votos_capriles12))
