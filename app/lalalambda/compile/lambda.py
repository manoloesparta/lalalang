import logging
import lalalang
from utils import (
    get_key_from_headers,
    build_response,
    BadRequestException,
)


def handler(event, context):
    """Lambda handler

    Parameters
    ----------
    event: dict, required
            API Gateway Lambda Proxy Input Format

    context: object, required
            Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
    """
    try:
        source = get_key_from_headers(event, "source")
        result = lalalang.run(source)
        return build_response(200, result)
    except BadRequestException as e:
        logging.error(str(e))
        return build_response(e.status, e)
    except Exception as e:
        logging.error(str(e))
        return build_response(500, "Internal server error")
