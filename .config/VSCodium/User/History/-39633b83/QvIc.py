import jsonlines
from rake_nltk import Rake
from unidecode import unidecode
import multiprocessing
from multiprocessing import Pool
import os

def process_document(document):
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

        return {'doc_id': doc_id, 'keywords': keywords}
    except Exception as e:
        print(f"Error processing document ID: {document.get('doc_id', 'Unknown')} - {e}")
        return None

def process_chunk(chunk):
    results = []
    for document in chunk:
        result = process_document(document)
        if result:
            results.append(result)
    return results

def extract_keywords_from_corpus(input_file_path, output_file_path, chunk_size=1048576):  # Default chunk size set to 1MB
    try:
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
                        chunk_data.append(jsonlines.loads(line))
                        processed_size += len(line.encode('utf-8'))
                    except jsonlines.DecoderError as e:
                        print(f"Error decoding line: {e}")
                        continue

                if chunk_data:
                    with Pool(multiprocessing.cpu_count()) as pool:
                        results = pool.map(process_document, chunk_data)
                    with jsonlines.open(output_file_path, mode='a') as writer:
                        for result in results:
                            if result:
                                writer.write(result)

    except Exception as e:
        print(f"Error processing the corpus: {e}")


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
