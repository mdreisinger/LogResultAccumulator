# aws_lambda_function.LogResultAccumulatore:
resource "aws_lambda_function" "LogResultAccumulatore" {
    architectures                  = [
        "x86_64",
    ]
    function_name                  = "LogResultAccumulator"
    image_uri                      = "126493000772.dkr.ecr.us-west-2.amazonaws.com/logresultaccumulator:latest"
    layers                         = []
    memory_size                    = 128
    package_type                   = "Image"
    reserved_concurrent_executions = -1
    role                           = "arn:aws:iam::126493000772:role/service-role/LogResultAccumulator-role-rrew47tg"
    skip_destroy                   = false
    source_code_hash               = "baccf3e11f3263e1ea280c2d2476acda0f9ee66fdc7038c4755786950072e143"
    tags                           = {}
    tags_all                       = {}
    timeout                        = 3

    ephemeral_storage {
        size = 512
    }

    tracing_config {
        mode = "PassThrough"
    }
}