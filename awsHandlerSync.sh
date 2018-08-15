#!/bin/sh

# TODO: add check for correct pwd
echo "are you in \"../bartbot/\"? (y/n)"
read inBartbot
[ ! "$inBartbot" = "y" ] && exit 1

# file descriptor 6 to null
exec 6>/dev/null

# toggle verbosity
if [ $# -ge 1 ] && [ "$1" = "--verbose" ] || [ $# -ge 1 ] && [ "$1" = "-v" ]
then
  exec 6>&1
  echo "verbose mode."
fi

echo "adding handler to zip..." >&1
cd lambdaEnv/src/
zip ../../handler.zip handler.py >&6 2>&1

echo "adding packages to zip..." >&1
cd ../../lambdaEnv/lib/python3.6/site-packages/
shopt -s extglob
zip -gr ../../../../handler.zip !(boto*) >&6 2>&1

echo "copying zip to s3..." >&1
cd ../../../..
aws s3 cp handler.zip s3://bartbot-bucket/handler.zip >&6 2>&1

echo "updating pyProcessMessages on lambda..." >&1
aws lambda update-function-code --function-name pyProcessMessages --s3-bucket bartbot-bucket --s3-key handler.zip >&6 2>&1

echo "done."

