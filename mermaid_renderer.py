"""
Mermaid Renderer Module
Converts mermaid diagrams to images using playwright
"""
import os
import re
import tempfile
import base64
from pathlib import Path
from typing import List, Tuple
import asyncio


class MermaidRenderer:
    """Renders mermaid diagrams to images"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='mermaid_')
        self.image_counter = 0
        
    async def setup_browser(self):
        """Initialize playwright browser"""
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch()
            self.context = await self.browser.new_context()
            return True
        except ImportError:
            print("Warning: Playwright not available. Install with: pip install playwright")
            print("Then run: playwright install chromium")
            return False
        except Exception as e:
            print(f"Warning: Could not initialize browser: {e}")
            return False
    
    async def cleanup_browser(self):
        """Cleanup playwright resources"""
        if hasattr(self, 'browser'):
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    def extract_mermaid_blocks(self, markdown_content: str) -> List[Tuple[str, str, int, int]]:
        """Extract all mermaid code blocks from markdown with their positions"""
        blocks = []
        
        # Pattern 1: Properly tagged mermaid blocks (case insensitive)
        pattern1 = r'```mermaid\s*\n(.*?)\n```'
        for match in re.finditer(pattern1, markdown_content, re.DOTALL | re.IGNORECASE):
            mermaid_code = match.group(1).strip()
            full_match = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            blocks.append((full_match, mermaid_code, start_pos, end_pos))
        
        # Pattern 2: Mermaid blocks without closing newline
        pattern2 = r'```mermaid\s*\n(.*?)```'
        for match in re.finditer(pattern2, markdown_content, re.DOTALL | re.IGNORECASE):
            mermaid_code = match.group(1).strip()
            full_match = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            # Check if not already found
            if not any(b[2] == start_pos for b in blocks):
                blocks.append((full_match, mermaid_code, start_pos, end_pos))
        
        # Pattern 3: Untagged blocks that start with mermaid keywords
        pattern3 = r'```\s*\n((?:graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|journey|gitGraph|mindmap|timeline|quadrantChart)[^\n]*.*?)\n```'
        for match in re.finditer(pattern3, markdown_content, re.DOTALL | re.IGNORECASE):
            mermaid_code = match.group(1).strip()
            full_match = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            # Check if not already found
            if not any(b[2] == start_pos for b in blocks):
                print(f"  Found untagged mermaid diagram at pos {start_pos}")
                blocks.append((full_match, mermaid_code, start_pos, end_pos))
        
        return blocks
    
    async def render_mermaid_to_image(self, mermaid_code: str, output_path: str) -> bool:
        """Render a single mermaid diagram to an image file"""
        try:
            page = await self.context.new_page()
            
            # Create HTML with mermaid
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script type="module">
                    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                    mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
                </script>
            </head>
            <body>
                <div class="mermaid">
{mermaid_code}
                </div>
            </body>
            </html>
            """
            
            await page.set_content(html_content)
            
            # Wait for mermaid to render
            await page.wait_for_timeout(2000)
            
            # Find the rendered SVG
            element = await page.query_selector('.mermaid svg')
            if element:
                await element.screenshot(path=output_path)
                await page.close()
                return True
            else:
                print(f"Warning: Could not find rendered mermaid diagram")
                await page.close()
                return False
                
        except Exception as e:
            print(f"Error rendering mermaid: {e}")
            return False
    
    def render_mermaid_fallback(self, mermaid_code: str, output_path: str) -> bool:
        """Fallback: Render mermaid using mermaid.ink API"""
        try:
            import requests
            import base64
            
            print(f"  Using fallback: mermaid.ink API")
            
            # Encode mermaid code
            mermaid_bytes = mermaid_code.encode('utf-8')
            encoded = base64.b64encode(mermaid_bytes).decode('utf-8')
            
            # Use mermaid.ink API to render the diagram
            url = f"https://mermaid.ink/img/{encoded}"
            
            # Download the rendered image
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ Rendered via mermaid.ink API")
                return True
            else:
                print(f"  ✗ mermaid.ink API returned status {response.status_code}")
                return self._render_mermaid_pil_fallback(mermaid_code, output_path)
                
        except Exception as e:
            print(f"  ✗ mermaid.ink API failed: {e}")
            return self._render_mermaid_pil_fallback(mermaid_code, output_path)
    
    def _render_mermaid_pil_fallback(self, mermaid_code: str, output_path: str) -> bool:
        """Ultimate fallback: Create a simple diagram visualization with PIL"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            print(f"  Using PIL fallback")
            
            # Create a larger image
            img = Image.new('RGB', (1200, 800), color='white')
            draw = ImageDraw.Draw(img)
            
            # Add border
            draw.rectangle([10, 10, 1190, 790], outline='#333', width=2)
            
            # Extract diagram type and content
            lines = mermaid_code.strip().split('\n')
            diagram_type = lines[0].strip() if lines else 'graph'
            
            try:
                font_title = ImageFont.truetype("arial.ttf", 24)
                font_text = ImageFont.truetype("arial.ttf", 14)
            except:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()
            
            # Draw title
            title = f"Mermaid {diagram_type.split()[0].title()} Diagram"
            draw.text((30, 30), title, fill='#2c3e50', font=font_title)
            
            # Draw the mermaid code in a readable format
            y_position = 80
            for line in lines[:15]:  # Show first 15 lines
                if line.strip():
                    draw.text((30, y_position), line[:80], fill='#555', font=font_text)
                    y_position += 25
            
            # Add a note
            draw.text((30, y_position + 40), 
                     "Note: Full diagram rendering requires Playwright/Chromium", 
                     fill='#888', font=font_text)
            
            img.save(output_path)
            print(f"  ✓ Created PIL fallback image")
            return True
        except Exception as e:
            print(f"  ✗ PIL fallback failed: {e}")
            return False
    
    async def process_markdown_async(self, markdown_content: str) -> str:
        """Process markdown and replace mermaid blocks with images"""
        blocks = self.extract_mermaid_blocks(markdown_content)
        
        if not blocks:
            print("No mermaid blocks found in markdown content")
            return markdown_content
        
        print(f"Found {len(blocks)} mermaid blocks to render")
        
        # Try to setup browser
        browser_available = await self.setup_browser()
        print(f"Browser available: {browser_available}")
        
        if not browser_available:
            print("⚠️ Browser not available - using mermaid.ink fallback API")
        
        # Process blocks in reverse order by position to maintain string positions
        blocks_sorted = sorted(blocks, key=lambda x: x[2], reverse=True)
        
        replacements = []  # Store (start, end, replacement_text)
        
        for full_block, mermaid_code, start_pos, end_pos in blocks_sorted:
            self.image_counter += 1
            image_filename = f"mermaid_diagram_{self.image_counter}.png"
            image_path = os.path.join(self.temp_dir, image_filename)
            
            print(f"\n[Diagram {self.image_counter}] at position {start_pos}-{end_pos}")
            print(f"  Mermaid code preview: {mermaid_code[:60]}...")
            print(f"  Output path: {image_path}")
            
            # Try to render with browser, fallback to API
            if browser_available:
                success = await self.render_mermaid_to_image(mermaid_code, image_path)
                if not success:
                    print(f"  Browser render failed, trying mermaid.ink API")
                    success = self.render_mermaid_fallback(mermaid_code, image_path)
            else:
                success = self.render_mermaid_fallback(mermaid_code, image_path)
            
            if success and os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                print(f"  ✓ Image created: {file_size} bytes")
                
                # Create image reference
                image_markdown = f"\n![Mermaid Diagram {self.image_counter}]({image_filename})\n"
                replacements.append((start_pos, end_pos, image_markdown))
                print(f"  ✓ Scheduled replacement")
            else:
                print(f"  ✗ Failed to create image file - keeping code block")
        
        # Apply replacements in reverse order
        processed_content = markdown_content
        for start_pos, end_pos, replacement in replacements:
            processed_content = processed_content[:start_pos] + replacement + processed_content[end_pos:]
        
        if browser_available:
            await self.cleanup_browser()
        
        replacements_made = len(replacements)
        print(f"\nTotal replacements made: {replacements_made}/{len(blocks)}")
        
        # Final verification
        remaining_mermaid = len(re.findall(r'```mermaid', processed_content, re.IGNORECASE))
        if remaining_mermaid > 0:
            print(f"⚠️ WARNING: {remaining_mermaid} mermaid blocks still remain in content!")
        else:
            print(f"✓ All mermaid blocks successfully replaced with images")
        
        return processed_content
    
    def process_markdown(self, markdown_content: str) -> str:
        """Synchronous wrapper for process_markdown_async"""
        return asyncio.run(self.process_markdown_async(markdown_content))
    
    def get_temp_dir(self) -> str:
        """Get the temporary directory containing generated images"""
        return self.temp_dir
