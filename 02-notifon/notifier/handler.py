import json


def hello(event, context):

    # Use this code if you don't use the http event with the LAMBDA-PROXY

    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
