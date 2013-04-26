#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
from sys import argv, exit

if len(argv) != 3:
    print 'uso: maduro_vs_chavez DIFERENCIA_CON_CHAVEZ DIFERENCIA_PARTICIPACION'
    print '\nej. DIFERENCIA_CON_CHAVEZ = 10 reporta las mesas en donde Maduro obtuvo 10% o mas de votos que Chavez.'
    print 'ej. DIFERENCIA_PARTICIPACION = 300 filtra todas aquellas mesas donde la diferencia de participacion en ambas elecciones haya sido mayor a 300% (tres veces la cantidad de electores).'
    exit(1)

DIF_CON_CHAVEZ = int(argv[1])
DIF_PARTICIPACION = int(argv[2])

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

votos_chavez, votos_maduro, mesas_afectadas = 0, 0, 0
for id_mesa, resultados in mesas.items():
    total12 = resultados.chavez + resultados.capriles12
    total13 = resultados.maduro + resultados.capriles13
    distancia = float(max(total12, total13)) / max(min(total12, total13), 1)
    if (resultados.chavez != -1 and
       resultados.maduro > (1 + (DIF_CON_CHAVEZ/100.0)) * resultados.chavez and
       distancia < (DIF_PARTICIPACION/100.0)):
        votos_chavez += resultados.chavez
        votos_maduro += resultados.maduro
        mesas_afectadas += 1
        print id_mesa, resultados, resultados.url13
print ('\nHubo %d mesas donde Maduro tuvo %d%% mas votos que Chavez, solo contando centros en donde los votos por ambas opciones variaron en menos del %d%%.'
% (mesas_afectadas, DIF_CON_CHAVEZ, DIF_PARTICIPACION))
print ('\nEn estas mesas hubo %d votos para Maduro en 2013 y %d votos para Chavez en 2012, diferencia: %d'
% (votos_maduro, votos_chavez, votos_maduro - votos_chavez))
