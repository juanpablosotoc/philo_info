from enum import Enum
from pydantic import BaseModel


class Provider(Enum):
    google = 'google'
    apple = 'apple'
    microsoft = 'microsoft'
