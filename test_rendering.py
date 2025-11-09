"""
Test script to verify mermaid diagram rendering works correctly
"""
import os
import sys
from pathlib import Path

# Test content with mermaid diagrams
TEST_CONTENT = """
# Test Document

This document tests mermaid diagram rendering.

## Test 1: Simple Flowchart

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

## Test 2: Sequence Diagram

```mermaid
sequenceDiagram
    Alice->>John: Hello John
    John-->>Alice: Hi Alice
```

## Test 3: Code Block (Should NOT be removed)

```python
def hello():
    print("This should stay in the PDF")
```

## Test 4: Untagged Mermaid (Should still be rendered)

```
graph LR
    X[Input] --> Y[Output]
```
"""


def test_markdown_processing():
    """Test the complete markdown to PDF pipeline"""
    print("=" * 60)
    print("Testing Markdown to PDF Conversion")
    print("=" * 60)
    
    # Import modules
    try:
        from markdown_fixer import MarkdownFixer
        from mermaid_renderer import MermaidRenderer
        from pdf_converter import PDFConverter
        print("✓ All modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import modules: {e}")
        return False
    
    # Step 1: Fix markdown
    print("\n1. Fixing markdown syntax...")
    try:
        fixer = MarkdownFixer(TEST_CONTENT)
        fixed_content = fixer.fix_all_issues()
        print(f"✓ Markdown fixed ({len(fixed_content)} characters)")
    except Exception as e:
        print(f"✗ Failed to fix markdown: {e}")
        return False
    
    # Step 2: Render mermaid diagrams
    print("\n2. Rendering mermaid diagrams...")
    try:
        renderer = MermaidRenderer()
        processed_content = renderer.process_markdown(fixed_content)
        temp_dir = renderer.get_temp_dir()
        print(f"✓ Mermaid diagrams processed")
        print(f"  Temp directory: {temp_dir}")
        
        # Check how many images were created
        if os.path.exists(temp_dir):
            images = list(Path(temp_dir).glob("*.png"))
            print(f"  Images created: {len(images)}")
            for img in images:
                print(f"    - {img.name} ({img.stat().st_size} bytes)")
        else:
            print(f"  Warning: Temp directory not found")
    except Exception as e:
        print(f"✗ Failed to render mermaid: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Convert to PDF
    print("\n3. Converting to PDF...")
    try:
        output_path = "test_output.pdf"
        converter = PDFConverter()
        success = converter.convert_markdown_to_pdf(
            processed_content, 
            output_path,
            image_base_path=temp_dir
        )
        
        if success and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ PDF created successfully")
            print(f"  Output: {output_path}")
            print(f"  Size: {file_size:,} bytes")
        else:
            print(f"✗ PDF creation failed")
            return False
    except Exception as e:
        print(f"✗ Failed to convert to PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Check if mermaid code blocks are in the final content
    print("\n4. Checking processed content...")
    if "```mermaid" in processed_content:
        print("⚠ Warning: Mermaid code blocks still present in processed content")
        print("  This means diagrams were not properly replaced with images")
    else:
        print("✓ Mermaid code blocks removed (replaced with images)")
    
    # Check if images are referenced
    image_refs = processed_content.count("![Mermaid Diagram")
    print(f"  Image references found: {image_refs}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    print(f"\nPlease open 'test_output.pdf' to verify:")
    print("  1. Mermaid diagrams are rendered as images (not code)")
    print("  2. Python code block is still visible")
    print("  3. All diagrams display correctly")
    
    return True


if __name__ == "__main__":
    success = test_markdown_processing()
    sys.exit(0 if success else 1)
