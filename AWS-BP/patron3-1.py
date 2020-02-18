try:
  import unzip_requirements
except ImportError as e:
  print("error en modulo")
  print(e)

import re
import os
import csv
import boto3
import lambdawarmer

s3 = boto3.client('s3')

@lambdawarmer.warmer(send_metric=True)
def patrontuberiaenvio(event, context):
  #obtención de información del evento
  data = event['body-json']
  #selección de data del archivo text/csv recibido.
  r_csv = re.search(r'Content-Type: text/csv(.*\,\w)', data, re.DOTALL)
  #divición de filas tomando como refencia salto de linea \n
  lst = [i for i in r_csv.group(1).split('\n') if i != '']
  rows = [i.split(',') for i in lst]
  #eliminación de data no relevante.
  del rows[0 : 2]
  #para obtener la cantidad de registros a ingresar en dynamodb.
  r_text = re.search(r'Content-Disposition: form-data; name="numreg"(.*)', data, re.DOTALL)
  lst=[i for i in r_text.group(1).split('\n') if i != '']
  result = [i.split(',') for i in lst]
  numreg= result[2]
  numreg= int(str(numreg[0]))
  print("Numero de registros en archivo CSV: "+str(numreg))
  rowsFinal = rows[:numreg]
  archivo=""
  #creación de un archivo csv a partir de la lista del csv receptado
  with open("/tmp/data.csv", 'w',newline='') as f:
    f = csv.writer(f)
    f.writerows(rowsFinal)
  #codificación del archivo csv tipo "utf-8"
  with open("/tmp/data.csv") as f:
    archivo = f.read()
  encoded_string = archivo.encode("utf-8")
  try:
    #envio de archivo al bucket de s3
    print("patrontuberiaenvio")
    s3.put_object(Bucket='mi.aws',Key='datacsv.csv',Body=encoded_string)
  except Exception as ex:
    print("error")
    print(ex)