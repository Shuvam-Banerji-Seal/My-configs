import jsonlines
from rake_nltk import Rake
from unidecode import unidecode
import multiprocessing
from multiprocessing import Pool, Manager
import os

def process_document(document, shared_keywords):
    try:
        doc_id = document['doc_id']
        text = document['text']

        # Convert unicode characters to ASCII
        text = unidecode(text)

        # Extract keywords using RAKE
        rake = Rake()
        rake.extract_keywords_from_text(text)
        keywords = list(set([kw.strip() for kw in rake.get_ranked_phrases() if kw.strip()]))

        # Print the current doc_id and extracted keywords
        print(f"Processing Document ID: {doc_id}")
        print("Keywords:", keywords)

        # Add keywords to shared list
        shared_keywords.extend(keywords)

        return {'doc_id': doc_id, 'keywords': keywords}
    except Exception as e:
        print(f"Error processing document ID: {document.get('doc_id', 'Unknown')} - {e}")
        return None

def process_chunk(chunk, shared_keywords):
    results = []
    for document in chunk:
        result = process_document(document, shared_keywords)
        if result:
            results.append(result)
    return results

def extract_keywords_from_corpus(input_file_path, output_file_path, chunk_size=1048576):  # Default chunk size set to 1MB
    try:
        manager = Manager()
        shared_keywords = manager.list()

        with open(input_file_path, 'r', encoding='utf-8') as f:
            file_size = os.path.getsize(input_file_path)
            processed_size = 0

            while processed_size < file_size:
                # Read chunk
                chunk_data = []
                while processed_size < file_size and len(chunk_data) < chunk_size:
                    line = f.readline()
                    if not line:
                        break
                    try:
                        chunk_data.append(json.loads(line))
                        processed_size += len(line.encode('utf-8'))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding line: {e}")
                        continue

                if chunk_data:
                    with Pool(multiprocessing.cpu_count()) as pool:
                        results = pool.starmap(process_document, [(doc, shared_keywords) for doc in chunk_data])
                    
                    # Write results to output file (avoid duplicates)
                    unique_keywords = set()
                    with jsonlines.open(output_file_path, mode='a') as writer:
                        for result in results:
                            if result:
                                doc_id = result['doc_id']
                                keywords = result['keywords']
                                unique_keywords.update(keywords)
                                writer.write(result)
                    
                    # Extend shared_keywords with unique keywords
                    shared_keywords.extend(unique_keywords)

        # Write all unique keywords to a separate file
        unique_keywords_file = 'unique_keywords.jsonl'
        with jsonlines.open(unique_keywords_file, mode='w') as writer:
            for keyword in shared_keywords:
                writer.write({'keyword': keyword})

    except Exception as e:
        print(f"Error processing the corpus: {e}")


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
