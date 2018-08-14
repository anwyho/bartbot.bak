#!/bin/sh
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

echo "done."

