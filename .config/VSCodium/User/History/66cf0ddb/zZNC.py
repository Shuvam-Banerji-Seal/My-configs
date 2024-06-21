import jsonlines
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
from multiprocessing import Pool, cpu_count
from autocorrect import Speller
import re
import contractions
import spacy
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load spacy's pre-trained model for NER
nlp = spacy.load('en_core_web_sm')

# Function to expand contractions
def expand_contractions(text):
    return contractions.fix(text)

# Function to clean and tokenize text
def clean_and_tokenize(text):
    # Remove non-ASCII characters
    text = unidecode(text)
    
    # Expand contractions
    text = expand_contractions(text)

    # Remove newlines, tabs, and excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # Tokenize text using NLTK's word tokenizer
    tokens = word_tokenize(text)
    
    # Remove punctuation and numbers
    tokens = [word for word in tokens if word.isalpha()]
    
    # Convert tokens back to a single string
    cleaned_text = " ".join(tokens)
    return cleaned_text

# Spell checker
spell = Speller(lang='en')

def correct_spelling(text):
    doc = nlp(text)
    corrected_words = []
    
    for token in doc:
        # Skip named entities (proper nouns)
        if token.ent_type_ in ['PERSON', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT']:
            corrected_words.append(token.text)
        else:
            corrected_words.append(spell(token.text))
    
    corrected_text = " ".join(corrected_words)
    return corrected_text

def process_document(obj):
    doc_id = obj['doc_id']
    text = obj['text']

    # Clean and tokenize text
    cleaned_text = clean_and_tokenize(text)
    
    # Correct spelling
    corrected_text = correct_spelling(cleaned_text)

    return {'doc_id': doc_id, 'text': corrected_text}

def process_corpus(input_file_path, output_file_path, batch_size=100):
    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Initialize output JSONL file for writing
        with jsonlines.open(output_file_path, mode='w') as writer:
            # Initialize multiprocessing pool
            pool = Pool(processes=cpu_count())

            try:
                # Process each document individually
                results = pool.imap(process_document, reader, chunksize=batch_size)

                # Write results to output file
                for result in results:
                    writer.write(result)
            finally:
                # Close multiprocessing pool
                pool.close()
                pool.join()


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/processed_corpus.jsonl'
process_corpus(input_file_path, output_file_path)
