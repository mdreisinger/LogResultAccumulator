# aws_s3_bucket.logresultaccumulator:
resource "aws_s3_bucket" "logresultaccumulator" {
    bucket                      = "logresultaccumulator"
    object_lock_enabled         = false
    request_payer               = "BucketOwner"
    tags                        = {}
    tags_all                    = {}

    grant {
        id          = "262f7623cd8d1394e6e25e76b68524620a25d8b08183bfde78c6dc86e600d0bf"
        permissions = [
            "FULL_CONTROL",
        ]
        type        = "CanonicalUser"
    }

    server_side_encryption_configuration {
        rule {
            bucket_key_enabled = true

            apply_server_side_encryption_by_default {
                sse_algorithm = "AES256"
            }
        }
    }

    versioning {
        enabled    = false
        mfa_delete = false
    }
}

# aws_s3_bucket_notification.new_file:
resource "aws_s3_bucket_notification" "new_file" {
    bucket      = "logresultaccumulator"
    eventbridge = false

    lambda_function {
        events              = [
            "s3:ObjectCreated:*",
        ]
        id                  = "new_file"
        lambda_function_arn = "arn:aws:lambda:us-west-2:126493000772:function:LogResultAccumulator"
    }
}