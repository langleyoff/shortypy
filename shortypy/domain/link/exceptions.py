from shortypy.exceptions import ShortypyException


class LinkCodeAlreadyExistsError(ShortypyException):
    pass


class LinkNotFoundError(ShortypyException):
    pass
