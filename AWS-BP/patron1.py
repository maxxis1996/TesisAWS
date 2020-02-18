try:
  import unzip_requirements
except ImportError as e:
  print("error en modulo")
  print(e)
import boto3
import os
import uuid
import re
import lambdawarmer

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE_NAME'])

@lambdawarmer.warmer(send_metric=True)
def patronswsimple(event, context):
  #obtención de información del evento
  data = event['body-json']
  #selección de data del archivo text/csv recibido.
  r_csv = re.search(r'Content-Type: text/csv(.*\,\w)', data, re.DOTALL)
  #divición de filas tomando como refencia salto de linea \n
  lst = [i for i in r_csv.group(1).split('\n') if i != '']
  rows = [i.split(',') for i in lst]
  #eliminación de data no relevante.
  del rows[0 : 3]
  #para obtener la cantidad de registros a ingresar en dynamodb.
  r_text = re.search(r'Content-Disposition: form-data; name="numreg"(.*)', data, re.DOTALL)
  lst=[i for i in r_text.group(1).split('\n') if i != '']
  result = [i.split(',') for i in lst]  
  numreg= result[2]
  numreg= str(numreg[0])
  numreg= int(numreg)
  print("Número de registros insertados: "+str(numreg))
  #seleccionar la cantidad de registros para almacenar del archivo csv.
  rowsFinal = rows[:numreg]
  #Carga de registros a dynamodb con el proceso batch
  with table.batch_writer() as batch:
    for row in rowsFinal:
      batch.put_item(Item={
          'id': str(uuid.uuid4()),
          'serie': row[0],
          'rank': row[1],
          'discipline': row[2],
          'sex': row[3],
          'salary': row[4]
          })



          