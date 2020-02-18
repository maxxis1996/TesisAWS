from uuid import uuid4
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
import graphene
from graphene_pynamodb import PynamoObjectType
import json


class User(Model):
  class Meta:
    table_name = 'tablapatron4max'
    region = 'us-east-1'
    host = 'https://dynamodb.us-east-1.amazonaws.com'

  id = UnicodeAttribute(hash_key=True)
  name = UnicodeAttribute(null=False)


if not User.exists():
  User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
  User(id=str(uuid4()), name="John Snow").save()
  User(id=str(uuid4()), name="Daenerys Targaryen").save()


class UserNode(PynamoObjectType):
  class Meta:
    model = User
    interfaces = (graphene.Node,)


class Query(graphene.ObjectType):
  users = graphene.List(UserNode)

  def resolve_users(self, args, context, info):
    return list(User.scan())


schema = graphene.Schema(query=Query)

query = '''
    query {
      users {
        id
      }
    }
'''
result = schema.execute(query)
print('errors', result.errors)
print('data', result.data)