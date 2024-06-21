import jsonlines
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode

def extract_keywords_from_corpus(input_file_path, output_file_path):
    # Initialize RAKE with NLTK's stopwords
    rake = Rake(stopwords=stopwords.words('english'))

    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Open the output JSONL file for writing
        with jsonlines.open(output_file_path, mode='w') as writer:
            for obj in reader:
                doc_id = obj['doc_id']
                text = obj['text']

                # Clean and normalize text (remove non-ASCII characters and normalize newlines)
                text = unidecode(text)
                text = text.replace("\n", " ")

                # Tokenize text using NLTK's word tokenizer
                tokens = word_tokenize(text)

                # Convert tokens back to a single string for RAKE
                cleaned_text = " ".join(tokens)

                # Extract keywords using RAKE
                rake.extract_keywords_from_text(cleaned_text)
                keywords = rake.get_ranked_phrases()

                # Print the current doc_id and extracted keywords
                print(f"Processing Document ID: {doc_id}")
                print("Keywords:", keywords)

                # Write the result to the output JSONL file
                writer.write({'doc_id': doc_id, 'keywords': keywords})


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
