from pydantic import BaseModel


class MessageOutput(BaseModel):
    message: str


class EntityCreatedOutput(MessageOutput):
    reference: str
