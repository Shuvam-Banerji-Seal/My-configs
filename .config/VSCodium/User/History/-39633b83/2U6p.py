import jsonlines
from rake_nltk import Rake

def extract_keywords_from_corpus(input_file_path, output_file_path):
    # Initialize RAKE
    rake = Rake()

    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Open the output JSONL file for writing
        with jsonlines.open(output_file_path, mode='w') as writer:
            for obj in reader:
                doc_id = obj['doc_id']
                text = obj['text']

                # Extract keywords using RAKE
                rake.extract_keywords_from_text(text)
                keywords = rake.get_ranked_phrases()

                # Print the current doc_id and extracted keywords
                print(f"Processing Document ID: {doc_id}")
                print("Keywords:", keywords)

                # Write the result to the output JSONL file
                writer.write({'doc_id': doc_id, 'keywords': keywords})

# Example usage
input_file_path = 'corpus.jsonl'
output_file_path = 'keywords.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
