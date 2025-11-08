#!/usr/bin/env python3
"""
Process the extracted medical reports through the Medical AI Assistant
"""

import re
import models_ollama as models
import diagnose_prompt
import care_plan_prompt
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

def extract_reports_from_markdown(filename="combined_reports.md"):
    """Extract individual reports from the combined markdown file."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by report headers
    reports = []
    report_sections = re.split(r'^## Report \d+: (.+)$', content, flags=re.MULTILINE)
    
    # Skip the header section and process pairs of (title, content)
    for i in range(1, len(report_sections), 2):
        if i + 1 < len(report_sections):
            title = report_sections[i].strip()
            content_raw = report_sections[i + 1].strip()
            
            # Extract content between triple backticks
            code_match = re.search(r'```\n(.*?)\n```', content_raw, re.DOTALL)
            if code_match:
                report_text = code_match.group(1).strip()
                reports.append({
                    'title': title,
                    'text': report_text
                })
    
    return reports

def process_single_report(report_data):
    """Process a single report through the medical AI pipeline."""
    title = report_data['title']
    report_text = report_data['text']
    
    print(f"\n{'='*80}")
    print(f"🏥 PROCESSING: {title}")
    print(f"{'='*80}")
    print(f"📝 Report length: {len(report_text)} characters")
    
    # Extract patient info for context
    age_match = re.search(r'Age\s+Sex\n.*?\s+(\d+)\s+(Male|Female)', report_text)
    if not age_match:
        age_match = re.search(r'Date of Birth.*?(\d{4})', report_text)
        if age_match:
            birth_year = int(age_match.group(1))
            current_year = 2025  # Based on report dates
            age = current_year - birth_year
            gender = "Unknown"
        else:
            age = "Unknown"
            gender = "Unknown"
    else:
        age = age_match.group(1)
        gender = age_match.group(2)
    
    print(f"👤 Patient: Age {age}, {gender}")
    print()
    
    try:
        # Generate analysis components
        print("📋 Generating evidence-based care plan...")
        with open('acp_guidelines.md', 'r') as f:
            context = f.read()
        care_plan = models.call_openai(
            care_plan_prompt.CARE_PLAN_PROMPT.format(context=context, report=report_text)
        ).choices[0].message.content
        
        print("🏥 Generating patient-friendly diagnosis summary...")
        with open('ajnr.md', 'r') as f:
            context = f.read()
        diagnosis = models.call_openai(
            diagnose_prompt.DIAGNOSE_PROMPT.format(context=context, report=report_text)
        ).choices[0].message.content
        
        print("📊 Finding age-relevant statistics...")
        stats = stats_finder.stat_finder(report_text)
        
        print("🤖 Generating provider communication message...")
        provider_message = models.call_openai(
            PROVIDER_ASSISTANT_PROMPT.format(diagnosis=diagnosis, care_plan=care_plan)
        ).choices[0].message.content
        
        return {
            'title': title,
            'care_plan': care_plan,
            'diagnosis': diagnosis,
            'stats': stats,
            'provider_message': provider_message
        }
        
    except Exception as e:
        print(f"❌ Error processing {title}: {e}")
        return None

def display_results(results):
    """Display the analysis results."""
    for i, result in enumerate(results, 1):
        if result is None:
            continue
            
        print(f"\n{'#'*100}")
        print(f"# ANALYSIS RESULTS #{i}: {result['title']}")
        print(f"{'#'*100}")
        
        print(f"\n{'='*60}")
        print("📋 CARE PLAN")
        print(f"{'='*60}")
        print(result['care_plan'])
        
        print(f"\n{'='*60}")
        print("🏥 PATIENT-FRIENDLY DIAGNOSIS")
        print(f"{'='*60}")
        print(result['diagnosis'])
        
        print(f"\n{'='*60}")
        print("📊 AGE-RELEVANT STATISTICS")
        print(f"{'='*60}")
        print(result['stats'])
        
        print(f"\n{'='*60}")
        print("💌 PROVIDER COMMUNICATION MESSAGE")
        print(f"{'='*60}")
        print(result['provider_message'])

def save_results_to_file(results):
    """Save results to a comprehensive analysis file."""
    with open('comprehensive_analysis.md', 'w') as f:
        f.write("# Comprehensive Medical AI Analysis\n\n")
        f.write(f"Generated using Llama 3.1 8B model\n\n")
        
        for i, result in enumerate(results, 1):
            if result is None:
                continue
                
            f.write(f"## Report {i}: {result['title']}\n\n")
            
            f.write("### Care Plan\n")
            f.write(result['care_plan'])
            f.write("\n\n")
            
            f.write("### Patient-Friendly Diagnosis\n")
            f.write(result['diagnosis'])
            f.write("\n\n")
            
            f.write("### Age-Relevant Statistics\n")
            f.write(result['stats'])
            f.write("\n\n")
            
            f.write("### Provider Communication Message\n")
            f.write(result['provider_message'])
            f.write("\n\n---\n\n")

def main():
    print("🏥 MEDICAL AI ASSISTANT - PROCESSING EXTRACTED REPORTS")
    print("=" * 60)
    print(f"🤖 Using model: {models.DEFAULT_MODEL}")
    print()
    
    # Extract reports from the combined markdown file
    print("📄 Loading extracted reports...")
    reports = extract_reports_from_markdown()
    
    print(f"✅ Found {len(reports)} reports to process:")
    for i, report in enumerate(reports, 1):
        print(f"  {i}. {report['title']}")
    print()
    
    # Process each report
    results = []
    for report in reports:
        result = process_single_report(report)
        results.append(result)
    
    # Display results
    print(f"\n{'='*80}")
    print("📊 PROCESSING COMPLETE - DISPLAYING RESULTS")
    print(f"{'='*80}")
    
    display_results(results)
    
    # Save to file
    save_results_to_file(results)
    
    successful_analyses = len([r for r in results if r is not None])
    print(f"\n{'='*80}")
    print("✅ ANALYSIS COMPLETE!")
    print(f"{'='*80}")
    print(f"📊 Successfully analyzed {successful_analyses}/{len(reports)} reports")
    print(f"💾 Comprehensive analysis saved to: comprehensive_analysis.md")

if __name__ == "__main__":
    main()