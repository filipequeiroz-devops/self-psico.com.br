output lambda_id {
  value       = aws_lambda_function.selfpsico.id
}

output api_gateway_url {
   value      = "${aws_apigatewayv2_api.selfpsico-API.api_endpoint}/depoimentos"
  description = "API Gateway URL"
}


output s3_bucket_name {
  value       = aws_s3_bucket.selfpsicobucket.id
  description = "S3 Bucket Name"
}