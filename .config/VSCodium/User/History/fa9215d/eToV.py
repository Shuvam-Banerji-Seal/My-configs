import json

def filter_docs_without_abstract(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Parse the JSON line
            doc = json.loads(line.strip())
            
            # Check if 'Abstract' is not in the sections list
            if "Abstract" not in doc.get('sections', []):
                # Extract doc_id and sections
                filtered_doc = {
                    "doc_id": doc["doc_id"],
                    "sections": doc["sections"]
                }
                # Write to the output file in JSONL format
                outfile.write(json.dumps(filtered_doc) + '\n')

# Define the input and output file paths
input_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/corpus_sec.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/corpus_sec_no_abs.jsonl'

# Call the function to filter documents
filter_docs_without_abstract(input_file_path, output_file_path)
