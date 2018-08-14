#!/bin/sh

# TODO: add check for correct pwd

echo "adding handler to zip..."
cd lambdaEnv/src/
zip ../../handler.zip handler.py >/dev/null

echo "adding packages to zip..."
cd ../../lambdaEnv/lib/python3.6/site-packages/
shopt -s extglob
zip -gr ../../../../handler.zip !(boto*) >/dev/null

echo "copying zip to s3..."
cd ../../../..
aws s3 cp handler.zip s3://bartbot-bucket/handler.zip >/dev/null

echo "updating pyProcessMessages on lambda..."
aws lambda update-function-code --function-name pyProcessMessages --s3-bucket bartbot-bucket --s3-key handler.zip >/dev/null

echo "done."

