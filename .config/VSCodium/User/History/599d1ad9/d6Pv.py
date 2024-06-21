import jsonlines
import string
import re
import spacy
from multiprocessing import Pool, cpu_count, current_process

# Initialize spaCy with English model
nlp = spacy.load('en_core_web_sm')

# Function to clean and tokenize text using spaCy
def clean_and_tokenize(text):
    # Remove non-ASCII characters and normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # Apply spaCy NLP pipeline
    doc = nlp(text)
    
    # Lemmatize tokens, remove stopwords and non-alphabetic tokens
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
    
    # Remove punctuations and single character tokens
    cleaned_tokens = [token for token in tokens if token not in string.punctuation and len(token) > 1]
    
    # Join tokens to form the cleaned text
    cleaned_text = " ".join(cleaned_tokens)
    
    return cleaned_text

def expand_query(query_text):
    # Simple heuristic for query expansion based on known genres
    genre_keywords = {
        'sci-fi': ['scifi', 'dystopian', 'experimental', 'surreal', 'future'],
        'drama': ['love', 'relationship', 'friendship', 'lonely', 'trouble', 'drama'],
        'horror': ['scary', 'fear', 'haunted', 'evil', 'dark', 'creepy'],
        'thriller': ['suspense', 'mystery', 'danger', 'tension', 'action'],
        'comedy': ['funny', 'humor', 'laugh', 'joke', 'comic'],
        'action': ['fight', 'battle', 'war', 'combat', 'action'],
        'romance': ['romantic', 'love', 'affection', 'heart', 'couple']
    }
    
    expanded_terms = set()
    
    # Tokenize query text
    tokens = query_text.lower().split()
    
    # Expand query based on genre keywords
    for genre, keywords in genre_keywords.items():
        for token in tokens:
            if token in keywords:
                expanded_terms.add(genre)
                break
    
    return list(expanded_terms) if expanded_terms else ['N/A']  # Return ['N/A'] if no genre is inferred

def process_query(query):
    query_id = query['query_id']
    query_text = query['query']
    
    # Clean and tokenize query text
    cleaned_text = clean_and_tokenize(query_text)
    
    # Expand query to infer genre
    inferred_genre = expand_query(query_text)
    
    # Add genre field to processed query
    processed_query = {
        'query_id': query_id,
        'query': cleaned_text,
        'genre': inferred_genre[0]  # Include the inferred genre under 'genre' field
    }
    
    return processed_query

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

# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/query_analysis/queries.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/query_analysis/cleaned_queries2.jsonl'
process_queries(input_file_path, output_file_path)
