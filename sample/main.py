import functions_framework
from flask import Request


@functions_framework.http
def sample(request: Request):
    return 'Hello world!'
