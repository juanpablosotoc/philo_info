import os

class Config:
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
    POLL_TIMEOUT = 0.2
    # File types supported by OpenAI's vision model
    vision_file_types = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    AWS_REGION = 'us-west-2'