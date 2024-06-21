import jsonlines
import logging

# Configure logging
logging.basicConfig(filename='extraction_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_document(obj):
    doc_id = obj.get('doc_id')
    title = obj.get('title')
    sections = obj.get('sections', [])
    titles = [section.get('section') for section in sections]
    
    # Print to terminal and log file
    print(f"Processing doc_id: {doc_id}, Sections: {titles}", flush=True)
    logging.info(f"Processing doc_id: {doc_id}, Sections: {titles}")
    
    return {
        'doc_id': doc_id,
        'title': title,
        'sections': titles
    }

def extract_section_titles(file_path):
    output_data = []

    try:
        with jsonlines.open(file_path) as reader:
            # Iterate over each line (document) in the JSONL file
            for obj in reader.iter():
                print(f"Processing doc_id: {obj['doc_id']}", flush=True)
                logging.info(f"Processing doc_id: {obj['doc_id']}")

                result = process_document(obj)
                output_data.append(result)

    except Exception as e:
        print(f"Error reading or processing file: {e}", flush=True)
        logging.error(f"Error reading or processing file: {e}")

    return output_data

def save_section_titles(output_path, data):
    try:
        with jsonlines.open(output_path, mode='w') as writer:
            writer.write_all(data)
        print(f"Data saved to {output_path}", flush=True)
        logging.info(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}", flush=True)
        logging.error(f"Error saving data: {e}")

# Replace 'corpus.jsonl' with the path to your JSONL file
input_file_path = '/home/shuvam/Information_Retrieval/Corpu_and_dataset/corpus/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpu_and_dataset/corpus/corpus_sec.jsonl'

# Extract section titles and save to the new file
print("Starting extraction process...", flush=True)
logging.info("Starting extraction process...")
section_titles = extract_section_titles(input_file_path)
print("Extraction process completed.", flush=True)
logging.info("Extraction process completed.")
print("Saving data...", flush=True)
logging.info("Saving data...")
save_section_titles(output_file_path, section_titles)
print("All done.", flush=True)
logging.info("All done.")
