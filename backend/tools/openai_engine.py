import os
from openai import OpenAI
from enum import Enum

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"

class OpenAIEngine:
    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def __call__(self, messages, stop_sequences=None):
        # Convert messages to OpenAI format
        formatted_messages = []
        for msg in messages:
            if isinstance(msg.get("content"), (list, dict)):
                content = str(msg["content"])
            else:
                content = msg["content"]
            
            role = msg.get("role", "user")
            if role in ["tool_call", "tool_response"]:
                role = "assistant"
            
            formatted_messages.append({
                "role": role,
                "content": content
            })
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            stop=stop_sequences,
            temperature=0.5,
        )
        return response.choices[0].message.content
