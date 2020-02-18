try:
  import unzip_requirements
except ImportError as e:
  print("error en modulo")
  print(e)
from uuid import uuid4
import boto3
import os
import json
import re
import lambdawarmer
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TABLE_NAME'])

@lambdawarmer.warmer(send_metric=True)
def BOTO(event, context):
  #Obtener numero de consulta a ejecutar
  data = event['body-json']
  r_text = re.search(r'Content-Disposition: form-data; name="numConsul"(.*)', data, re.DOTALL)
  lst=[i for i in r_text.group(1).split('\n') if i != '']
  result = [i.split(',') for i in lst]
  numreg= result[2]
  numreg= int(str(numreg[0]))
  
  #Ejecución de consultas de acuerdo a selección en formulario. 
  if numreg==1:
    #Obtener valor de variable para la condición.
    r_text = re.search(r'Content-Disposition: form-data; name="salario"(.*)', data, re.DOTALL)
    lst=[i for i in r_text.group(1).split('\n') if i != '']
    result = [i.split(',') for i in lst]
    salario= result[2]
    variable= str(salario[0])
    variable="'"+variable+"'"
    response = table.query(
      KeyConditionExpression=Key('id').eq('02309d4d-aacb-4998-b192-8bbccbd98957')
      )
    
  elif numreg==2:
    #Obtener valor de variable para la condición.
    r_text = re.search(r'Content-Disposition: form-data; name="salario"(.*)', data, re.DOTALL)
    lst=[i for i in r_text.group(1).split('\n') if i != '']
    result = [i.split(',') for i in lst]
    salario= result[2]
    variable= int(str(salario[0]))
    response = table.scan(
      ProjectionExpression="id,salary,sex",
      #Consulta que devuelve valores mayores o iguales a variable salario
      FilterExpression=Attr('salary').gt(variable)
    )
  elif numreg==3:
    response = table.scan()
  items = response['Items']
  print(items)