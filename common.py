import enum


class Mark(enum.Enum):
    undefined = -1
    dislike = 0
    like = 1


DEFAULT_URL_DATA = {
    'mark': Mark.undefined.name,
    "prediction": Mark.undefined.name,
    'encoding': []
}