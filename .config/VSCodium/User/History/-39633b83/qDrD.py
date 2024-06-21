import json
import concurrent.futures
import os

def process_line(line):
    try:
        # Parse the JSON line
        doc = json.loads(line.strip())
        
        # Check if 'Abstract' is not in the sections list
        if "Abstract" not in doc.get('sections', []):
            # Extract doc_id, title, and sections
            filtered_doc = {
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "sections": doc["sections"]
            }
            # Return the filtered document as JSON string
            return json.dumps(filtered_doc)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def write_results(output_file, results):
    try:
        with open(output_file, 'a', encoding='utf-8') as outfile:
            for result in results:
                if result:
                    outfile.write(result + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

def process_chunk(chunk, output_file):
    results = [process_line(line) for line in chunk]
    write_results(output_file, results)

def filter_docs_without_abstract(input_file, chunk_size=50000):
    with open(input_file, 'r', encoding='utf-8') as infile:
        chunk = []
        for line in infile:
            chunk.append(line)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []

        # Yield any remaining lines
        if chunk:
            yield chunk

def parallel_processing(input_file, output_file, num_workers=None, chunk_size=50000):
    # Clear the output file first
    open(output_file, 'w').close()

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for chunk in filter_docs_without_abstract(input_file, chunk_size):
            futures.append(executor.submit(process_chunk, chunk, output_file))
        
        # Ensure all futures are completed
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing chunk: {e}")

# Define the input and output file paths
input_file_path = 'input.jsonl'
output_file_path = 'output.jsonl'

# Set the number of workers to the number of available CPU cores, or specify a custom number
num_workers = os.cpu_count()

# Call the function to filter documents using parallel processing
parallel_processing(input_file_path, output_file_path, num_workers=num_workers)


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
extract_keywords_from_corpus(input_file_path, output_file_path)
