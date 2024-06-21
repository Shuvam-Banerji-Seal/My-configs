import json
from collections import defaultdict

def count_sections(jsonl_file):
    section_count = defaultdict(int)
    document_count = defaultdict(int)

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            sections = data.get('sections', [])

            # Count sections in current document
            seen_sections = set()
            for section in sections:
                section_count[section] += 1
                if section not in seen_sections:
                    document_count[section] += 1
                    seen_sections.add(section)

    # Sort sections by frequency in descending order
    sorted_sections = sorted(section_count.items(), key=lambda x: x[1], reverse=True)

    # Print results
    for section, freq in sorted_sections:
        documents_found = document_count[section]
        print(f'Section: {section}, Frequency: {freq}, Documents Found In: {documents_found}')

# Example usage:
jsonl_file = 'sample.jsonl'  # Replace with your JSONL file path
count_sections(jsonl_file)
