zip -r ../lambda.zip lambda_function.py
aws lambda update-function-code \
  --function-name tuprwareProxy \
  --zip-file fileb://../lambda.zip