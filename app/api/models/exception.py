
MESSAGE = {
    400: "It’s not Token",
    401: "만료된 토큰",
    403: "Token Permission Error",
    404: "User Not found",
    405: "User that already exists"
}

class TokenException(Exception):
    def __init__(
            self, 
            status:int,
            data: any = None
        ) -> None:
        self.status = status
        self.data = data.__str__()
        self.message = MESSAGE[status] if MESSAGE.get(status) != None else "Failed"
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status={self.status!r}, message={self.message!r}, data={self.data!r})"