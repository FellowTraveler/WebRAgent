import os
from openai import OpenAI
from app.services.llm_service import LLMService

class OpenAIService(LLMService):
    """Service for interacting with OpenAI's API"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    def _generate_completion(self, system_message, user_message, max_tokens):
        """
        Generate a completion using OpenAI's API
        
        Args:
            system_message (str): The system message
            user_message (str): The user message
            max_tokens (int): The maximum number of tokens to generate
            
        Returns:
            str: The generated response text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def _generate_chat_completion(self, messages, max_tokens):
        """
        Generate a chat completion using OpenAI's API
        
        Args:
            messages (list): The formatted message list
            max_tokens (int): The maximum number of tokens to generate
            
        Returns:
            str: The generated response text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content