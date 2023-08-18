from fastapi.responses import JSONResponse

def baseResponse(**kwargs):
    if kwargs.get("message") == None:
        kwargs["message"] = "success"
    if kwargs.get("data") == None:
        kwargs["data"] = None
    if kwargs.get("status") == None:
        kwargs["status"] = 200
    print(kwargs)
    return kwargs