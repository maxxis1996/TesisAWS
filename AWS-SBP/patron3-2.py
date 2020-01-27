def patrontuberia(event, context):
  try:
    import unzip_requirements
  except ImportError as e:
    print("error en modulo")
    print(e)
  from uuid import uuid4
  import json
  import boto3
  import re
  import uuid
  import logging
  import os
  import csv
  import pandas as pd
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(os.environ['DYNAMO_TABLE_NAME'])
  s3 = boto3.client('s3')
  #obtención de nombre del bucket
  bucket_name = event['Records'][0]['s3']['bucket']['name']
  #obtención de clave del archivo csv
  file_key = event['Records'][0]['s3']['object']['key']
  #obtención del archivo csv
  csv = s3.get_object(Bucket=bucket_name, Key=file_key)
  #selección de filas a utilizar
  df = pd.read_csv(csv['Body'], skip_blank_lines=True, usecols=['id', 'rank', 'discipline', 'sex','salary'])
  df = df.astype(str)
  df = df.fillna("NA")
  values = df.T.to_dict().values()
  #Carga de registros a dynamodb con el proceso batch
  with table.batch_writer() as batch:
    for row in values:
      batch.put_item(Item={
          'id': str(uuid.uuid4()),
          'serie': int(row["id"]),
          'rank': row["rank"],
          'discipline': row["discipline"],
          'sex': row["sex"],
          'salary': int(row["salary"])
          })
  

  