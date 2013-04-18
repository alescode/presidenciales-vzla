import csv
from collections import defaultdict

def construir_url(cne_new_id):
    if eleccion:
        return 'http://www.cne.gob.ve/resultado_presidencial_%s/pp/0/reg_%s.html' % (str(eleccion), str(cne_new_id))
    return None

def resultado_centro(cne_new_id):
    capriles, maduro, nulos = 0, 0, 0
    for mesa in centros[cne_new_id].values():
        capriles += mesa['capriles']
        maduro += mesa['maduro']
        nulos += mesa['NULOS']
    return {'capriles': capriles, 'maduro': maduro, 'NULOS': nulos}

def resultado_parroquia(parroquia_id):
    capriles, maduro, nulos = 0, 0, 0
    for cne_new_id in parroquias[parroquia_id].keys():
        res = resultado_centro(cne_new_id)
        capriles += res['capriles']
        maduro += res['maduro']
        nulos += res['NULOS']
    return {'capriles': capriles, 'maduro': maduro, 'NULOS': nulos}

def resultado_municipio(municipio_id):
    capriles, maduro, nulos = 0, 0, 0
    for parroquia_id in municipios[municipio_id].keys():
        res = resultado_parroquia(parroquia_id)
        capriles += res['capriles']
        maduro += res['maduro']
        nulos += res['NULOS']
    return {'capriles': capriles, 'maduro': maduro, 'NULOS': nulos}

def resultado_estado(estado_id):
    capriles, maduro, nulos = 0, 0, 0
    for municipio_id in estados[estado_id].keys():
        res = resultado_municipio(municipio_id)
        capriles += res['capriles']
        maduro += res['maduro']
        nulos += res['NULOS']
    return {'capriles': capriles, 'maduro': maduro, 'NULOS': nulos}

def resultado_pais():
    capriles, maduro, nulos = 0, 0, 0
    for estado_id in estados.keys():
        res = resultado_estado(estado_id)
        capriles += res['capriles']
        maduro += res['maduro']
        nulos += res['NULOS']
    return {'capriles': capriles, 'maduro': maduro, 'NULOS': nulos}

eleccion = None

estados = defaultdict(dict)
municipios = defaultdict(dict)
parroquias = defaultdict(dict)
centros = defaultdict(dict) # cne_new_code es la clave
mesas = defaultdict(dict) # cne_new_code + '_' + table_number es la clave

with open('data_2013.csv', 'rb') as csvfile:
    cnt = 0
    for fila in csv.reader(csvfile):
        # 0 state_id 
        # 1 county id
        # 2 township
        # 3 voting center
        # 4 voting table
        # 5 cne new code
        # 6 table number
        # 7 candidato
        # 8 votos
        if cnt != 0:
            mesa = fila[5] + '_' + fila[6]
            mesas[mesa][fila[7]] = int(fila[8])
            centros[fila[5]][mesa] = mesas[mesa]
            parroquias[fila[2]][fila[5]] = centros[fila[5]]
            municipios[fila[1]][fila[2]] = parroquias[fila[2]]
            estados[fila[0]][fila[1]] = municipios[fila[1]]
        cnt += 1
