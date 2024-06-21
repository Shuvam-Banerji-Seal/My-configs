import jsonlines
import concurrent.futures
from rake_nltk import Rake
from unidecode import unidecode
from nltk.tokenize import RegexpTokenizer

def process_document(obj):
    doc_id = obj['doc_id']
    text = obj['text']

    # Convert Unicode to ASCII
    text = unidecode(text)

    # Tokenize text using NLTK RegexpTokenizer to handle newlines
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    # Join tokens back into a single string
    cleaned_text = ' '.join(tokens)

    # Initialize RAKE
    rake = Rake()

    # Extract keywords using RAKE
    rake.extract_keywords_from_text(cleaned_text)
    keywords = rake.get_ranked_phrases()

    # Print the current doc_id and extracted keywords
    print(f"Processing Document ID: {doc_id}")
    print("Keywords:", keywords)

    return {'doc_id': doc_id, 'keywords': keywords}

def extract_keywords_from_corpus(input_file_path, output_file_path):
    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Open the output JSONL file for writing
        with jsonlines.open(output_file_path, mode='w') as writer:
            # Process documents in parallel for faster extraction
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(process_document, reader)

                # Write results to the output JSONL file
                for result in results:
                    writer.write(result)


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
