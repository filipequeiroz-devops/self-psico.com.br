output lambda_id {
  value       = aws_lambda_function.selfpsico.id
}

output api_gateway_url {
  value       = aws_api_gateway_rest_api.selfpsico.invoke_url
  description = "API Gateway URL"
}