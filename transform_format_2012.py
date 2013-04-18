import pdb
import csv
import sys
campos = ["state_id", "county_id", "township_id", "voting_center_id", "voting_table_id", "cne_new_code", "table_number"]
candids = ["chavez", "capriles", "chirino", "sequera", "reyes", "bolivar", "NULOS"]
filename = sys.argv[1]
fout = open('newformat.csv','w')
with open(filename, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(10024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    cnt = 0
    for item in reader:
        if cnt==0:
            for item in campos:
                fout.write(item+',')
            fout.write('candidato,votos\n')

        elif cnt >0:
            cs = ''
            for campo in [0, 2, 4, 8, 10, 9, 10]:
                cs = cs + item[campo]+','
            for candidato in range(11,18):
                fout.write(cs+candids[candidato-11]+','+item[candidato]+'\n')
        cnt = cnt + 1

fout.close()
