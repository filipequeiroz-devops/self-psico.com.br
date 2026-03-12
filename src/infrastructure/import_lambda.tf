data "archive_file" "authorize_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_handler/"
  output_path = "${path.module}/lambda_handler/payload/lambda_authorize_payload.zip"
}

resource "aws_lambda_function" "selfpsico" {
    function_name                  = "selfpsico"
    filename      = data.archive_file.authorize_zip.output_path
    handler                        = "return_dynamodbitems.lambda_handler" # inside zip file, search for o return_dynamodbitems.py
    memory_size                    = 128
    package_type                   = "Zip"
    region                         = "us-east-1"
    reserved_concurrent_executions = -1
    role                           = "arn:aws:iam::307162859835:role/service-role/selfpsico-role-u4y8pxh4"
    runtime                        = "python3.10"
    timeout                        = 3

    source_code_hash = data.archive_file.authorize_zip.output_base64sha256
    
    ephemeral_storage {
        size = 512
    }

    logging_config {
        application_log_level = null
        log_format            = "Text"
        log_group             = "/aws/lambda/selfpsico"
        system_log_level      = null
    }

    tracing_config {
        mode = "PassThrough"
    }
}