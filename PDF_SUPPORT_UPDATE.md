# PDF Support Update

## Summary

The markdown research processor has been updated to accept both **Markdown (.md)** and **PDF (.pdf)** files as input.

## What Changed

### 1. Dependencies (requirements.txt)
- Added **PyPDF2>=3.0** for PDF text extraction

### 2. Web Application (app.py)
- Updated ALLOWED_EXTENSIONS to include 'pdf'
- Added extract_text_from_pdf() function to extract text from PDF files
- Modified upload endpoint to detect file type and handle PDFs differently
- Updated error messages to mention both file types
- Changed application title to "Markdown/PDF to PDF Converter"

### 3. CLI Tool (main.py)
- Added extract_text_from_pdf() method to MarkdownProcessor class
- Updated process_file() to detect and handle PDF files
- Updated process_directory() to find and process both .md and .pdf files
- Updated help text and examples to mention PDF support

### 4. Web Interface (templates/index.html)
- Updated file input to accept .pdf files
- Changed title from "Markdown to PDF Converter" to "Markdown/PDF to PDF Converter"
- Updated subtitle and labels to mention PDF files
- Added note in footer about PDF processing

## How It Works

### For PDF Input Files:
1. **Text Extraction**: When a PDF is uploaded, the program uses PyPDF2 to extract text from all pages
2. **Markdown Formatting**: Extracted text is formatted as markdown with page headers (# Page 1, # Page 2, etc.)
3. **Processing Pipeline**: The extracted text goes through the same processing pipeline as markdown files:
   - Markdown syntax fixing
   - Mermaid diagram rendering
   - Code block cleanup
   - PDF generation

### For Markdown Input Files:
- Processing remains unchanged - same as before

## Usage Examples

### Web Interface
1. Navigate to the web application
2. Click "Choose a markdown or PDF file" 
3. Select either a .md or .pdf file
4. Click "Convert to PDF"
5. Download the processed PDF

### Command Line

`powershell
# Process a markdown file
python main.py research_output.md

# Process a PDF file
python main.py document.pdf

# Process a PDF with custom output name
python main.py document.pdf -o processed_document.pdf

# Process all markdown and PDF files in a directory
python main.py -d ./research_outputs

# Verbose mode to see processing details
python main.py document.pdf -v
`

## Installation

To use the updated program, install the new dependency:

`powershell
pip install PyPDF2>=3.0
`

Or install all dependencies:

`powershell
pip install -r requirements.txt
`

## Notes

- PDF files are extracted as plain text, so complex formatting, images, and tables in the original PDF may not be preserved
- The extracted text is treated as markdown and processed through the same pipeline
- Maximum file size remains 16MB for both markdown and PDF files
- Backup files were created: app.py.backup, main.py.backup, index.html.backup

## File Changes

-  equirements.txt - Added PyPDF2 dependency
-  pp.py - Added PDF extraction and handling
-  main.py - Added PDF extraction and handling  
-  	emplates/index.html - Updated UI for PDF support

