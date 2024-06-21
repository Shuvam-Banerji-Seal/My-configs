import jsonlines
from nltk.tokenize import word_tokenize
from unidecode import unidecode
from multiprocessing import Pool, cpu_count, current_process
from autocorrect import Speller
import re
import contractions
import spacy
import nltk
import resource

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Ensure the SpaCy model is downloaded
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    from spacy.cli import download
    download('en_core_web_sm')
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
    
    # Join tokens to form the cleaned text while keeping punctuation
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

def update_sections(text, sections):
    updated_sections = []
    current_length = 0
    for section in sections:
        section_length = section['end'] - section['start']
        updated_sections.append({
            'start': current_length,
            'end': current_length + section_length,
            'section': section['section'],
            'text': text[current_length:current_length + section_length]  # Add this line to include the section text
        })
        current_length += section_length
    return updated_sections

def process_document(obj):
    doc_id = obj['doc_id']
    text = obj['text']
    sections = obj['sections']
    title = obj['title']
    wikidata_id = obj['wikidata_id']

    # Clean and tokenize text
    cleaned_text = clean_and_tokenize(text)
    
    # Correct spelling
    corrected_text = correct_spelling(cleaned_text)

    # Update section indices
    updated_sections = update_sections(corrected_text, sections)

    return {
        'doc_id': doc_id,
        'text': corrected_text,
        'sections': updated_sections,
        'title': title,
        'wikidata_id': wikidata_id
    }

def process_and_write_document(doc, output_file_path):
    try:
        process_id = current_process().name
        print(f"Processing document ID {doc['doc_id']} on {process_id}")
        processed_doc = process_document(doc)
        with jsonlines.open(output_file_path, mode='a') as writer:
            writer.write(processed_doc)
    except Exception as e:
        print(f"Error processing document ID {doc['doc_id']}: {e}")

def process_corpus(input_file_path, output_file_path):
    # Limit memory usage to 12GB
    resource.setrlimit(resource.RLIMIT_AS, (12 * 1024**3, 12 * 1024**3))

    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Initialize multiprocessing pool
        pool = Pool(processes=cpu_count())

        try:
            # Process each document individually
            for obj in reader:
                pool.apply_async(process_and_write_document, (obj, output_file_path))

            pool.close()
            pool.join()

        finally:
            pool.close()
            pool.join()


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/processed_corpus_2.jsonl'
process_corpus(input_file_path, output_file_path)
