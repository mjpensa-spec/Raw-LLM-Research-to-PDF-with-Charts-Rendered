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
    
    def extract_mermaid_blocks(self, markdown_content: str) -> List[Tuple[str, str]]:
        """Extract all mermaid code blocks from markdown"""
        # Match both properly tagged mermaid blocks and untagged blocks that look like mermaid
        pattern = r'```mermaid\n(.*?)```'
        matches = re.finditer(pattern, markdown_content, re.DOTALL | re.IGNORECASE)
        
        blocks = []
        for match in matches:
            mermaid_code = match.group(1).strip()
            full_match = match.group(0)
            blocks.append((full_match, mermaid_code))
        
        # Also check for code blocks without language tags that start with mermaid keywords
        generic_pattern = r'```\n((?:graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|journey|gitGraph|mindmap|timeline|quadrantChart).*?)```'
        generic_matches = re.finditer(generic_pattern, markdown_content, re.DOTALL | re.IGNORECASE)
        
        for match in generic_matches:
            mermaid_code = match.group(1).strip()
            full_match = match.group(0)
            # Avoid duplicates
            if (full_match, mermaid_code) not in blocks:
                print(f"Found untagged mermaid diagram: {mermaid_code[:50]}...")
                blocks.append((full_match, mermaid_code))
        
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
        """Fallback: Create a simple text representation"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple image with the diagram type
            img = Image.new('RGB', (800, 400), color='white')
            draw = ImageDraw.Draw(img)
            
            # Extract diagram type
            first_line = mermaid_code.split('\n')[0].strip()
            
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            text = f"Mermaid Diagram:\n{first_line}\n\n(Render in browser for full visualization)"
            draw.text((50, 50), text, fill='black', font=font)
            
            img.save(output_path)
            return True
        except Exception as e:
            print(f"Error creating fallback image: {e}")
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
        
        processed_content = markdown_content
        
        for full_block, mermaid_code in blocks:
            self.image_counter += 1
            image_filename = f"mermaid_diagram_{self.image_counter}.png"
            image_path = os.path.join(self.temp_dir, image_filename)
            
            print(f"Rendering mermaid diagram {self.image_counter} to {image_path}")
            
            # Try to render with browser, fallback to simple image
            if browser_available:
                success = await self.render_mermaid_to_image(mermaid_code, image_path)
            else:
                success = self.render_mermaid_fallback(mermaid_code, image_path)
            
            if success and os.path.exists(image_path):
                # Use absolute path for image reference so WeasyPrint can find it
                abs_image_path = os.path.abspath(image_path)
                print(f"Successfully rendered diagram, absolute path: {abs_image_path}")
                
                # Replace mermaid block with image reference using just the filename
                # The base_url will handle resolving it
                image_markdown = f"\n![Mermaid Diagram {self.image_counter}]({image_filename})\n"
                processed_content = processed_content.replace(full_block, image_markdown, 1)
            else:
                print(f"Failed to render diagram {self.image_counter}")
        
        if browser_available:
            await self.cleanup_browser()
        
        return processed_content
    
    def process_markdown(self, markdown_content: str) -> str:
        """Synchronous wrapper for process_markdown_async"""
        return asyncio.run(self.process_markdown_async(markdown_content))
    
    def get_temp_dir(self) -> str:
        """Get the temporary directory containing generated images"""
        return self.temp_dir
