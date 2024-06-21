import csv
import json
import concurrent.futures
import logging
from multiprocessing import cpu_count, Manager, Process, Queue
import memory_profiler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_qrel(qrel_path):
    """Parse qrel file and return a dictionary with query_id as key and doc_id as value."""
    qrel_dict = {}
    try:
        with open(qrel_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                query_id = parts[0]
                doc_id = parts[2]
                qrel_dict[query_id] = doc_id
        logging.info(f"Successfully parsed qrel file: {qrel_path}")
    except Exception as e:
        logging.error(f"Error parsing qrel file: {e}")
    return qrel_dict

def parse_results(results_path):
    """Parse results file and return a dictionary with query_id as key and list of (doc_id, rank) tuples as value."""
    results_dict = {}
    try:
        with open(results_path, 'r') as file:
            current_query_id = None
            rank = 0
            for line in file:
                line = line.strip()
                if line.startswith("Query ID:"):
                    current_query_id = line.split()[-1]
                    results_dict[current_query_id] = []
                    rank = 0
                elif line.startswith("Total number of matching documents:"):
                    continue
                elif current_query_id is not None and line:
                    rank += 1
                    results_dict[current_query_id].append((line, rank))
        logging.info(f"Successfully parsed results file: {results_path}")
    except Exception as e:
        logging.error(f"Error parsing results file: {e}")
    return results_dict

def load_index(index_path):
    """Load the index file into a dictionary."""
    index_dict = {}
    try:
        with open(index_path, 'r') as index_file:
            reader = csv.DictReader(index_file)
            for row in reader:
                index_dict[row['doc_id']] = int(row['offset'])
        logging.info(f"Successfully loaded index file: {index_path}")
    except Exception as e:
        logging.error(f"Error loading index file: {e}")
    return index_dict

def process_query(query_id, correct_doc_id, doc_ids_with_ranks, corpus_path, index_dict, output_queue):
    """Process a single query to find documents before the correct document and return their details."""
    results = []
    correct_doc_found = False

    try:
        with open(corpus_path, 'r') as corpus_file:
            for doc_id, rank in doc_ids_with_ranks:
                if doc_id == correct_doc_id:
                    correct_doc_found = True
                    break
                if doc_id in index_dict:
                    corpus_file.seek(index_dict[doc_id])
                    line = corpus_file.readline()
                    doc = json.loads(line)
                    doc['rank'] = rank
                    results.append(doc)
    except Exception as e:
        logging.error(f"Error processing query {query_id}: {e}")
    
    output_queue.put((query_id, results))

def write_results(output_queue, output_path):
    """Write results to output file."""
    with open(output_path, 'w') as out_file:
        while True:
            result = output_queue.get()
            if result is None:
                break
            query_id, results = result
            for doc in results:
                out_file.write(f"Query ID: {query_id}\n")
                out_file.write(f"Document ID: {doc['doc_id']}\n")
                out_file.write(f"Rank: {doc['rank']}\n")
                sections = "\n".join(f"{sec['section']} (start: {sec['start']}, end: {sec['end']})" for sec in doc.get('sections', []))
                out_file.write(f"Sections: {sections}\n")
                out_file.write(f"Text: {doc['text']}\n")
                out_file.write("\n")
                print(f"Query ID: {query_id} \n Document ID: {doc['doc_id']} \n Rank: {doc['rank']} \n Section: {doc['sections']} \n Text: {doc['text']}")
    logging.info(f"All results written to {output_path}")

#@memory_profiler.profile
def main():
    qrel_path = "/home/shuvam/Information_Retrieval/reults_bm25/qrel_querries/qrel.txt"
    results_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/results_k1_0_6_b_1_0_txt"
    corpus_path = "/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl"
    index_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/corpus_index.csv"
    output_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/all_results_before_corr_ans_indexing_approach.txt"


    qrel_dict = parse_qrel(qrel_path)
    results_dict = parse_results(results_path)
    index_dict = load_index(index_path)

    manager = Manager()
    output_queue = manager.Queue()
    num_workers = cpu_count()

    writer_process = Process(target=write_results, args=(output_queue, output_path))
    writer_process.start()

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for query_id, correct_doc_id in qrel_dict.items():
            if query_id in results_dict:
                doc_ids_with_ranks = results_dict[query_id]
                futures.append(executor.submit(process_query, query_id, correct_doc_id, doc_ids_with_ranks, corpus_path, index_dict, output_queue))
        
        for future in concurrent.futures.as_completed(futures):
            future.result()
    
    output_queue.put(None)
    writer_process.join()

if __name__ == "__main__":
    main()
