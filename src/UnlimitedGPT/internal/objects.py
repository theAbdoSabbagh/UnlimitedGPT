from typing import Optional

class ChatGPTResponse:
    """
    The response object returned by ChatGPT
    """
    def __init__(
        self,
        response: str,
        conversation_id: Optional[str] = None
    ):
        self.response = response
        self.conversation_id = conversation_id
    
    def __str__(self):
        return self.response
    
    def __repr__(self):
        return f'<ChatGPTResponse response="{self.response}" conversation_id="{self.conversation_id}">'
    