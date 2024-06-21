import jsonlines
import concurrent.futures
import logging
import os

# Configure logging
logging.basicConfig(filename='extraction_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_document(obj):
    doc_id = obj.get('doc_id')
    title = obj.get('title')
    sections = obj.get('sections', [])
    titles = [section.get('section') for section in sections]
    
    # Print to terminal and log file
    print(f"Processing doc_id: {doc_id}, Sections: {titles}")
    logging.info(f"Processing doc_id: {doc_id}, Sections: {titles}")
    
    return {
        'doc_id': doc_id,
        'title': title,
        'sections': titles
    }

def extract_section_titles(file_path):
    output_data = []

    with jsonlines.open(file_path) as reader:
        documents = [obj for obj in reader]
        print(f"Total documents to process: {len(documents)}")
        logging.info(f"Total documents to process: {len(documents)}")

        # Get the number of available CPU cores
        max_workers = os.cpu_count()
        print(f"Using {max_workers} workers for processing.")
        logging.info(f"Using {max_workers} workers for processing.")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(process_document, documents))
            output_data.extend(results)

    return output_data

def save_section_titles(output_path, data):
    with jsonlines.open(output_path, mode='w') as writer:
        writer.write_all(data)
    print(f"Data saved to {output_path}")
    logging.info(f"Data saved to {output_path}")

# Replace 'corpus.jsonl' with the path to your JSONL file
input_file_path = '/home/shuvam/Information_Retrieval/Corpu_and_dataset/corpus/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpu_and_dataset/corpus/corpus_sec.jsonl'

# Extract section titles and save to the new file
print("Starting extraction process...")
logging.info("Starting extraction process...")
section_titles = extract_section_titles(input_file_path)
print("Extraction process completed.")
logging.info("Extraction process completed.")
print("Saving data...")
logging.info("Saving data...")
save_section_titles(output_file_path, section_titles)
print("All done.")
logging.info("All done.")
