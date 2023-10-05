# RUN THIS INSIDE THE lambda/ DIRECTORY (run ../deploy.sh)
zip -r ../lambda.zip lambda_function.py
aws lambda update-function-code \
  --function-name tuprwareProxy \
  --zip-file fileb://../lambda.zip