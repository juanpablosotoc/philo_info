from .openai import chat
from aws import s3, dynamodb
import os

def transform_gutengerg_audio(content: str) -> str:
    # split the content by '<Audio>' and '</Audio>'
    parts = content.split('<Audio>')
    for i in range(1, len(parts)):
        # split the content by '</Audio>'
        textToRead, text = parts[i].split('</Audio>')
        audioFilePath = chat.text_to_speech(textToRead, 'alloy')
        audioName = os.path.basename(audioFilePath)
        # upload to aws s3
        s3.upload_file('factic-user-files', audioName, audioFilePath)
        # remove the file from the local machine
        os.remove(audioFilePath)
        # upload the file to dynamodb
        item = {
            'file_id': audioName,
        }
        dynamodb.put_item(item, 'files')
        # replace the audio tag with the audio tag
        parts[i] = f'<audio src="{s3.generate_public_url('factic-user-files', audioName)}"/> {text}'
    return ''.join(parts)
