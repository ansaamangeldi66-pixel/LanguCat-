import aiohttp
import json
import asyncio
from config import HUGGINGFACE_API_TOKEN, HUGGINGFACE_API_URL

class ChatHandler:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        self.conversation_history = {}
        self.last_request = {}
        self.rate_limit = 1  # seconds between requests
        self.max_history = 5  # number of exchanges to keep

    async def get_response(self, user_id: int, message: str) -> str:
        """Get response from API with grammar checking"""
        try:
            # Rate limiting
            await self._handle_rate_limit(user_id)
            
            # Format prompt with grammar checking instructions
            prompt = self._create_grammar_prompt(message)
            
            # Get API response
            response = await self._make_api_request(prompt)
            
            # Update conversation history
            self._update_history(user_id, message, response)
            
            return response
            
        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            raise Exception(f"Chat API error: {str(e)}")

    def _create_grammar_prompt(self, message: str) -> str:
        """Create a prompt that includes grammar checking instructions"""
        return (
            "As English teacher, check grammar and reply:\n"
            "If errors found - start with 'Grammar: ' list errors and corrections\n"
            "If no errors - start with 'Grammar: Perfect!'\n"
            "Then give a short response.\n\n"
            f"Message: {message}"
        )

    async def _handle_rate_limit(self, user_id: int):
        """Handle rate limiting for requests"""
        current_time = asyncio.get_event_loop().time()
        if user_id in self.last_request:
            time_passed = current_time - self.last_request[user_id]
            if time_passed < self.rate_limit:
                await asyncio.sleep(self.rate_limit - time_passed)
        self.last_request[user_id] = current_time

    async def _make_api_request(self, prompt: str) -> str:
        """Make request to HuggingFace API"""
        print("\nSending request to API")
        print(f"Prompt: {prompt[:200]}...")  # Print first 200 chars
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                HUGGINGFACE_API_URL,
                headers=self.headers,
                json={"inputs": prompt, "parameters": {"truncation": True, "max_length": 100}}
            ) as response:
                if response.status != 200:
                    print(f"API Error: Status {response.status}")
                    error_text = await response.text()
                    print(f"Error response: {error_text}")
                    raise Exception(f"API request failed: {response.status}")
                
                result = await response.json()
                print(f"API Response received: {result}")
                
                if not isinstance(result, list) or not result:
                    raise Exception("Invalid API response format")
                
                bot_response = result[0].get('generated_text', '').strip()
                if not bot_response:
                    raise Exception("Empty response from API")
                
                print(f"Final response: {bot_response}")
                return bot_response

    def _update_history(self, user_id: int, message: str, response: str):
        """Update conversation history for user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        history = self.conversation_history[user_id]
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        
        # Keep only last N exchanges
        if len(history) > self.max_history * 2:
            self.conversation_history[user_id] = history[-self.max_history * 2:]

    def reset_conversation(self, user_id: int):
        """Reset conversation history for user"""
        self.conversation_history.pop(user_id, None)
