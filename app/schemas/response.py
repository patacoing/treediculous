from enum import Enum
from pydantic import BaseModel


class Classification(Enum):
    UGLY = "ugly"
    NICE = "nice"


class ResponseSchemas(BaseModel):
    classname: Classification
    probability: float