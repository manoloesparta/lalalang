import json


class BadRequestException(Exception):
    """Exception for Bad Requests"""

    status = 400


def get_key_from_body(event, key):
    """Retieve specific key from the headers of a request event"""
    body = json.loads(event.get("body"))
    value = body.get(key)
    if not value:
        raise BadRequestException("Body don't contain key: %s" % key)
    return value


def build_response(status, message):
    """Create the format for the lambda response"""
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"output": str(message)}),
    }
