import enum
import os

class Mark(enum.Enum):
    undefined = -1
    dislike = 0
    like = 1


DEFAULT_URL_DATA = {
    'mark': Mark.undefined.name,
    "prediction": Mark.undefined.name,
    'encoding': []
}

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
