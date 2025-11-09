# Rendering Fix Documentation

## Problem Description

The PDF output was showing Mermaid diagram code blocks instead of rendered visual diagrams. LLM-generated research often contains:
- Mermaid flowcharts, sequence diagrams, and other visual diagrams
- These should appear as images in the final PDF
- Instead, they were appearing as raw code blocks

## Root Causes Identified

1. **Image Path Resolution Issue**: 
   - Mermaid diagrams were being rendered to PNG images in a temporary directory
   - WeasyPrint (PDF converter) couldn't find these images due to incorrect base URL
   - The `base_url` parameter wasn't being set properly for image resolution

2. **Relative vs Absolute Paths**:
   - Images were referenced with absolute file paths
   - WeasyPrint needed either relative paths with a proper base_url OR file:// URLs
   - The markdown contained paths like `/tmp/mermaid_xxx/diagram.png` which WeasyPrint couldn't resolve

3. **Code Block Detection**:
   - The `remove_non_essential_code_blocks()` function wasn't aggressive enough
   - It was keeping diagram code blocks that should have been removed
   - Untagged mermaid blocks weren't being detected

## Fixes Applied

### 1. Fixed Image Path Resolution in `pdf_converter.py`

**Changes:**
- Added `image_base_path` parameter to `convert_markdown_to_pdf()`
- Modified `html_to_pdf()` to accept and use a `base_url` parameter
- Convert the base path to proper file:// URL format for WeasyPrint
- Added debug logging to track base_url being used

**Code:**
```python
def convert_markdown_to_pdf(self, markdown_content: str, output_path: str, 
                           image_base_path: Optional[str] = None) -> bool:
    html_content = self.markdown_to_html(markdown_content)
    
    # Set base_url for image resolution
    base_url = None
    if image_base_path:
        # Convert to file:// URL format
        base_url = f"file:///{os.path.abspath(image_base_path).replace(os.sep, '/')}/"
    
    return self.html_to_pdf(html_content, output_path, base_url=base_url)
```

### 2. Updated Image References in `mermaid_renderer.py`

**Changes:**
- Changed from absolute paths to relative filenames in markdown
- The base_url in WeasyPrint now resolves these relative paths
- Added debug logging to track rendering progress
- Improved detection of untagged mermaid blocks

**Code:**
```python
# Use just the filename - base_url will resolve it
image_markdown = f"\n![Mermaid Diagram {self.image_counter}]({image_filename})\n"
```

**Also added:**
- Detection for mermaid diagrams without language tags
- Case-insensitive matching for mermaid blocks
- Better logging of found diagrams

### 3. Connected Components in `app.py`

**Changes:**
- Pass the mermaid temp directory to PDF converter
- Added logging to track the image directory path

**Code:**
```python
# Get the temp directory where images are stored
image_temp_dir = renderer.get_temp_dir()
print(f"Mermaid images stored in: {image_temp_dir}")

# Convert to PDF with image base path
converter = PDFConverter()
success = converter.convert_markdown_to_pdf(
    processed_content, 
    output_path,
    image_base_path=image_temp_dir
)
```

### 4. Improved Code Block Removal

**Changes:**
- More aggressive diagram keyword detection
- Added more diagram-related keywords (gantt, sequence, state, etc.)
- Content inspection even for untagged blocks
- Better logging of what's being removed

**Keywords added:**
- gantt, sequence, class, state, entity, pie, timeline, mindmap, gitgraph

### 5. Enhanced CSS for PDF Output

**Changes:**
- Added `page-break-inside: avoid` to images
- Ensures diagrams don't split across pages

## How It Works Now

1. **Upload**: User uploads markdown with mermaid code blocks
2. **Fix Syntax**: `MarkdownFixer` cleans up any syntax issues
3. **Render Diagrams**: 
   - `MermaidRenderer` finds all mermaid blocks (tagged and untagged)
   - Uses Playwright to render each to PNG in temp directory
   - Replaces code blocks with `![Mermaid Diagram](filename.png)` references
4. **Remove Leftover Code**: 
   - Removes any remaining diagram code blocks
   - Keeps actual programming language code blocks (Python, JavaScript, etc.)
5. **Convert to PDF**:
   - `PDFConverter` converts markdown to HTML
   - Sets base_url to the temp directory
   - WeasyPrint resolves image references and embeds images in PDF
   - Outputs final PDF with all diagrams rendered as images

## Testing the Fix

Run the test script:
```powershell
python test_rendering.py
```

This will:
1. Create test markdown with mermaid diagrams
2. Process it through the full pipeline
3. Generate `test_output.pdf`
4. Report on success/failure

**Expected output:**
- ✓ All modules imported
- ✓ Markdown fixed
- ✓ Mermaid diagrams rendered (with count of PNG files created)
- ✓ PDF created successfully
- ✓ No mermaid code blocks in processed content
- ✓ Image references found

## Verification Checklist

Open the generated PDF and verify:

- [ ] Flowchart appears as a diagram image (not code)
- [ ] Sequence diagram appears as a diagram image (not code)
- [ ] Python code block still appears as formatted code
- [ ] Untagged mermaid diagram is rendered
- [ ] No `graph TD`, `sequenceDiagram`, or other diagram code visible
- [ ] Images are clear and properly sized
- [ ] No broken image icons

## Deployment Notes

When deploying, ensure:

1. **Playwright is installed**:
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **WeasyPrint dependencies** (especially on Windows):
   - GTK3 runtime required
   - See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows

3. **Sufficient disk space** for temporary image files

4. **Check logs** for these messages:
   - "Found X mermaid blocks to render"
   - "Browser available: True"
   - "Successfully rendered diagram, absolute path: ..."
   - "Mermaid images stored in: ..."

## Troubleshooting

### Images still not appearing in PDF

1. Check logs for "Browser available: False"
   - Install Playwright: `playwright install chromium`
   
2. Check logs for "Failed to render diagram"
   - Verify mermaid syntax is valid
   - Check if Chromium browser is accessible

3. Check for WeasyPrint warnings
   - Ensure base_url is being set correctly
   - Verify image files exist in temp directory

### Code blocks still appearing

1. Verify mermaid blocks are being detected
   - Look for "Found X mermaid blocks" in logs
   
2. Check if blocks are tagged correctly
   - Should be ` ```mermaid` not ` ```diagram` or untagged

3. Ensure removal function is running
   - Look for "Removing code block with language: X" in logs

## Performance Considerations

- Each mermaid diagram takes ~2-3 seconds to render (Playwright startup + render)
- Multiple diagrams are processed sequentially
- Temp files are cleaned up after 1 hour (see `cleanup_old_files()`)
- For large documents with many diagrams, processing may take time

## Future Enhancements

Possible improvements:
1. Parallel diagram rendering for faster processing
2. Caching rendered diagrams (same diagram = reuse image)
3. Support for other diagram types (PlantUML, GraphViz, etc.)
4. Option to embed diagrams as SVG instead of PNG
5. Configurable image quality/resolution
