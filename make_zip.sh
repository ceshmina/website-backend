#!/bin/bash

rm lambda_function.zip
cd /usr/local/lib/python3.11/site-packages
zip -r9 /app/lambda_function.zip .
cd /usr/local/lib64/python3.11/site-packages
zip -r9 /app/lambda_function.zip .
cd /app
zip -g lambda_function.zip lambda_function.py
