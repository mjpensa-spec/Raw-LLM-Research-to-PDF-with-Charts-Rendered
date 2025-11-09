"""
Markdown Fixer Module
Handles parsing and fixing markdown syntax issues, especially for mermaid diagrams
"""
import re
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class CodeBlock:
    """Represents a code block in markdown"""
    language: str
    content: str
    start_line: int
    end_line: int
    is_valid: bool = True
    fixed_content: str = None


class MarkdownFixer:
    """Fixes common markdown rendering issues"""
    
    MERMAID_KEYWORDS = [
        'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
        'stateDiagram', 'erDiagram', 'gantt', 'pie', 'journey',
        'gitGraph', 'mindmap', 'timeline', 'quadrantChart'
    ]
    
    def __init__(self, content: str):
        self.content = content
        self.code_blocks: List[CodeBlock] = []
        
    def parse_code_blocks(self) -> List[CodeBlock]:
        """Extract all code blocks from markdown content"""
        # Pattern to match code blocks with or without language specifier
        pattern = r'^```(\w*)\n(.*?)^```'
        matches = re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        blocks = []
        for match in matches:
            language = match.group(1).strip().lower()
            content = match.group(2)
            start_pos = match.start()
            end_pos = match.end()
            
            # Count line numbers
            start_line = self.content[:start_pos].count('\n')
            end_line = self.content[:end_pos].count('\n')
            
            block = CodeBlock(
                language=language,
                content=content,
                start_line=start_line,
                end_line=end_line
            )
            blocks.append(block)
        
        self.code_blocks = blocks
        return blocks
    
    def detect_mermaid_blocks(self) -> List[CodeBlock]:
        """Detect blocks that should be mermaid but aren't marked correctly"""
        mermaid_blocks = []
        
        for block in self.code_blocks:
            # Check if language is already mermaid
            if block.language == 'mermaid':
                mermaid_blocks.append(block)
                continue
            
            # Check if content looks like mermaid but isn't marked
            content_lower = block.content.strip().lower()
            for keyword in self.MERMAID_KEYWORDS:
                if content_lower.startswith(keyword):
                    block.language = 'mermaid'
                    block.is_valid = False  # Needs fixing
                    mermaid_blocks.append(block)
                    break
        
        return mermaid_blocks
    
    def fix_mermaid_syntax(self, content: str) -> str:
        """Fix common mermaid syntax errors"""
        fixed = content.strip()
        
        # Fix common arrow syntax issues
        fixed = re.sub(r'-->', '-->', fixed)  # Normalize arrows
        fixed = re.sub(r'--->', '-->', fixed)
        
        # Fix node ID issues (remove spaces in IDs)
        # Pattern: Look for node definitions with spaces
        fixed = re.sub(r'\[([^\]]+)\]\s*\(([^\)]+)\)', r'[\1](\2)', fixed)
        
        # Ensure proper line endings
        lines = fixed.split('\n')
        cleaned_lines = [line.rstrip() for line in lines if line.strip()]
        fixed = '\n'.join(cleaned_lines)
        
        # Fix table syntax in mermaid (common LLM error)
        # Mermaid doesn't use markdown tables, convert to class diagram or other format
        if '|' in fixed and '---' in fixed:
            # This might be a mistaken markdown table in mermaid
            # Convert to a simple flowchart representation
            fixed = self._convert_table_to_flowchart(fixed)
        
        return fixed
    
    def _convert_table_to_flowchart(self, content: str) -> str:
        """Convert markdown table to flowchart if found in mermaid block"""
        lines = content.split('\n')
        
        # Check if it's actually a markdown table
        has_pipes = any('|' in line for line in lines)
        has_separator = any(re.match(r'\s*\|?\s*[-:]+\s*\|', line) for line in lines)
        
        if not has_pipes or not has_separator:
            return content
        
        # Extract table headers and rows
        table_lines = [line for line in lines if '|' in line]
        if len(table_lines) < 2:
            return content
        
        # Simple conversion: create a flowchart
        flowchart = "flowchart TD\n"
        node_id = 1
        
        for line in table_lines:
            if re.match(r'\s*\|?\s*[-:]+\s*\|', line):
                continue  # Skip separator
            
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                flowchart += f"    A{node_id}[{' | '.join(cells)}]\n"
                if node_id > 1:
                    flowchart += f"    A{node_id-1} --> A{node_id}\n"
                node_id += 1
        
        return flowchart
    
    def fix_all_issues(self) -> str:
        """Parse and fix all markdown issues"""
        self.parse_code_blocks()
        self.detect_mermaid_blocks()
        
        fixed_content = self.content
        
        # Process blocks in reverse order to maintain positions
        for block in reversed(self.code_blocks):
            if block.language == 'mermaid':
                # Fix mermaid syntax
                fixed_code = self.fix_mermaid_syntax(block.content)
                block.fixed_content = fixed_code
                
                # Create properly formatted code block
                old_block = f"```{block.language}\n{block.content}```"
                new_block = f"```mermaid\n{fixed_code}\n```"
                
                # Replace in content
                fixed_content = fixed_content.replace(old_block, new_block, 1)
        
        return fixed_content
    
    def add_missing_fences(self, content: str) -> str:
        """Add missing code fence markers"""
        # Look for common patterns that should be fenced
        lines = content.split('\n')
        result = []
        in_code = False
        
        for i, line in enumerate(lines):
            # Detect potential code blocks without fences
            # (e.g., multiple lines of indented code)
            if not in_code and line.startswith('    ') and i > 0:
                # Check if previous line was also indented
                if i < len(lines) - 1 and lines[i + 1].startswith('    '):
                    result.append('```')
                    in_code = True
            elif in_code and not line.startswith('    ') and line.strip():
                result.append('```')
                in_code = False
            
            result.append(line)
        
        if in_code:
            result.append('```')
        
        return '\n'.join(result)
