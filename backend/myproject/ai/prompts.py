class Prompts:
    create_file_search_assistant_instr = "You are a very helpful assistant who will give me a detailed summary of the information in the documents that I have uploaded."
    @staticmethod
    def process_link_messages(link: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of what the following website is about:
        {link}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_text_messages(text: str) -> list:
        human_message_str = f"""
        Give me a detailed summary of the text denoted by [[[ ]]]. 
        [[[ 
            {text} 
        ]]]
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_transcript_messages(transcript: str) -> list:
        human_message_str = f"""
        Give me a very detailed summary of the following transcript:
        {transcript}
        """
        return [{"role": "user", "content": human_message_str}]
    
    @staticmethod
    def process_image_messages(base64_image: str, detail='auto') -> list:
        return [
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "Give me a detailsed summary of the information portrayed in the following image:"},
                {
                "type": "image_url",
                "image_url": {
                    'url': f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail
                },
                },
            ],
            }
        ]
        
    @staticmethod
    def process_document_messages(message_file) -> list:
        mes = [{
        "role": "user",
        "content": "Give me a detailed summary of the information in the following document.",
        # Attach the new file to the message.
        "attachments": [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
        }]
        print(mes)
        return mes
    
    @staticmethod
    def ask_assistant_file_search_messages(message_file = None) -> list:
        messages = [{
            "role": "user",
            "content": "Give me a very detailed description of the information in the documents that I have uploaded.",
        }]
        # Attach a new file to the message.
        if message_file: 
            messages[0]['attachments'] = [{ "file_id": message_file.id, "tools": [{"type": "file_search"}] }]
        return messages
