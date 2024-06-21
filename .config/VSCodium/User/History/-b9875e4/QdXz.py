import jsonlines

def extract_section_titles(file_path):
    output_data = []

    with jsonlines.open(file_path) as reader:
        for obj in reader:
            doc_id = obj.get('doc_id')
            title = obj.get('title')
            sections = obj.get('sections', [])
            titles = [section.get('section') for section in sections]
            output_data.append({
                'doc_id': doc_id,
                'title': title,
                'sections': titles
            })
    
    return output_data

def save_section_titles(output_path, data):
    with jsonlines.open(output_path, mode='w') as writer:
        writer.write_all(data)

# Replace 'corpus.jsonl' with the path to your JSONL file
input_file_path = '/home/shuvam/Information_Retrieval/Corpu_and_dataset/corpus/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpu_and_dataset/corpus/corpus_sec.jsonl'

# Extract section titles and save to the new file
section_titles = extract_section_titles(input_file_path)
save_section_titles(output_file_path, section_titles)
