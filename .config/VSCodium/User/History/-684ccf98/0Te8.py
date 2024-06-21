import json
import csv
import concurrent.futures
import logging
from multiprocessing import cpu_count, Manager, Process

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_chunk(chunk, start_offset):
    """Process a chunk of the corpus and return doc_id and offset pairs."""
    results = []
    offset = start_offset
    for line in chunk:
        try:
            doc = json.loads(line)
            results.append((doc['doc_id'], offset))
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON at offset {offset}: {e}")
        offset += len(line)
    return results

def write_to_index(index_queue, index_path):
    """Write to the index file from the queue."""
    with open(index_path, 'w', newline='') as index_file:
        writer = csv.writer(index_file)
        writer.writerow(['doc_id', 'offset'])
        while True:
            result = index_queue.get()
            if result is None:
                break
            for doc_id, offset in result:
                writer.writerow([doc_id, offset])
    logging.info(f"Index creation completed successfully. Index file: {index_path}")

def create_index(corpus_path, index_path, chunk_size=1000):
    """Create an index file mapping doc_id to byte offset using multi-threading."""
    manager = Manager()
    index_queue = manager.Queue()
    num_workers = cpu_count()

    writer_process = Process(target=write_to_index, args=(index_queue, index_path))
    writer_process.start()

    try:
        with open(corpus_path, 'r') as corpus_file:
            corpus_file.seek(0, 2)
            file_size = corpus_file.tell()

            def generate_chunks():
                corpus_file.seek(0)
                while corpus_file.tell() < file_size:
                    start_offset = corpus_file.tell()
                    chunk = [corpus_file.readline() for _ in range(chunk_size)]
                    yield chunk, start_offset

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = {executor.submit(process_chunk, chunk, start_offset): (chunk, start_offset)
                           for chunk, start_offset in generate_chunks()}
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    index_queue.put(result)
    except Exception as e:
        logging.error(f"Failed to create index: {e}")
    finally:
        index_queue.put(None)
        writer_process.join()


if __name__ == "__main__":
    corpus_path = "/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl"
    index_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/corpus_index.csv"
    create_index(corpus_path, index_path)
