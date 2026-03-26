import docx
import sys

def main():
    doc_path = r'C:\Users\thanb\.gemini\projects\PRDReviewer\resources\PRD AI Health.docx'
    out_path = r'C:\Users\thanb\.gemini\projects\SRSReviewer\srs_docs\prd_text.txt'
    
    doc = docx.Document(doc_path)
    text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
        
    print("Done extracting PRD")

if __name__ == '__main__':
    main()
