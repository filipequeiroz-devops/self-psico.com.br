resource "aws_s3_bucket" "selfpsicobucket" {
      provider                    = aws.saopaulo  #bucket está numa region diferente dos demais recursos, então preciso especificar o provider"    
      bucket                      = "self-psico.com.br"
      policy                      = jsonencode(
          {
              Statement = [
                  {
                     Action    = "s3:GetObject"
                      Effect    = "Allow"
                      Principal = "*"
                     Resource  = "arn:aws:s3:::self-psico.com.br/*"
                      Sid       = "PublicReadGetObject"
                  },
              ]
              Version   = "2012-10-17"
          }
      )

      grant {
          id          = "36f938009b1b5440915ec44c06bab1305722d106dabaf79d6c23ec21ca8ed66f"
          permissions = [
              "FULL_CONTROL",
          ]
          type        = "CanonicalUser"
          uri         = null
      }

      server_side_encryption_configuration {
          rule {
              bucket_key_enabled = false

              apply_server_side_encryption_by_default {
                  kms_master_key_id = null
                  sse_algorithm     = "AES256"
              }
          }
      }

      versioning {
          enabled    = true
          mfa_delete = false
      }

      website {

          index_document           = "index.html"
      }
  }