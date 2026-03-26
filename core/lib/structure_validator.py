"""
Structure Validator Module
Enforces mandatory structure checks for SRS based on ISO/IEC/IEEE 29148:2018 standards.
"""

from typing import List, Tuple, Dict
import re
from .srs_parser import SRSParser

MANDATORY_SECTIONS = [
    "Introduction",
    "Overall Description", 
    "Specific Requirements",
    "Stakeholder Requirements",
]

def normalize_section_name(name: str) -> str:
    clean_name = re.sub(r'^\d+(\.\d+)*\s*', '', name).strip()
    return clean_name.lower()

def validate_structure(srs_parser: SRSParser, strict: bool = False) -> Tuple[bool, List[str], List[str]]:
    existing_sections = srs_parser.get_section_list()
    existing_normalized = {normalize_section_name(s): s for s in existing_sections}
    
    missing_sections = []
    present_sections = []
    
    for mandatory in MANDATORY_SECTIONS:
        mandatory_normalized = normalize_section_name(mandatory)
        
        found = False
        if srs_parser.get_section(mandatory):
            found = True
        elif mandatory_normalized in existing_normalized:
            found = True
            
        if found:
            present_sections.append(mandatory)
        else:
            missing_sections.append(mandatory)
            
    is_valid = len(missing_sections) == 0 if strict else len(present_sections) > 0
    
    return is_valid, missing_sections, present_sections
