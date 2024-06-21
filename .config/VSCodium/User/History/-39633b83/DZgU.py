import jsonlines
from rake_nltk import Rake
from unidecode import unidecode
import multiprocessing
from multiprocessing import Pool

def process_document(document):
    try:
        doc_id = document['doc_id']
        text = document['text']

        # Convert unicode characters to ASCII
        text = unidecode(text)

        # Extract keywords using RAKE
        rake = Rake()
        rake.extract_keywords_from_text(text)
        keywords = rake.get_ranked_phrases()

        # Print the current doc_id and extracted keywords
        print(f"Processing Document ID: {doc_id}")
        print("Keywords:", keywords)

        return {'doc_id': doc_id, 'keywords': keywords}
    except Exception as e:
        print(f"Error processing document ID: {document.get('doc_id', 'Unknown')} - {e}")
        return None

def process_chunk(chunk):
    return [process_document(doc) for doc in chunk if doc is not None]

def extract_keywords_from_corpus(input_file_path, output_file_path, chunk_size=1000):
    try:
        # Open the input JSONL file for reading
        with jsonlines.open(input_file_path) as reader:
            chunk = []
            for obj in reader:
                chunk.append(obj)
                if len(chunk) == chunk_size:
                    with Pool(multiprocessing.cpu_count()) as pool:
                        results = pool.map(process_chunk, [chunk])
                    # Write the results to the output JSONL file
                    with jsonlines.open(output_file_path, mode='a') as writer:
                        for result in results:
                            for item in result:
                                if item:
                                    writer.write(item)
                    chunk = []

            # Process any remaining documents in the last chunk
            if chunk:
                with Pool(multiprocessing.cpu_count()) as pool:
                    results = pool.map(process_chunk, [chunk])
                with jsonlines.open(output_file_path, mode='a') as writer:
                    for result in results:
                        for item in result:
                            if item:
                                writer.write(item)
    except Exception as e:
        print(f"Error processing the corpus: {e}")



# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
