from asyncore import write
from multiprocessing.resource_sharer import stop
import sys
import csv
from datetime import datetime

#GUARDADO DE DATOS
nombre_csv = sys.argv[1]
dni_pedido = sys.argv[2]
salida_pedido = sys.argv[3]
tipo_pedido = sys.argv[4]
estado_pedido = None
rango_pedido = None

if len(sys.argv) == 6:
    opcional = sys.argv[5]
    estados_posibles = ["PENDIENTE", "RECHAZADO", "APROBADO"]
    if opcional in estados_posibles:
        estado_pedido = opcional
    else:
        rango_pedido = opcional.split(":")
        inicio = datetime.timestamp(datetime.strptime(rango_pedido[0], "%d-%m-%Y"))
        fin = datetime.timestamp(datetime.strptime(rango_pedido[1], "%d-%m-%Y")) 

elif len(sys.argv) == 7:
    estado_pedido = sys.argv[5]
    rango_pedido = sys.argv[6].split(":")
    inicio = datetime.timestamp(datetime.strptime(rango_pedido[0], "%d-%m-%Y"))
    fin = datetime.timestamp(datetime.strptime(rango_pedido[1], "%d-%m-%Y"))



salida = []

#FILTRADO DE DATOS

with open(nombre_csv,'r') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=",")
        for fila in lector:
            dni_csv = fila[8]
            tipo_csv = fila[9]
            estado_csv = fila[10]
            fecha_csv = float(fila[6])

            if dni_csv != dni_pedido or tipo_csv != tipo_pedido :
                continue
            if estado_pedido != None and estado_csv != estado_pedido:
                continue
            if rango_pedido and (fecha_csv < inicio or fecha_csv > fin):
                continue
            salida.append(fila)

#CONDICIONES
conjunto = set()
for i, fila in enumerate(salida):
    nro_cheque_salida = fila[0]
    nro_cuenta_salida = fila[3]
    dni_salida = fila[8]
    if (nro_cheque_salida,nro_cuenta_salida, dni_salida) in conjunto:
        print(f'Hay inconsistencias en la fila {i}')
        quit()
    else:
        conjunto.add((nro_cheque_salida,nro_cuenta_salida, dni_salida))


#SALIDA
if salida_pedido == 'PANTALLA':
    for fila in salida:
        print(",".join(fila))

elif salida_pedido == 'CSV':
    datos_filtrados = [[fila[3], fila[5], fila[6], fila[7]] for fila in salida]
    ahora = (datetime.now()).strftime("%d-%m-%Y")
    with open(f'{fila[8]}-{ahora}.csv','w',newline='') as csv_salida:
        writer = csv.writer(csv_salida)
        writer.writerows(datos_filtrados)
    