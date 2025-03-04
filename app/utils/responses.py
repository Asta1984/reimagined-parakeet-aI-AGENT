# app/utils/responses.py
from fastapi import Response

class XMLResponse(Response):
    media_type = "application/xml"
    
    def __init__(self, content: str, status_code: int = 200):
        super().__init__(
            content=content,
            media_type=self.media_type,
            status_code=status_code
        )