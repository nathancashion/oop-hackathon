import requests
import json
import os

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"  # Use the most capable model available

def call_openai(prompt='Write a Python function that returns the square of a number', model=None):
    """
    Call Ollama API instead of OpenAI for local inference.
    Returns an object that mimics the OpenAI response structure.
    """
    if model is None:
        model = DEFAULT_MODEL
    
    # Prepare the request payload for Ollama
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2000
        }
    }
    
    try:
        # Call Ollama generate endpoint
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120  # Medical explanations might take a while
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Create a mock response object that matches OpenAI's structure
            class MockChoice:
                def __init__(self, content):
                    self.message = type('obj', (object,), {'content': content})()
            
            class MockResponse:
                def __init__(self, content):
                    self.choices = [MockChoice(content)]
            
            return MockResponse(result['response'])
        else:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to Ollama: {e}")

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def list_available_models():
    """Get list of available Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except:
        return []

if __name__ == "__main__":
    # Test the Ollama connection
    print("Testing Ollama connection...")
    if test_ollama_connection():
        print("✓ Ollama is running")
        models = list_available_models()
        print(f"✓ Available models: {', '.join(models)}")
        
        # Test a simple prompt
        print("\nTesting with a simple prompt...")
        try:
            result = call_openai("Explain what MRI stands for in one sentence.")
            print(f"✓ Response: {result.choices[0].message.content}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print("✗ Ollama is not running. Please start Ollama first.")