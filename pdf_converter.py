"""
PDF Converter Module
Converts processed markdown to PDF with all visuals rendered
"""
import os
import markdown
from pathlib import Path
from typing import Optional


class PDFConverter:
    """Converts markdown to PDF with rendered visuals"""
    
    def __init__(self):
        self.md_processor = markdown.Markdown(
            extensions=[
                'extra',
                'codehilite',
                'tables',
                'fenced_code',
                'toc'
            ]
        )
    
    def markdown_to_html(self, markdown_content: str, image_base_path: Optional[str] = None) -> str:
        """Convert markdown to HTML with embedded images"""
        import re
        import base64
        
        # Debug: Check if there are still mermaid blocks
        mermaid_blocks = re.findall(r'```mermaid.*?```', markdown_content, re.DOTALL)
        if mermaid_blocks:
            print(f"⚠️ WARNING: Found {len(mermaid_blocks)} unprocessed mermaid blocks in markdown!")
            for i, block in enumerate(mermaid_blocks[:2], 1):  # Show first 2
                print(f"  Block {i}: {block[:100]}...")
        
        # Check for image references
        image_refs = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', markdown_content)
        print(f"Found {len(image_refs)} image references in markdown")
        
        # Convert images to base64 data URIs if image_base_path is provided
        if image_base_path:
            def replace_image(match):
                alt_text = match.group(1)
                img_path = match.group(2)
                
                # If it's already a data URI or absolute URL, leave it
                if img_path.startswith(('data:', 'http://', 'https://')):
                    return match.group(0)
                
                # Construct full path
                if not os.path.isabs(img_path):
                    full_path = os.path.join(image_base_path, img_path)
                else:
                    full_path = img_path
                
                # Convert to base64 data URI
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'rb') as img_file:
                            img_data = base64.b64encode(img_file.read()).decode('utf-8')
                            print(f"✓ Embedded image: {os.path.basename(img_path)}")
                            return f'![{alt_text}](data:image/png;base64,{img_data})'
                    except Exception as e:
                        print(f"✗ Failed to embed {img_path}: {e}")
                else:
                    print(f"✗ Image not found: {full_path}")
                
                return match.group(0)
            
            markdown_content = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', replace_image, markdown_content)
        
        # Reset the processor to clear any previous state
        self.md_processor.reset()
        html_body = self.md_processor.convert(markdown_content)
        
        # Wrap in complete HTML document with styling
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        h1 {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }}
        h2 {{
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 0.3em;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            page-break-inside: avoid;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        table, th, td {{
            border: 1px solid #ddd;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""
        return html
    
    def html_to_pdf(self, html_content: str, output_path: str, base_url: Optional[str] = None) -> bool:
        """Convert HTML to PDF using WeasyPrint"""
        try:
            from weasyprint import HTML, CSS
            
            # Use provided base_url or default to output directory
            if base_url is None:
                base_url = f"file:///{os.path.dirname(os.path.abspath(output_path)).replace(os.sep, '/')}/"
            
            print(f"Converting HTML to PDF with base_url: {base_url}")
            
            # Create PDF
            html_obj = HTML(string=html_content, base_url=base_url)
            html_obj.write_pdf(output_path)
            
            return True
        except ImportError:
            print("Error: WeasyPrint not installed. Install with: pip install weasyprint")
            print("Note: WeasyPrint requires GTK3 on Windows. See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows")
            return False
        except Exception as e:
            print(f"Error converting HTML to PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def convert_markdown_to_pdf(self, markdown_content: str, output_path: str, image_base_path: Optional[str] = None) -> bool:
        """
        Convert markdown content directly to PDF
        
        Args:
            markdown_content: The markdown text to convert
            output_path: Path where PDF should be saved
            image_base_path: Base path for resolving image references
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print("Converting Markdown to PDF")
        print(f"{'='*60}")
        print(f"Image base path: {image_base_path}")
        print(f"Output path: {output_path}")
        
        # Convert markdown to HTML with embedded images
        html_content = self.markdown_to_html(markdown_content, image_base_path)
        
        # Set base_url for image resolution (fallback if embedding fails)
        base_url = None
        if image_base_path:
            # Convert to file:// URL format
            base_url = f"file:///{os.path.abspath(image_base_path).replace(os.sep, '/')}/"
        
        # Convert HTML to PDF
        return self.html_to_pdf(html_content, output_path, base_url=base_url)
    
    def convert_file_to_pdf(self, markdown_file: str, output_path: Optional[str] = None) -> bool:
        """
        Convert a markdown file to PDF
        
        Args:
            markdown_file: Path to input markdown file
            output_path: Path for output PDF (defaults to same name with .pdf extension)
            
        Returns:
            True if successful, False otherwise
        """
        # Read markdown file
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except Exception as e:
            print(f"Error reading markdown file: {e}")
            return False
        
        # Determine output path
        if output_path is None:
            output_path = str(Path(markdown_file).with_suffix('.pdf'))
        
        # Convert to PDF
        return self.convert_markdown_to_pdf(markdown_content, output_path)
