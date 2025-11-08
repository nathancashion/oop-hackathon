"""
Enhanced main module with support for both OpenAI and local Ollama models.
This version allows you to choose between cloud-based OpenAI and local medgemma-assistant.
"""

import extract_pdf
import models
import ollama_models  # Our new Ollama integration
import diagnose_prompt
import care_plan_prompt
import test_reports
import stats_finder
from typing import Optional

# Configuration: Set to True to use Ollama, False to use OpenAI
USE_OLLAMA = True  # Change this to switch between models

PROVIDER_ASSISTANT_PROMPT = """
Use the following information to help a provider write a portal message to a patient that helps them understand a recent radiology report and what options are available for care.

# Diagnosis
{diagnosis}

# Care Plan
{care_plan}

Instructions:
- Please be empathetic and friendly in your disposition and explain things in simple terminology.
- The goal of this message is to alleviate concerns, explain findings and set up the discussion in the follow-up visit so that the provider and patient can use shared decision to determine the next steps in treatment.
"""

def get_ai_response(prompt: str) -> str:
    """
    Get AI response using either Ollama or OpenAI based on configuration.
    
    Args:
        prompt: The prompt to send to the AI model
        
    Returns:
        AI response text
    """
    if USE_OLLAMA:
        return ollama_models.call_ollama(prompt)
    else:
        return models.call_openai(prompt).choices[0].message.content

def provider_assist(care_plan: str, diagnosis: str) -> str:
    """Generate provider assistance message."""
    prompt = PROVIDER_ASSISTANT_PROMPT.format(diagnosis=diagnosis, care_plan=care_plan)
    return get_ai_response(prompt)

def care_plan(report: str = test_reports.JAMES_REPORT) -> str:
    """Generate care plan recommendations."""
    if USE_OLLAMA:
        # Use Ollama's specialized care plan function
        client = ollama_models.OllamaClient()
        # First get a diagnosis to inform the care plan
        with open('ajnr.md', 'r') as f:
            context = f.read()
        diagnosis = client.generate_diagnosis(report, context)
        return client.generate_care_plan(diagnosis)
    else:
        # Use original OpenAI approach
        with open('acp_guidelines.md', 'r') as out_file:
            context = out_file.read()
        return models.call_openai(care_plan_prompt.CARE_PLAN_PROMPT.format(context=context, report=report)).choices[0].message.content

def summary_diagnosis(report: str = test_reports.JAMES_REPORT) -> str:
    """Generate patient-friendly diagnosis summary."""
    if USE_OLLAMA:
        # Use Ollama's specialized diagnosis function
        client = ollama_models.OllamaClient()
        with open('ajnr.md', 'r') as f:
            context = f.read()
        return client.generate_diagnosis(report, context)
    else:
        # Use original OpenAI approach
        with open('ajnr.md', 'r') as out_file:
            context = out_file.read()
        return models.call_openai(diagnose_prompt.DIAGNOSE_PROMPT.format(context=context, report=report)).choices[0].message.content

def summary_age(report: str = test_reports.JAMES_REPORT) -> str:
    """Get age-specific statistics for conditions found in report."""
    return stats_finder.stat_finder(report=report)

def fetch_patient_age() -> int:
    """Fetch patient age (currently returns mock data)."""
    return 65

def summary(diagnosis_summary: str, stats_diagnosis_age: str) -> str:
    """Combine diagnosis and age statistics."""
    return f"{diagnosis_summary} \n\n\n\n {stats_diagnosis_age}"

def run_full_pipeline(report: str = test_reports.JAMES_REPORT, patient_age: Optional[int] = None) -> dict:
    """
    Run the complete medical AI assistant pipeline.
    
    Args:
        report: The radiology report text
        patient_age: Optional patient age for age-specific recommendations
        
    Returns:
        Dictionary containing all generated content
    """
    print("🏥 Starting Medical AI Assistant Pipeline...")
    print(f"📊 Using {'Ollama (local medgemma-assistant)' if USE_OLLAMA else 'OpenAI GPT-4'}")
    
    # Generate diagnosis
    print("🔍 Generating patient-friendly diagnosis...")
    if USE_OLLAMA and patient_age:
        client = ollama_models.OllamaClient()
        with open('ajnr.md', 'r') as f:
            context = f.read()
        diagnosis = client.generate_diagnosis(report, context, age=patient_age)
    else:
        diagnosis = summary_diagnosis(report)
    
    # Generate care plan
    print("📋 Generating care plan recommendations...")
    if USE_OLLAMA and patient_age:
        client = ollama_models.OllamaClient()
        care = client.generate_care_plan(diagnosis, age=patient_age)
    else:
        care = care_plan(report)
    
    # Generate provider message
    print("👨‍⚕️ Generating provider assistance message...")
    provider_response = provider_assist(care, diagnosis)
    
    # Get age statistics
    print("📈 Fetching age-specific statistics...")
    age_stats = summary_age(report)
    
    results = {
        'diagnosis': diagnosis,
        'care_plan': care,
        'provider_message': provider_response,
        'age_statistics': age_stats,
        'model_used': 'Ollama (medgemma-assistant)' if USE_OLLAMA else 'OpenAI GPT-4'
    }
    
    print("✅ Pipeline complete!")
    return results

