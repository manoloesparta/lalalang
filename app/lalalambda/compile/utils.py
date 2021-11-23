import json


class BadRequestException(Exception):
    """Exception for Bad Requests"""

    status = 400


def get_key_from_body(event, key):
    """Retieve specific key from the headers of a request event"""
    value = event.get("body", {}).get(key)
    if not value:
        raise BadRequestException("Headers don't contain key: %s" % key)
    return value


def build_response(status, message):
    """Create the format for the lambda response"""
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps({"output": str(message)}),
    }
