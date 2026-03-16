#aqui eu vou importar tanto a api gateway quanto a integração com a lambda, e também irei importar as rotas
resource "aws_apigatewayv2_api" "selfpsico-API" {

    description                  = "Created by AWS Lambda"
    ip_address_type              = "ipv4"
    name                         = "selfpsico-API"
    protocol_type                = "HTTP"
    region                       = "us-east-1"
    route_selection_expression   = "$request.method $request.path"

    cors_configuration {
        allow_credentials = false
        allow_headers     = [
            "authorization",
            "content-type",
        ]
        allow_methods     = [
            "GET",
            "OPTIONS",
            "POST",
            "PUT",
        ]
        allow_origins     = [
            "*",
        ]
        expose_headers    = []
        max_age           = 0
    }
}

resource "aws_apigatewayv2_integration" "selfpsico-integration" {
      api_id                                    = aws_apigatewayv2_api.selfpsico-API.id
      integration_uri                           = aws_lambda_function.selfpsico.invoke_arn
      connection_type                           = "INTERNET"
      integration_method                        = "POST"
      integration_type                          = "AWS_PROXY"
      payload_format_version                    = "2.0"
      region                                    = "us-east-1"
      timeout_milliseconds                      = 30000
  }


resource "aws_apigatewayv2_route" "route_depoimentos_post" {
      api_id                                    = aws_apigatewayv2_api.selfpsico-API.id
      route_key                                 = "POST /depoimentos"
      target                                    = "integrations/${aws_apigatewayv2_integration.selfpsico-integration.id}"
  }

resource "aws_apigatewayv2_route" "route_depoimentos_get" {
      api_id                                    = aws_apigatewayv2_api.selfpsico-API.id
      route_key                                 = "GET /depoimentos"
      target                                    = "integrations/${aws_apigatewayv2_integration.selfpsico-integration.id}"
  }

#criando metodo novo - put
resource "aws_apigatewayv2_route" "route_depoimentos_put" {
      api_id                                    = aws_apigatewayv2_api.selfpsico-API.id
      route_key                                 = "PUT /depoimentos"
      target                                    = "integrations/${aws_apigatewayv2_integration.selfpsico-integration.id}"
  }

#criando metodo novo - delete
resource "aws_apigatewayv2_route" "route_depoimentos_delete" {
      api_id                                    = aws_apigatewayv2_api.selfpsico-API.id
      route_key                                 = "DELETE /depoimentos"
      target                                    = "integrations/${aws_apigatewayv2_integration.selfpsico-integration.id}"
  }