#!/bin/sh

# start in ../bartbot/
if [[ ! "$PWD" == *bartbot/lambdaEnv/src ]]; then
  echo "Error: current directory must be \"../bartbot/lambdaEnv/src\"." 
  exit 1
fi

# file descriptor 6 to null
exec 6>/dev/null

# toggle verbosity
if [[ $# -ge 1 && $1 = "--verbose" || \
      $# -ge 1 && $1 = "-v" ]]; then
  exec 6>&1
  echo "Verbose mode."
fi

# begin updating AWS Lambda function
echo "Adding handler to zip..." >&1
zip ./handler.zip handler.py >&6 2>&1

echo "Adding packages to zip..." >&1
cd ../lib/python3.6/site-packages/
shopt -s extglob
zip -gr ../../../src/handler.zip !(boto*|awscli*|pip*|s3*) >&6 2>&1

echo "Copying zip to s3..." >&1
cd ../../../src
aws s3 cp handler.zip s3://bartbot-bucket/handler.zip >&6 2>&1

echo "Updating pyProcessMessages on lambda..." >&1
aws lambda update-function-code --function-name pyProcessMessages --s3-bucket bartbot-bucket --s3-key handler.zip >&6 2>&1

echo "Updated pyProcessMessages." >&1
