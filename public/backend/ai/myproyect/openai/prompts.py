# This class is used to store the prompts for the Openai calls.
class Prompts:
    @staticmethod
    def check_request_type(request: str) -> list:
        """Returns a list of messages that ask the assistant to check the type of request."""
        return [
            {
                'role': 'assistant',
                'content': """You are a very useful assistant who will respond only using json. You will be asked to determine the type of a request. The only possible types are:
                - 'info': answer this when the user is providing a piece of information, asking a question or asking you to explain something.
                - 'change_appearance': answer this when the user is asking you to change the appearance of the app.
                - 'quiz': answer this when the user is asking you to create a quiz.
                - 'contact': answer this when the user is asking you to contact someone.                
                    Ex: 
                        - Set a reminder to login to factic everyday at 5.
                        - Call me everyday to remind me to login to study.
                        - Call me everyday to remind me to login to factic.
                - 'create_playlist': answer this when the user is asking you to create a playlist of information or if the user is asking you to explain about a very big and vast topic.
                    Ex:
                        - Create a playlist of information about the history of the world.
                        - Help me study for my calculus exam.
                        - Help me study for my history exam.
                        - Help me study for my biology exam.
                        - Create a playlist of the history of the world.
                - 'recap': Answer this when the user is asking you to recap on some piece of information.
                - 'other': answer this when the user is asking you to do something else, is saluting you or isnt doing anything specific.
                    Ex:
                        - Good morning.
                        - Good afternoon.
                        - Hello
                        - How are you?
                        - What's up?
                        - Goodbye.
                        - Bye.
                        - I would love to hang out with you.
                """
            },
            {
                'role': 'user',
                'content': """What's the type of the request denoted by [[[ ]]]. 
                [[[
                    What's your mission?
                ]]]"""
            },
            {
                'role': 'assistant',
                'content': """{
                    "type": "info"
                }"""
            },
            {
                'role': 'user',
                'content': """What's the type of the request denoted by [[[ ]]]. 
                [[[
                    Change the background color to blue.
                ]]]"""
            },
            {
                'role': 'assistant',
                'content': """{
                    "type": "change_appearance"
                }"""
            },
            {
                'role': 'user',
                'content': """What's the type of the request denoted by [[[ ]]]. 
                [[[
                    Create a quiz about the history of the world.
                ]]]"""
            },
            {
                'role': 'assistant',
                'content': """{
                    "type": "quiz"
                }"""
            },
            {
                'role': 'user',
                'content': """What's the type of the request denoted by [[[ ]]]. 
                [[[
                    Call me everyday to remind me to login to study.
                ]]]"""
            },
            {
                'role': 'assistant',
                'content': """{
                    "type": "contact"
                }"""
            },
            {
                'role': 'user',
                'content': """What's the type of the request denoted by [[[ ]]]. 
                [[[
                    How are you today?
                ]]]"""
            },
            {
                'role': 'assistant',
                'content': """{
                    "type": "other"
                }"""
            },
            {
                'role': 'user',
                'content': """What's the type of the request denoted by [[[ ]]]. 
                [[[
                    Help me study for my biology exam.
                ]]]"""
            },
            {
                'role': 'assistant',
                'content': """{
                    "type": "create_playlist"
                }"""
            },
            {
            "role": "user",
            "content": f"""What's the type of the request denoted by [[[ ]]]. 
            [[[
                {request}
            ]]]"""
            }
        ]
    
    @staticmethod 
    def get_processed_info_messages(text: str = '', image_urls: list = []):
        content_list = [{
            'type': 'text',
            'text': """Its possible that the user has uploaded files to the vector space attached to this thread, 
            if that is the case then please process the information in the files and provide a detailed explanation of the information. If there are no files in the vector space then you can skip this step."""
        }]
        if len(text) > 0:
            content_list.append({
            'type': 'text',
            'text': f"""The following is some information that the user provided, 
            please give me the information that the user is requesting or a thourough explanation of the information provided.\n[[[{text}]]]"""
            })
        for image_url in image_urls:
            content_list.append([
                {"type": "text", "text": "Give me a detailed description of the information in this image."},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                },
                },
            ])
        assert len(content_list) > 0, 'No content to process.'
        return [
            {
                'role': 'user',
                'content': content_list
            }
        ]
