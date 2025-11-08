# Ollama MedGemma Integration

This document explains how to use the local MedGemma model with Ollama as an alternative to OpenAI for your medical AI assistant project.

## Setup Complete ✅

The following components have been set up:

1. **Model Downloaded**: `alibayram/medgemma:latest` - A medical-focused variant of Google's Gemma model
2. **Custom Modelfile**: `Modelfile` - Configures the model with medical-specific prompts and parameters
3. **Custom Model Created**: `medgemma-assistant` - Your personalized medical AI assistant model
4. **Integration Module**: `ollama_models.py` - Python interface for using the Ollama model
5. **Enhanced Main**: `main_ollama.py` - Updated pipeline that can use either Ollama or OpenAI

## Quick Start

### Using the Custom Model Directly
```bash
# Test the model with a simple question
ollama run medgemma-assistant "What is disc degeneration?"

# Interactive mode
ollama run medgemma-assistant
```

### Using the Python Integration
```python
# Test the Ollama integration
python3 ollama_models.py

# Run the full pipeline with Ollama
python3 main_ollama.py
```

## Configuration

### Switching Between Models
In `main_ollama.py`, change the `USE_OLLAMA` variable:

```python
USE_OLLAMA = True   # Use local Ollama model
USE_OLLAMA = False  # Use OpenAI GPT-4
```

### Model Parameters
The Modelfile configures these parameters for medical use:
- **Temperature**: 0.3 (conservative, factual responses)
- **Top P**: 0.9 (focused but not overly restrictive)
- **Context Length**: 4096 tokens
- **Max Output**: 1024 tokens

## Key Features

### Medical-Specific System Prompt
The model is configured with a specialized system prompt for:
- Patient education and empathetic communication
- Radiology report analysis (especially MRI lumbar spine)
- Evidence-based treatment recommendations
- Age-appropriate statistics and context

### Structured Functions
- `generate_diagnosis()` - Patient-friendly explanations
- `generate_care_plan()` - Treatment recommendations
- `provider_assist()` - Provider communication assistance

## Advantages of Local Ollama

✅ **Privacy**: All processing happens locally  
✅ **Cost**: No API fees after initial setup  
✅ **Speed**: No network latency for requests  
✅ **Availability**: Works offline  
✅ **Customization**: Full control over model behavior  

## Available Models

```bash
ollama list
```

Current models:
- `medgemma-assistant:latest` - Your custom medical assistant
- `alibayram/medgemma:latest` - Base medical model
- Other models (llama3.1, llama3.2, etc.)

## Usage Examples

### Direct Medical Query
```bash
ollama run medgemma-assistant "Explain L4-L5 disc degeneration to a 45-year-old patient"
```

### Python Integration
```python
from ollama_models import OllamaClient

client = OllamaClient()
diagnosis = client.generate_diagnosis(report_text, context="", age=45)
care_plan = client.generate_care_plan(diagnosis, age=45)
```

### Full Pipeline Comparison
```python
# In main_ollama.py
results = test_both_models()  # Compare Ollama vs OpenAI outputs
```

## Performance Notes

- **First Request**: May take 10-15 seconds as model loads into memory
- **Subsequent Requests**: Much faster (2-5 seconds)
- **Memory Usage**: ~2.5GB RAM when model is loaded
- **Model stays loaded**: For ~5 minutes after last request

## Troubleshooting

### Model Not Responding
```bash
# Check if Ollama is running
ollama ps

# Restart Ollama service if needed
# On macOS, restart the Ollama app
```

### Memory Issues
```bash
# Check available RAM
# The model requires ~2.5GB to run effectively
```

### Python Import Errors
```bash
# Make sure you're in the right directory
cd /Users/nately/Development/oop-hackathon

# Check Python path
python3 -c "import ollama_models; print('✅ Import successful')"
```

## File Structure

```
oop-hackathon/
├── Modelfile                 # Ollama model configuration
├── ollama_models.py          # Python integration
├── main_ollama.py           # Enhanced main with Ollama support
├── README_OLLAMA.md         # This documentation
└── [existing files]         # Your original project files
```

## Next Steps

1. **Test the Integration**: Run `python3 main_ollama.py` to see it in action
2. **Compare Models**: Use `test_both_models()` to compare Ollama vs OpenAI
3. **Customize Prompts**: Modify the system prompt in `Modelfile` if needed
4. **Optimize Parameters**: Adjust temperature, top_p, etc. based on your needs

## Model Management

```bash
# Remove the custom model if needed
ollama rm medgemma-assistant

# Recreate with updated Modelfile
ollama create medgemma-assistant -f Modelfile

# Pull updates to base model
ollama pull alibayram/medgemma:latest
```

---

🏥 **Your medical AI assistant is now ready to run locally with enhanced privacy and control!**