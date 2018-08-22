#!/bin/sh

# start in ../bartbot/
SRCPATH="bartbot/env/src"
if [[ ! "$PWD" == *$SRCPATH ]]; then
  echo "Error: current directory must be \"$SRCPATH\"." 
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

echo "Starting AWS Lambda update at $(date +"%r")..." >&1

# begin updating AWS Lambda function
echo "Adding handler to zip..." >&1
zip ./handler.zip handler.py >&6 2>&1

echo "Adding site-packages to zip..." >&1
cd ../lib/python3.6/site-packages/
shopt -s extglob
zip -gr ../../../src/handler.zip !(boto*|awscli*|pip*|s3*) >&6 2>&1

echo "Uploading zip to s3..." >&1
cd ../../../src
aws s3 cp handler.zip s3://bartbot-bucket/handler.zip >&6 2>&1

echo "Updating AWS Lambda function..." >&1
aws lambda update-function-code --function-name pyProcessMessages --s3-bucket bartbot-bucket --s3-key handler.zip >&6 2>&1

echo "Updated AWS Lambda function at $(date +"%r")." >&1