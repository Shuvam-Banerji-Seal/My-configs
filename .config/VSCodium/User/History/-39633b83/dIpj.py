import jsonlines
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
from multiprocessing import Pool, cpu_count

def clean_and_tokenize(text):
    # Clean and normalize text (remove non-ASCII characters and normalize newlines)
    text = unidecode(text)
    text = text.replace("\n", " ")

    # Tokenize text using NLTK's word tokenizer
    tokens = word_tokenize(text)

    # Convert tokens back to a single string
    cleaned_text = " ".join(tokens)
    return cleaned_text

def process_documents(batch):
    # Initialize RAKE with NLTK's stopwords
    rake = Rake(stopwords=stopwords.words('english'))

    results = []
    for obj in batch:
        doc_id = obj['doc_id']
        text = obj['text']

        # Clean and tokenize text
        cleaned_text = clean_and_tokenize(text)

        # Extract keywords using RAKE
        rake.extract_keywords_from_text(cleaned_text)
        keywords = rake.get_ranked_phrases()

        results.append({'doc_id': doc_id, 'keywords': keywords})

    return results

def extract_keywords_from_corpus(input_file_path, output_file_path, batch_size=100):
    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Initialize output JSONL file for writing
        with jsonlines.open(output_file_path, mode='w') as writer:
            # Initialize multiprocessing pool
            pool = Pool(processes=cpu_count())

            try:
                while True:
                    # Read a batch of documents
                    batch = [obj for obj in reader.iter(batch_size)]
                    
                    # Exit loop if no more documents
                    if not batch:
                        break
                    
                    # Split batch into chunks for multiprocessing
                    chunk_size = max(1, len(batch) // cpu_count())
                    chunks = [batch[i:i + chunk_size] for i in range(0, len(batch), chunk_size)]

                    # Process chunks using multiprocessing
                    results = pool.map(process_documents, chunks)

                    # Flatten results (list of lists) into a single list of dictionaries
                    flattened_results = [item for sublist in results for item in sublist]

                    # Write flattened results to output file
                    writer.write_all(flattened_results)

            finally:
                # Close multiprocessing pool
                pool.close()
                pool.join()


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
