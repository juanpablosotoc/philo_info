from .aws import documentDBClient, DocumentDBClient

# assumes that we have already connected to the database
class UserDB():
    email: str
    db: DocumentDBClient

    def __init__(self, email: str) -> None:
        self.email = email
        self.db = documentDBClient