def main():
    """Main execution function."""
    print("🚀 Medical AI Assistant - Enhanced Version")
    print("=" * 50)
    
    # You can specify a patient age here for more personalized results
    patient_age = 45  # Change this or set to None
    
    # Run the full pipeline
    results = run_full_pipeline(test_reports.JAMES_REPORT, patient_age)
    
    # Display results
    print("\n📋 CARE PLAN")
    print("=" * 50)
    print(results['care_plan'])
    
    print("\n🔍 DIAGNOSIS EXPLANATION")
    print("=" * 50)
    print(results['diagnosis'])
    
    print("\n👨‍⚕️ PROVIDER MESSAGE")
    print("=" * 50)
    print(results['provider_message'])
    
    print("\n📈 AGE STATISTICS")
    print("=" * 50)
    print(results['age_statistics'])
    
    print(f"\n🤖 Model Used: {results['model_used']}")

def test_both_models():
    """Compare outputs from both Ollama and OpenAI models."""
    print("🔄 Comparing Ollama vs OpenAI outputs...")
    
    # Test with Ollama
    global USE_OLLAMA
    USE_OLLAMA = True
    print("\n🤖 OLLAMA RESULTS:")
    print("-" * 30)
    ollama_results = run_full_pipeline(test_reports.JAMES_REPORT)
    
    # Test with OpenAI
    USE_OLLAMA = False
    print("\n🌐 OPENAI RESULTS:")
    print("-" * 30)
    openai_results = run_full_pipeline(test_reports.JAMES_REPORT)
    
    print("\n📊 COMPARISON COMPLETE")
    return {
        'ollama': ollama_results,
        'openai': openai_results
    }

if __name__ == "__main__":
    main()
    
    # Optionally extract PDF and process it
    try:
        print("\n📄 Processing PDF...")
        response = extract_pdf.sync_extract_report_from_pdf('red_flags.pdf')
        extract_pdf.store_extracted_info(response, 'red_flags.md')
        print("✅ PDF processing complete!")
    except Exception as e:
        print(f"⚠️ PDF processing failed: {e}")

import models_ollama as models  # Use Ollama instead of OpenAI
import diagnose_prompt
import care_plan_prompt
import test_reports
import stats_finder_ollama as stats_finder

PROVIDER_ASSISTANT_PROMPT = """
Use the following information to help a provider write a portal message to a patient that helps them understand a recent radiology report and what options are available for care.

# Diagnosis
{diagnosis}

# Care Plan
{care_plan}

Instructions:
- Please be empathetic and friendly in your disposition and explain things in simple terminology.
- The goal of this message is to alleviate concerns, explain findings and set up the discussion in the follow-up visit so that the provider and patient can use shared decision to determine the next steps in treatment.
"""

def provider_assist(care_plan, diagnosis):
    print("🤖 Generating provider communication message...")
    return models.call_openai(PROVIDER_ASSISTANT_PROMPT.format(diagnosis=diagnosis, care_plan=care_plan)).choices[0].message.content

def care_plan(report=test_reports.JAMES_REPORT):
    print("📋 Generating evidence-based care plan...")
    with open('acp_guidelines.md', 'r') as out_file:
        context = out_file.read()
    return models.call_openai(care_plan_prompt.CARE_PLAN_PROMPT.format(context=context, report=report)).choices[0].message.content

def summary_diagnosis(report=test_reports.JAMES_REPORT):
    print("🏥 Generating patient-friendly diagnosis summary...")
    with open('ajnr.md', 'r') as out_file:
        context = out_file.read()
    return models.call_openai(diagnose_prompt.DIAGNOSE_PROMPT.format(context=context, report=report)).choices[0].message.content

def summary_age(report=test_reports.JAMES_REPORT):
    print("📊 Finding age-relevant statistics...")
    return stats_finder.stat_finder(report=report)

def summary(diagnosis_summary, stats_diagnosis_age):
    return f"{diagnosis_summary} \n\n\n\n {stats_diagnosis_age}"

def fetch_patient_age():
    return 65

def main(): 
    print("🏥 MEDICAL AI ASSISTANT DEMO")
    print("===========================")
    print()
    print("🔧 Using Ollama (Local AI Models)")
    print(f"📊 Available models: {', '.join(models.list_available_models())}")
    print(f"🤖 Using model: {models.DEFAULT_MODEL}")
    print()
    
    print("Processing MRI report for patient (57 years old):")
    print("-" * 50)
    print(test_reports.JAMES_REPORT[:200] + "...")
    print("-" * 50)
    print()
    
    try:
        # Generate each component
        care = care_plan()
        diagnosis = summary_diagnosis()
        stats = summary_age()
        response = provider_assist(care, diagnosis)
        
        print("\n" + "=" * 60)
        print("📋 CARE PLAN")
        print("=" * 60)
        print(care)
        
        print("\n" + "=" * 60)
        print("🏥 PATIENT-FRIENDLY DIAGNOSIS")
        print("=" * 60)
        print(diagnosis)
        
        print("\n" + "=" * 60)
        print("📊 AGE-RELEVANT STATISTICS")
        print("=" * 60)
        print(stats)
        
        print("\n" + "=" * 60)
        print("💌 PROVIDER COMMUNICATION MESSAGE")
        print("=" * 60)
        print(response)
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETE!")
        print("=" * 60)
        print("🎉 Successfully processed radiology report using local AI models!")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        print("Make sure Ollama is running and the selected model is available.")

# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main()