from enum import Enum

class RequestType(Enum):
    info = 'info'
    change_appearance = 'change_appearance'
    quiz = 'quiz'
    contact = 'contact'
    create_playlist = 'create_playlist'
    recap = 'recap'
    other = 'other'
