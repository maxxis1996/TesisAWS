try:
  import unzip_requirements
except ImportError as e:
  print("error en modulo")
  print(e)
import boto3
import os
import uuid
import json
import re

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE_NAME'])

@lambdawarmer.warmer(send_metric=True)
def patronfanout(event, context):
  data = event['body-json']
  r_csv = re.search(r'Content-Type: text/csv(.*\,\w)', data, re.DOTALL)
  lst = [i for i in r_csv.group(1).split('\n') if i != '']
  rows = [i.split(',') for i in lst]
  del rows[0 : 3]
  r_text = re.search(r'Content-Disposition: form-data; name="numreg"(.*)', data, re.DOTALL)
  lst=[i for i in r_text.group(1).split('\n') if i != '']
  result = [i.split(',') for i in lst]  
  numreg= result[2]
  numreg= int(str(numreg[0]))
  rowsFinal = rows[:numreg]
  listaParticionada = [""]
  bandera=True
  #Divición del numero total de registros para 5 trabajadores
  umbral=int((numreg/5))
  rangoInicio=0
  rangoFin=umbral
  #bucle donde se particiona la lista de elementos a almacenar
  for i in range(5):
    if bandera:
      listaParticionada= rowsFinal[rangoInicio:rangoFin]
      bandera=False
    elif bandera==False:
      listaParticionada= rowsFinal[rangoInicio:rangoFin]
      bandera=True
    rangoInicio=rangoFin
    rangoFin=rangoFin+umbral    
    try:
      #creacion de un diccionario con la información a enviar a cada trabajador
      x = {"list" : listaParticionada,"count" : i}
      #Envio de información particionada a cada trabajador
      lambda_client.invoke(
        FunctionName="aws-patrones-dev-trabajadores",
        InvocationType='Event',
        Payload=json.dumps(x)
      )
      print("Lambda invocation message:")
    except Exception as ex:
      print(ex)

def trabajadores(event, context):
  #Recepción de información particionada
  coun = int(event['count'])
  print(coun)
  rowsFinal = event['list']
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
