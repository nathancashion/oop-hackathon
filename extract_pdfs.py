#!/usr/bin/env python3
"""
Extract text from PDF files and create a combined markdown file.
"""

import pdfplumber
import PyPDF2
from datetime import datetime
import os

def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (better for complex layouts)."""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    except Exception as e:
        print(f"pdfplumber failed for {pdf_path}: {e}")
        return None

def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2 (fallback method)."""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    except Exception as e:
        print(f"PyPDF2 failed for {pdf_path}: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """Try multiple extraction methods."""
    print(f"📄 Extracting text from: {pdf_path}")
    
    # Try pdfplumber first (usually better)
    text = extract_with_pdfplumber(pdf_path)
    
    # Fall back to PyPDF2 if pdfplumber fails
    if not text or len(text.strip()) < 50:
        print(f"  ⚠️  pdfplumber extraction insufficient, trying PyPDF2...")
        text = extract_with_pypdf2(pdf_path)
    
    if text and len(text.strip()) >= 50:
        print(f"  ✅ Extracted {len(text)} characters")
        return text
    else:
        print(f"  ❌ Failed to extract meaningful text")
        return None

def main():
    # PDF files to process
    pdf_files = [
        ("2021-06-20 Cashion Danny MRI Lumbar Spine.pdf", "Cashion Danny MRI Lumbar Spine (2021-06-20)"),
        ("2025-09-11 XR Cx 2-3 View FlexExt.pdf", "XR Cx 2-3 View FlexExt (2025-09-11)"),
        ("2025-09-20 CT Cx without Contrast.pdf", "CT Cx without Contrast (2025-09-20)")
    ]
    
    # Create combined markdown file
    markdown_content = f"""# Medical Reports Extraction

Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This document contains text extracted from 3 medical PDF reports for processing with the Medical AI Assistant.

"""

    extracted_count = 0
    
    for pdf_file, title in pdf_files:
        if not os.path.exists(pdf_file):
            print(f"⚠️  File not found: {pdf_file}")
            continue
        
        text = extract_text_from_pdf(pdf_file)
        
        markdown_content += f"""## Report {extracted_count + 1}: {title}

"""
        
        if text:
            # Clean up the text a bit
            cleaned_text = text.replace('\x00', '').replace('\x0c', '\n\n')  # Remove null chars and form feeds
            markdown_content += f"""```
{cleaned_text}
```

---

"""
            extracted_count += 1
        else:
            markdown_content += """*Could not extract text from this PDF. It may be an image-based PDF requiring OCR.*

---

"""
    
    # Write to file
    output_file = "combined_reports.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n{'='*60}")
    print(f"📝 EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successfully extracted {extracted_count}/{len(pdf_files)} PDF reports")
    print(f"💾 Combined report saved as: {output_file}")
    
    if extracted_count > 0:
        # Show a preview
        print(f"\n📖 Preview of {output_file}:")
        print("-" * 40)
        with open(output_file, 'r') as f:
            preview = f.read()[:500]
            print(preview + "..." if len(preview) >= 500 else preview)

if __name__ == "__main__":
    main()