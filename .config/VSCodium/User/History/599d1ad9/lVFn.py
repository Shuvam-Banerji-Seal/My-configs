import jsonlines
import string
import re
import spacy
from multiprocessing import Pool, cpu_count, current_process
from autocorrect import Speller

# Initialize spaCy with English model
nlp = spacy.load('en_core_web_sm')

# Initialize spell checker
spell = Speller(lang='en')

# Function to clean and tokenize text using spaCy
def clean_and_tokenize(text):
    # Remove non-ASCII characters and normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # Apply spaCy NLP pipeline
    doc = nlp(text)
    
    # Lemmatize tokens, remove stopwords and non-alphabetic tokens
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
    
    # Spell check and correct tokens
    corrected_tokens = [spell(token) for token in tokens]
    
    # Remove punctuations and single character tokens
    cleaned_tokens = [token for token in corrected_tokens if token not in string.punctuation and len(token) > 1]
    
    # Join tokens to form the cleaned text
    cleaned_text = " ".join(cleaned_tokens)
    
    return cleaned_text

def process_query(query):
    query_id = query['query_id']
    query_text = query['query']
    
    # Clean and tokenize query text
    cleaned_text = clean_and_tokenize(query_text)

    return {
        'query_id': query_id,
        'query': cleaned_text
    }

def process_and_write_query(query, output_file_path):
    try:
        process_id = current_process().name
        print(f"Processing query ID {query['query_id']} on {process_id}")
        processed_query = process_query(query)
        with jsonlines.open(output_file_path, mode='a') as writer:
            writer.write(processed_query)
    except Exception as e:
        print(f"Error processing query ID {query['query_id']}: {e}")

def process_queries(input_file_path, output_file_path):
    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Initialize multiprocessing pool
        pool = Pool(processes=cpu_count())

        try:
            # Process each query individually
            for query in reader:
                pool.apply_async(process_and_write_query, (query, output_file_path))

            pool.close()
            pool.join()

        finally:
            pool.close()
            pool.join()

# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/query_analysis/queries.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/query_analysis/cleaned_queries.jsonl'
process_queries(input_file_path, output_file_path)
