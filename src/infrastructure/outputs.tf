output lambda_id {
  value       = aws_lambda_function.selfpsico.id
}

output api_gateway_url {
  value       = aws_api_gateway_rest_api.selfpsico.invoke_url
  description = "API Gateway URL"
}

output s3_bucket_name {
  value       = aws_s3_bucket.selfpsico.bucket
  description = "S3 Bucket Name"
}