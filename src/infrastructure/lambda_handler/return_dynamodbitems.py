import json
import boto3
import uuid
import os # Adcionado para ler
from datetime import datetime
from decimal import Decimal  

# 2. NOVA CLASSE: Converte Decimal para tipos que o JSON entende (int ou float)
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SiteAvaliacoes')

ADMIN_PASSWORD = os.environ.get("SENHA_ANGELA") # Lê a variavei de ambiente "senha_angela" que foi criada a partir do arquivo variables.tf e variaveis.tfvars, omitidos no git

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
}

def lambda_handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method", 
                 event.get("httpMethod", ""))

        if method == "OPTIONS":
            return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

        if method == "GET":
            response = table.scan()
            items = sorted(response.get("Items", []), key=lambda x: x.get('created_at', ''), reverse=True)
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                # 3. AJUSTE: Adicionado cls=DecimalEncoder para não dar erro 500
                "body": json.dumps(items, cls=DecimalEncoder)
            }

        if method == "POST":
            body = json.loads(event.get("body", "{}"))
            item = {
                "id": str(uuid.uuid4()),
                "nome": body.get("nome"),
                "mensagem": body.get("mensagem"),
                "estrelas": body.get("estrelas"),
                "resposta_admin": None,
                "created_at": datetime.utcnow().isoformat()
            }
            table.put_item(Item=item)
            return {
                "statusCode": 201,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Depoimento salvo"})
            }

        if method == "PUT":
            body = json.loads(event.get("body", "{}"))
            
            if body.get("admin_key") != ADMIN_PASSWORD:
                return {
                    "statusCode": 403,
                    "headers": CORS_HEADERS,
                    "body": json.dumps({"error": "Acesso negado: Senha incorreta"})
                }

            table.update_item(
                Key={'id': body.get("id")},
                UpdateExpression="set resposta_admin = :r",
                ExpressionAttributeValues={':r': body.get("resposta_admin")},
                ReturnValues="UPDATED_NEW"
            )
        

            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Resposta publicada!"})
            }
        
        if method == "DELETE":
            body = json.loads(event.get("body", "{}"))

            if body.get("admin_key") != ADMIN_PASSWORD:
                return {
                    "statusCode": 403,
                    "headers": CORS_HEADERS,
                    "body": json.dumps({"error": "Acesso negado"})
                }

            table.delete_item(
                Key={'id': body.get("id")}
            )

            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Depoimento removido com sucesso!"})
            }

        return {
            "statusCode": 405,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Method not allowed"})
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }