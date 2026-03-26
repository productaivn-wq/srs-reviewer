import json
import os
import yaml
from pathlib import Path

def main():
    root = Path(r'C:\Users\thanb\.gemini\projects\SRSReviewer')
    srs_dir = root / 'srs_docs'
    out_dir = root / 'srs_docs' / 'ready_prompts'
    out_dir.mkdir(exist_ok=True)
    
    # Load alignment prompt template
    prompt_path = root / 'core' / 'prompts' / 'srs_alignment_prompt.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    # Load PRD text
    with open(srs_dir / 'prd_text.txt', 'r', encoding='utf-8') as f:
        prd_text = f.read()
        
    # Load Health domain profile
    domain_path = root / 'core' / 'domain_profiles' / 'health.yaml'
    with open(domain_path, 'r', encoding='utf-8') as f:
        domain_profile = yaml.safe_load(f)
        
    # Format domain checks specifically
    domain_str = "\n\nDOMAIN SAFETY CHECKS (Health Profile):\n"
    for check in domain_profile.get('checks', []):
        domain_str += f"- [{check['id']}] {check['title']} ({check['severity']}): {check['description']}\n"
    domain_str += "Please ensure you score these domain safety checks within your review findings.\n"
    
    template = template.replace('{{REFERENCE_CONTENT}}', prd_text)
    template += domain_str
    
    # Process each SRS
    srs_files = [
        'US-29_30_Han_che_Chan_doan_Ke_don.md',
        'US-33_Quan_ly_Consent.md',
        'US-35_Khong_quang_cao.md',
        'US-36_Hien_thi_nguon_du_lieu.md'
    ]
    
    for filename in srs_files:
        srs_path = srs_dir / filename
        if not srs_path.exists():
            continue
        with open(srs_path, 'r', encoding='utf-8') as f:
            srs_text = f.read()
            
        full_prompt = template.replace('{{SRS_CONTENT}}', srs_text)
        
        # System instructions
        system_instruction = (
            "You are an expert system architect and business analyst reviewing an SRS document "
            "according to ISO/IEC/IEEE 29148:2018 standards. "
            "CRITICAL: Your ENTIRE response must be a single valid JSON object — no explanation, "
            "no markdown, no text before or after. Just pure JSON. "
            "Each dimension MUST have at least 2 issues. Review must be in Vietnamese. "
            "IMPORTANT: DO NOT use any tools. DO NOT attempt to write files or use the terminal. "
            "You MUST output ONLY the raw JSON string directly in your response message. "
            "DO NOT output the template variables verbatim; you must fill them with your actual evaluation."
        )
        
        final_text = f"{system_instruction}\n\n{full_prompt}"
        
        out_path = out_dir / f"{filename.split('_')[0]}_prompt.txt"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(final_text)
        print(f"Generated {out_path}")

if __name__ == '__main__':
    main()
