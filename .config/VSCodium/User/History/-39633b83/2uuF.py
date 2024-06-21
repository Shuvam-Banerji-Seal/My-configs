import jsonlines
from rake_nltk import Rake
from unidecode import unidecode
import multiprocessing
from multiprocessing import Pool, Manager

def process_document(document):
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

def extract_keywords_from_corpus(input_file_path, output_file_path):
    # Read the input JSONL file
    with jsonlines.open(input_file_path) as reader:
        documents = [obj for obj in reader]

    # Use multiprocessing to process documents in parallel
    with Pool(multiprocessing.cpu_count()) as pool:
        results = pool.map(process_document, documents)

    # Write the results to the output JSONL file
    with jsonlines.open(output_file_path, mode='w') as writer:
        for result in results:
            writer.write(result)



# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
