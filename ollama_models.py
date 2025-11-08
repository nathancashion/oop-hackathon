"""
Ollama model integration for the medical AI assistant project.
This module provides an alternative to OpenAI using the local medgemma-assistant model.
"""

import subprocess
import json
from typing import Optional, Dict, Any


class OllamaClient:
    """Client for interacting with Ollama models locally."""
    
    def __init__(self, model_name: str = "medgemma-assistant"):
        self.model_name = model_name
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response using the Ollama model.
        
        Args:
            prompt: The user prompt/question
            system_prompt: Optional system prompt (will override Modelfile system prompt)
            
        Returns:
            Generated response text
        """
        # Build the command
        cmd = ["ollama", "run", self.model_name]
        
        # If system prompt is provided, add it to the prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        else:
            full_prompt = prompt
        
        try:
            result = subprocess.run(
                cmd + [full_prompt],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise Exception(f"Ollama error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise Exception("Ollama request timed out")
        except Exception as e:
            raise Exception(f"Failed to call Ollama: {str(e)}")
    
    def generate_diagnosis(self, report_text: str, context: str = "", age: Optional[int] = None) -> str:
        """
        Generate a patient-friendly diagnosis explanation.
        
        Args:
            report_text: The radiology report text
            context: Additional medical context
            age: Patient age for age-appropriate statistics
            
        Returns:
            Patient-friendly diagnosis explanation
        """
        age_context = f" The patient is {age} years old." if age else ""
        
        prompt = f"""Please analyze this radiology report and provide a patient-friendly explanation of the findings.{age_context}

Context: {context}

Report: {report_text}

Please provide:
1. A clear explanation of what was found
2. What these findings mean in everyday terms
3. How common these conditions are (especially for the patient's age if provided)
4. General guidance on next steps

Keep the response under 1000 characters and use a compassionate, reassuring tone."""
        
        return self.generate(prompt)
    
    def generate_care_plan(self, diagnosis: str, age: Optional[int] = None) -> str:
        """
        Generate treatment recommendations and care plan.
        
        Args:
            diagnosis: The diagnosis/findings summary
            age: Patient age for age-appropriate recommendations
            
        Returns:
            Treatment care plan recommendations
        """
        age_context = f" for a {age}-year-old patient" if age else ""
        
        prompt = f"""Based on this diagnosis, please provide evidence-based treatment recommendations{age_context}.

Diagnosis: {diagnosis}

Please provide:
1. Conservative treatment options (physical therapy, lifestyle changes)
2. Medical interventions if needed
3. When to seek immediate medical attention
4. Expected timeline for improvement
5. Cost and invasiveness considerations

Focus on patient-centered, accessible language and prioritize less invasive options first."""
        
        return self.generate(prompt)


# Convenience functions to match existing OpenAI interface
def call_ollama(prompt: str, model_name: str = "medgemma-assistant") -> str:
    """Simple function to call Ollama model, similar to call_openai interface."""
    client = OllamaClient(model_name)
    return client.generate(prompt)


# Example usage functions
def test_ollama_diagnosis():
    """Test the diagnosis generation with a sample report."""
    from test_reports import JAMES_REPORT
    
    client = OllamaClient()
    diagnosis = client.generate_diagnosis(JAMES_REPORT, age=45)
    print("Ollama Diagnosis:")
    print(diagnosis)
    print("\n" + "="*50 + "\n")
    
    care_plan = client.generate_care_plan(diagnosis, age=45)
    print("Ollama Care Plan:")
    print(care_plan)


if __name__ == "__main__":
    # Test the integration
    test_ollama_diagnosis()