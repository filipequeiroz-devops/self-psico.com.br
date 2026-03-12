import json
import boto3
import uuid
from datetime import datetime

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SiteAvaliacoes')

# 🔐 DEFINA SUA SENHA AQUI (ou use Variáveis de Ambiente do Lambda)
ADMIN_PASSWORD = "Angela123@"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,PUT,OPTIONS" # Adicionado PUT
}

def lambda_handler(event, context):
    try:
        # Pega o método de diferentes formas dependendo da config do API Gateway
        method = event.get("requestContext", {}).get("http", {}).get("method", 
                 event.get("httpMethod", ""))

        # 🔹 PRE-FLIGHT (CORS)
        if method == "OPTIONS":
            return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

        # 🔹 GET → Listar depoimentos
        if method == "GET":
            response = table.scan()
            # Ordenar por data (opcional)
            items = sorted(response.get("Items", []), key=lambda x: x.get('created_at', ''), reverse=True)
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": json.dumps(items)
            }

        # 🔹 POST → Novo depoimento (Paciente)
        if method == "POST":
            body = json.loads(event.get("body", "{}"))
            item = {
                "id": str(uuid.uuid4()),
                "nome": body.get("nome"),
                "mensagem": body.get("mensagem"),
                "estrelas": body.get("estrelas"),
                "resposta_admin": None, # Inicia vazio
                "created_at": datetime.utcnow().isoformat()
            }
            table.put_item(Item=item)
            return {
                "statusCode": 201,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Depoimento salvo"})
            }

        # 🔹 PUT → Responder depoimento (Apenas Angela)
        if method == "PUT":
            body = json.loads(event.get("body", "{}"))
            
            # 1. Verifica a senha
            if body.get("admin_key") != ADMIN_PASSWORD:
                return {
                    "statusCode": 403,
                    "headers": CORS_HEADERS,
                    "body": json.dumps({"error": "Acesso negado: Senha incorreta"})
                }

            # 2. Atualiza apenas o campo de resposta no DynamoDB
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