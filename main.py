"""
Main CLI Application
Processes markdown files with LLM research outputs and converts to PDF
"""
import os
import sys
import argparse
from pathlib import Path
from typing import Optional
import PyPDF2

from markdown_fixer import MarkdownFixer
from mermaid_renderer import MermaidRenderer
from pdf_converter import PDFConverter


class MarkdownProcessor:
    """Main processor for markdown files"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.fixer = None
        self.renderer = MermaidRenderer()
        self.converter = PDFConverter()

    def log(self, message: str):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(f"[INFO] {message}")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string formatted as markdown
        """
        text_content = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                self.log(f"Extracting text from {len(pdf_reader.pages)} pages")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"# Page {page_num}\n\n{text}\n")
                        
            return '\n'.join(text_content)
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def process_file(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """
        Process a single markdown or PDF file

        Args:
            input_file: Path to input markdown or PDF file
            output_file: Path to output PDF (optional, defaults to same name with .pdf)

        Returns:
            True if successful, False otherwise
        """
        self.log(f"Processing file: {input_file}")

        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            return False

        # Determine file type
        file_extension = Path(input_file).suffix.lower()
        
        # Read input file
        try:
            if file_extension == '.pdf':
                self.log("Detected PDF file - extracting text...")
                original_content = self.extract_text_from_pdf(input_file)
                self.log(f"Extracted {len(original_content)} characters from PDF")
            else:
                self.log("Detected markdown file - reading content...")
                with open(input_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                self.log(f"Read {len(original_content)} characters from input file")
        except Exception as e:
            print(f"Error reading input file: {e}")
            return False

        # Step 1: Fix markdown syntax issues
        self.log("Step 1: Fixing markdown syntax...")
        self.fixer = MarkdownFixer(original_content)
        fixed_content = self.fixer.fix_all_issues()

        mermaid_blocks = self.fixer.detect_mermaid_blocks()
        self.log(f"Found {len(mermaid_blocks)} mermaid blocks")

        # Step 2: Render mermaid diagrams to images
        self.log("Step 2: Rendering mermaid diagrams...")
        processed_content = self.renderer.process_markdown(fixed_content)

        # Step 3: Remove any remaining code blocks that should be visual
        self.log("Step 3: Cleaning up remaining code blocks...")
        processed_content = self.remove_non_essential_code_blocks(processed_content)

        # Determine output path
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.pdf'))

        self.log(f"Output will be saved to: {output_file}")

        # Step 4: Convert to PDF
        self.log("Step 4: Converting to PDF...")
        success = self.converter.convert_markdown_to_pdf(processed_content, output_file)

        if success:
            self.log(f"Successfully created PDF: {output_file}")
            print(f" PDF created: {output_file}")
            return True
        else:
            print(f" Failed to create PDF")
            return False

    def remove_non_essential_code_blocks(self, content: str) -> str:
        """
        Remove code blocks that should have been rendered as visuals
        Keep only code blocks that are actual code examples (not mermaid, not diagrams)
        """
        import re

        # Languages that should be kept as code examples
        keep_languages = {'python', 'javascript', 'java', 'c', 'cpp', 'csharp',
                         'ruby', 'go', 'rust', 'php', 'sql', 'bash', 'shell',
                         'typescript', 'jsx', 'tsx', 'json', 'xml', 'yaml', 'html', 'css'}

        def replacer(match):
            language = match.group(1).strip().lower()
            code_content = match.group(2)

            # Keep if it's a recognized programming language
            if language in keep_languages:
                return match.group(0)

            # Remove if it's empty or just whitespace
            if not code_content.strip():
                return ""

            # Remove if it looks like a diagram language
            diagram_keywords = ['mermaid', 'diagram', 'graph', 'flowchart', 'chart']
            if any(keyword in language for keyword in diagram_keywords):
                return ""

            # If no language specified, keep it as it might be important
            if not language:
                return match.group(0)

            return match.group(0)

        # Process code blocks
        pattern = r'`(\w*)\n(.*?)`'
        cleaned = re.sub(pattern, replacer, content, flags=re.DOTALL)

        return cleaned

    def process_directory(self, input_dir: str, output_dir: Optional[str] = None) -> bool:
        """
        Process all markdown and PDF files in a directory

        Args:
            input_dir: Directory containing markdown or PDF files
            output_dir: Directory for output PDFs (optional)

        Returns:
            True if all files processed successfully
        """
        if not os.path.isdir(input_dir):
            print(f"Error: Input directory not found: {input_dir}")
            return False

        # Find all markdown and PDF files
        md_files = list(Path(input_dir).glob('*.md'))
        pdf_files = list(Path(input_dir).glob('*.pdf'))
        all_files = md_files + pdf_files

        if not all_files:
            print(f"No markdown or PDF files found in: {input_dir}")
            return False

        print(f"Found {len(md_files)} markdown file(s) and {len(pdf_files)} PDF file(s) to process")

        success_count = 0
        for file_path in all_files:
            # Determine output path
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, file_path.stem + '_processed.pdf')
            else:
                output_file = str(file_path.with_suffix('')) + '_processed.pdf'

            # Process file
            if self.process_file(str(file_path), output_file):
                success_count += 1

        print(f"\nProcessed {success_count}/{len(all_files)} files successfully")
        return success_count == len(all_files)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Process markdown or PDF files with LLM research outputs and convert to PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single markdown file
  python main.py research_output.md

  # Process a PDF file (extracts text and re-processes)
  python main.py document.pdf

  # Process a single file with custom output name
  python main.py research_output.md -o final_report.pdf

  # Process all markdown and PDF files in a directory
  python main.py -d ./research_outputs

  # Process directory with custom output directory
  python main.py -d ./research_outputs -o ./pdfs

  # Verbose mode for debugging
  python main.py research_output.md -v
        """
    )

    parser.add_argument('input', nargs='?', help='Input markdown or PDF file to process')
    parser.add_argument('-d', '--directory', help='Process all markdown and PDF files in directory')
    parser.add_argument('-o', '--output', help='Output PDF file or directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Validate arguments
    if not args.input and not args.directory:
        parser.print_help()
        print("\nError: Please specify either an input file or a directory with -d")
        sys.exit(1)

    if args.input and args.directory:
        print("Error: Cannot specify both input file and directory")
        sys.exit(1)

    # Create processor
    processor = MarkdownProcessor(verbose=args.verbose)

    # Process files
    try:
        if args.directory:
            success = processor.process_directory(args.directory, args.output)
        else:
            success = processor.process_file(args.input, args.output)

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
