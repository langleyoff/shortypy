from pydantic import BaseModel


class ErrorLinkNotFound(BaseModel):
    detail: str


class ErrorLinkCodeAlreadyExists(BaseModel):
    detail: str
