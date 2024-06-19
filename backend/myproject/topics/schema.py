from pydantic import BaseModel


class NQuestionsTopics(BaseModel):
    n_topics: int
    n_questions: int
