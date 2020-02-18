try:
  import unzip_requirements
except ImportError as e:
  print("error en modulo")
  print(e)
from uuid import uuid4
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model
import graphene
from graphene_pynamodb import PynamoObjectType, PynamoConnectionField
import json
import re
import lambdawarmer
#Definir atributos de la tabla de DynamoDB
class User(Model):
  class Meta:
    table_name = "tablapatronesmax"
    region = "us-east-1"
    host = "https://dynamodb.us-east-1.amazonaws.com"
  id = UnicodeAttribute(hash_key=True,null=False)
  discipline = UnicodeAttribute(null=False)
  rank = UnicodeAttribute(null=False)
  salary = NumberAttribute(default=0)
  serie = NumberAttribute(default=0)
  sex = UnicodeAttribute(null=False)
#Crear esquema GraphQL
class UserNode(PynamoObjectType):
  class Meta:
    model = User
    interfaces = (graphene.Node,)
#Ejecutar y devolver datos para la consulta
class Query(graphene.ObjectType):
  user = graphene.Field(UserNode, variable = graphene.String(required=True))
  usersCondition = graphene.List(UserNode, variable = graphene.Int(required=True))
  allUsers = graphene.List(UserNode)
  def resolve_user(self, *args, **kwargs):
    iD=kwargs.get('variable')
    print(iD)
    #Consulta que devuelve valor iguales a variable id
    return list(User.scan(id__eq='00c81dcc-8877-44da-8fee-6b9ebfbd4cf0'))
  def resolve_usersCondition(self, *args, **kwargs):
    salario=kwargs.get('variable')
    #Consulta que devuelve valores mayores o iguales a variable salario
    return list(User.scan(salary__gt=salario))
  def resolve_allUsers(self, *args, **kwargs): 
    #Consulta que devuelve todos los valores
    return list(User.scan())

schema = graphene.Schema(query=Query)

@lambdawarmer.warmer(send_metric=True)
def patrongrafico(event, context):
  #Obtener numero de consulta a ejecutar
  data = event['body-json']
  r_text = re.search(r'Content-Disposition: form-data; name="numConsul"(.*)', data, re.DOTALL)
  lst=[i for i in r_text.group(1).split('\n') if i != '']
  result = [i.split(',') for i in lst]
  numreg= result[2]
  numreg= int(str(numreg[0]))
  
  variable=0
  variable2=''
  try:
    #Configurar variable de consulta de acuerdo a selección en formulario 
    if numreg==1:
      #Obtener valor de variable para la condición.
      r_text = re.search(r'Content-Disposition: form-data; name="salario"(.*)', data, re.DOTALL)
      lst=[i for i in r_text.group(1).split('\n') if i != '']
      result = [i.split(',') for i in lst]
      salario= result[2]
      variable= str(salario[0])
      variable2='query1'
    elif numreg==2:
      r_text = re.search(r'Content-Disposition: form-data; name="salario"(.*)', data, re.DOTALL)
      lst=[i for i in r_text.group(1).split('\n') if i != '']
      result = [i.split(',') for i in lst]
      salario= result[2]
      variable= int(str(salario[0]))
      variable2='query2'
    elif numreg==3:
      variable2='query3'
    #Estructura de las consultas y atributos a devolver
    query_string = '''
      query query1($variable: String!) {
        user(variable: $variable) {
          id
          discipline
        }
      }
      query query2($variable: Int!) {
        usersCondition(variable: $variable) {
          id
          salary
          sex
        }
      }
      query query3 {
        allUsers {
          id
          discipline
          rank
          salary
          serie
          sex
        }
      }
    '''
    #Ejecución de la consulta con variables adicionales
    result = schema.execute(
      query_string,
      operation_name=variable2,
      variables={'variable': variable},
    )
    print('errors', result.errors)
    print('data', result.data)
  except Exception as ex:
    print(ex)