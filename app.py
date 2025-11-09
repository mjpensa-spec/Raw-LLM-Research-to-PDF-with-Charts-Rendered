"""
Flask Web Application for Markdown to PDF Converter
Provides a web interface for uploading markdown files and downloading PDFs
"""
import os
import tempfile
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2

from markdown_fixer import MarkdownFixer
from mermaid_renderer import MermaidRenderer
from pdf_converter import PDFConverter


app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp(prefix='md_uploads_')
app.config['OUTPUT_FOLDER'] = tempfile.mkdtemp(prefix='pdf_outputs_')
app.config['ALLOWED_EXTENSIONS'] = {'md', 'markdown', 'txt', 'pdf'}

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    text_content = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    text_content.append(f"# Page {page_num}\n\n{text}\n")
                    
        return '\n'.join(text_content)
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def cleanup_old_files():
    """Clean up files older than 1 hour"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=1)

        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            for file_path in Path(folder).glob('*'):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_time:
                        file_path.unlink()
    except Exception as e:
        print(f"Error cleaning up old files: {e}")


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle markdown or PDF file upload and process it
    Returns the PDF file directly
    """
    cleanup_old_files()

    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Check if file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a .md, .markdown, or .pdf file'}), 400

    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        upload_filename = f"{unique_id}_{original_filename}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)

        # Save uploaded file
        file.save(upload_path)

        # Determine file type and read content
        file_extension = Path(original_filename).suffix.lower()
        
        if file_extension == '.pdf':
            # Extract text from PDF
            markdown_content = extract_text_from_pdf(upload_path)
        else:
            # Read markdown content
            with open(upload_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

        # Process markdown
        # Step 1: Fix syntax
        fixer = MarkdownFixer(markdown_content)
        fixed_content = fixer.fix_all_issues()
        
        # Step 2: Render mermaid diagrams
        renderer = MermaidRenderer()
        processed_content = renderer.process_markdown(fixed_content)
        
        # Get the temp directory where images are stored
        image_temp_dir = renderer.get_temp_dir()
        print(f"Mermaid images stored in: {image_temp_dir}")

        # Step 3: Remove non-essential code blocks
        processed_content = remove_non_essential_code_blocks(processed_content)

        # Step 4: Convert to PDF
        output_filename = f"{unique_id}_{Path(original_filename).stem}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        converter = PDFConverter()
        success = converter.convert_markdown_to_pdf(
            processed_content, 
            output_path,
            image_base_path=image_temp_dir
        )

        if not success:
            return jsonify({'error': 'Failed to generate PDF'}), 500

        # Return the PDF file
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{Path(original_filename).stem}_processed.pdf"
        )

    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

    finally:
        # Cleanup uploaded file
        try:
            if os.path.exists(upload_path):
                os.remove(upload_path)
        except:
            pass


def remove_non_essential_code_blocks(content: str) -> str:
    """
    Remove code blocks that should have been rendered as visuals
    Keep only code blocks that are actual code examples
    """
    import re

    # Languages that should be kept as code examples
    keep_languages = {'python', 'javascript', 'java', 'c', 'cpp', 'csharp', 
                     'ruby', 'go', 'rust', 'php', 'sql', 'bash', 'shell',
                     'typescript', 'jsx', 'tsx', 'json', 'xml', 'yaml', 'html', 'css',
                     'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'lua'}

    def replacer(match):
        language = match.group(1).strip().lower()
        code_content = match.group(2)

        # Remove if it's empty or just whitespace
        if not code_content.strip():
            return ""

        # Remove if it's explicitly a diagram/chart language
        diagram_keywords = ['mermaid', 'diagram', 'graph', 'flowchart', 'chart', 
                           'gantt', 'sequence', 'class', 'state', 'entity',
                           'pie', 'timeline', 'mindmap', 'gitgraph']
        if any(keyword in language.lower() for keyword in diagram_keywords):
            print(f"Removing code block with language: {language}")
            return ""
        
        # Check if content looks like a diagram even without proper language tag
        content_start = code_content.strip().lower()[:50]
        if any(keyword in content_start for keyword in diagram_keywords):
            print(f"Removing untagged diagram code block")
            return ""

        # Keep if it's a recognized programming language
        if language in keep_languages:
            return match.group(0)

        # If no language specified and doesn't look like a diagram, keep it
        if not language:
            return match.group(0)

        # Default: keep unknown code blocks (might be programming languages we didn't list)
        return match.group(0)

    # Process code blocks with triple backticks
    pattern = r'```(\w*)\n(.*?)```'
    cleaned = re.sub(pattern, replacer, content, flags=re.DOTALL)

    return cleaned


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Markdown to PDF Converter is running'})


if __name__ == '__main__':
    import os

    # Get environment configuration
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    port = int(os.environ.get('PORT', 5000))

    print("=" * 60)
    print("Markdown/PDF to PDF Converter - Web UI")
    print("=" * 60)
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Server starting at: http://0.0.0.0:{port}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Output folder: {app.config['OUTPUT_FOLDER']}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")

    app.run(debug=debug_mode, host='0.0.0.0', port=port)
