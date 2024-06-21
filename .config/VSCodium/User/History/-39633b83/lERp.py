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

def process_document(obj):
    doc_id = obj['doc_id']
    text = obj['text']

    # Clean and tokenize text
    cleaned_text = clean_and_tokenize(text)

    # Initialize RAKE with NLTK's stopwords
    rake = Rake(stopwords=stopwords.words('english'))
    
    # Extract keywords using RAKE
    rake.extract_keywords_from_text(cleaned_text)
    keywords = rake.get_ranked_phrases()

    return {'doc_id': doc_id, 'keywords': keywords}

def extract_keywords_from_corpus(input_file_path, output_file_path, batch_size=100):
    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Initialize output JSONL file for writing
        with jsonlines.open(output_file_path, mode='w') as writer:
            # Initialize multiprocessing pool
            pool = Pool(processes=cpu_count())

            try:
                # Process each document individually
                results = pool.imap(process_document, reader)

                # Write results to output file
                writer.write_all(results)

            finally:
                # Close multiprocessing pool
                pool.close()
                pool.join()

# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
