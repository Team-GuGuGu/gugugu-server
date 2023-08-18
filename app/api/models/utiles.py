from fastapi import Request
from .exception import TokenException
def requestsToken(request: Request):
    try:
        string = request.headers.get("Authorization").split(" ")
        header = string[0]
        token = string[1]
    except:
        raise TokenException(400)
    if header != "Dgswgr":
        raise TokenException(400)
    if token == None:
        raise TokenException(400)
    return token