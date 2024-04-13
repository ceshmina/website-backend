#!/bin/bash

pipenv install
PYTHON_DIR=$(pipenv --venv)/lib/python3.12/site-packages

ZIP_FILE="lambda_function.zip"
cd $PYTHON_DIR
zip -r9 $OLDPWD/$ZIP_FILE .

cd $OLDPWD
zip -g $ZIP_FILE lambda_function.py
