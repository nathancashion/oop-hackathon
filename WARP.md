# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a medical AI assistant hackathon project that processes radiology reports (specifically MRI lumbar spine reports) and provides:
1. Patient-friendly diagnosis explanations using medical literature context
2. Treatment care plan recommendations based on established guidelines  
3. Age-specific statistics for conditions to provide context
4. Provider-friendly messages to help communicate findings to patients

The system integrates OpenAI GPT-4 and LlamaParse for PDF extraction to create a complete radiology report analysis pipeline.

## Essential Commands

### Setup and Dependencies
```bash
# Install required dependencies (not managed by requirements.txt)
pip install openai llama-parse requests

# Verify Python environment
python3 --version  # Requires Python 3.x

# Test imports
python3 -c "import openai, llama_parse, requests"
```

### Running the Application
```bash
# Run main application pipeline
python3 main.py

# Run individual components
python3 -c "import extract_pdf; print(extract_pdf.sync_extract_report_from_pdf('example.pdf'))"
python3 -c "import stats_finder; print(stats_finder.stat_finder('report_text'))"

# Syntax check all Python files
find . -name "*.py" -exec python3 -m py_compile {} \;
```

### Testing Components
```bash
# Test PDF extraction
python3 -c "import extract_pdf; print(extract_pdf.sync_extract_report_from_pdf('red_flags.pdf'))"

# Test diagnosis with sample report
python3 -c "import test_reports, diagnose_prompt, models; print(models.call_openai(diagnose_prompt.DIAGNOSE_PROMPT.format(context='', report=test_reports.JAMES_REPORT)).choices[0].message.content)"
```

## Code Architecture

### Core Components

**main.py** - Central orchestration module that:
- Coordinates the entire pipeline from diagnosis to care plan to provider messaging
- Contains the main workflow: `summary_diagnosis()` → `care_plan()` → `provider_assist()`
- Provides example usage and testing functions

**models.py** - OpenAI API integration layer:
- Centralized OpenAI client configuration
- Single `call_openai()` function used throughout the system
- Uses GPT-4 model for all text generation tasks

**extract_pdf.py** - PDF processing using LlamaParse:
- Extracts structured text from medical PDF reports
- Supports configurable output formats (markdown, text)
- Handles both file storage and content extraction

### AI Prompt Engineering

**diagnose_prompt.py** - Patient education prompt:
- Uses medical literature context and age-based statistics
- Generates empathetic, layman-friendly explanations of radiology findings
- Includes specific formatting requirements (1000 character limit, markdown output)

**care_plan_prompt.py** - Treatment recommendation prompt:
- References medical guidelines from `acp_guidelines.md`
- Provides treatment options with invasiveness and cost considerations
- Focuses on patient-centered, accessible language

### Data Management

**data.py** - Age-stratified prevalence statistics:
- Contains prevalence data for 8 common spinal conditions across age groups (20s-80s)
- Used to provide context about how common findings are for patient's age

**test_reports.py** - Sample medical reports:
- Contains realistic MRI lumbar spine reports for testing
- Includes patient demographics and detailed imaging findings

**stats_finder.py** - Condition identification and statistics:
- Matches report findings to known conditions in `data.py`
- Extracts age-appropriate prevalence statistics for patient education

### Supporting Files

- **acp_guidelines.md** - Medical treatment guidelines for care plan generation
- **ajnr.md** - Literature context for diagnosis explanations
- **red_flags.md** - Critical findings that require immediate attention

## Configuration Requirements

### API Keys
The application requires two API keys to be configured in:

1. **OpenAI API Key** in `models.py`:
```python
client = OpenAI(api_key="your_openai_key_here")
```

2. **LlamaIndex API Key** in `extract_pdf.py`:
```python
LLM_MODELS['llamaindex']['key'] = "your_llamaindex_key_here"
```

### Input Files
- PDF files for extraction should be placed in the project root
- Medical guideline files (`.md` format) are read directly by the care plan and diagnosis functions

## Development Workflow

1. **Testing Individual Components**: Start with the modular functions in each file before running the full pipeline
2. **PDF Processing**: Use `extract_pdf.py` to convert medical reports to text before processing
3. **Prompt Iteration**: Modify prompt templates in `*_prompt.py` files to adjust AI responses
4. **Statistics Updates**: Update prevalence data in `data.py` as new research becomes available
5. **Report Testing**: Add new test cases to `test_reports.py` for validation

## Key Integration Points

- All AI text generation flows through `models.call_openai()`
- PDF extraction outputs feed directly into diagnosis and care plan prompts
- Statistics from `data.py` are injected into diagnosis prompts for age-appropriate context
- The `main.py` orchestrates the complete patient communication workflow
