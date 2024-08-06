import os


class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    # File types supported by OpenAI's vision model
    vision_file_types = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    # File types not supported by OpenAI's vision model
    not_supported_image_file_types = ['avif', 'heic']
    image_file_types = vision_file_types + not_supported_image_file_types
    