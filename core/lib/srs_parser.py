"""
SRS Parser Module
Utilities for parsing and extracting content from SRS documents
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

class SRSParser:
    """Parse SRS markdown files and extract structured content"""
    
    def __init__(self, srs_path: str):
        self.srs_path = Path(srs_path)
        self.content = self._load_content()
        self.sections = self._parse_sections()
    
    def _load_content(self) -> str:
        """Load SRS file content"""
        if not self.srs_path.exists():
            raise FileNotFoundError(f"SRS file not found: {self.srs_path}")
        
        with open(self.srs_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_sections(self) -> Dict[str, str]:
        """Parse markdown sections from SRS based on headings"""
        sections = {}
        current_section = "frontmatter"
        current_content = []
        
        lines = self.content.split('\n')
        
        for line in lines:
            header_match = re.match(r'^#{1,6}\s+(.+)$', line)
            if header_match:
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                # Remove markdown numbering like '1. ', '1.2 ', etc. for clean section names
                raw_name = header_match.group(1).strip()
                clean_name = re.sub(r'^\d+(\.\d+)*\s*', '', raw_name)
                current_section = clean_name
                current_content = [line] # include the header itself in the content
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections

    def get_section(self, section_name: str) -> Optional[str]:
        if section_name in self.sections:
            return self.sections[section_name]
        section_lower = section_name.lower()
        for key, value in self.sections.items():
            if section_lower in key.lower():
                return value
        return None
    
    def get_all_sections(self) -> Dict[str, str]:
        return self.sections
    
    def get_section_list(self) -> List[str]:
        return list(self.sections.keys())
