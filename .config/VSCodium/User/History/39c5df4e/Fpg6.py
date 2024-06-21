import json
from collections import defaultdict

def count_sections(jsonl_file, output_jsonl_file):
    section_count = defaultdict(int)
    document_count = defaultdict(int)

    # Process the input JSONL file
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

    # Prepare results to write to output JSONL file
    results = []
    rank = 1
    for section, freq in sorted_sections:
        documents_found = document_count[section]
        total_documents = len(document_count)
        result = {
            "section": section,
            "rank": rank,
            "frequency": freq,
            "documents_found_in": documents_found,
            "total_documents": total_documents
        }
        results.append(result)
        rank += 1

    # Write results to output JSONL file
    with open(output_jsonl_file, 'w', encoding='utf-8') as outfile:
        for result in results:
            json.dump(result, outfile)
            outfile.write('\n')

# Example usage:
jsonl_file = 'sample.jsonl'           # Replace with your JSONL file path
output_jsonl_file = 'results.jsonl'   # Replace with desired output JSONL file path
count_sections(jsonl_file, output_jsonl_file)
