import csv
import json
import concurrent.futures

def parse_qrel(qrel_path):
    """Parse qrel file and return a dictionary with query_id as key and doc_id as value."""
    qrel_dict = {}
    with open(qrel_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            query_id = parts[0]
            doc_id = parts[2]
            qrel_dict[query_id] = doc_id
    return qrel_dict

def parse_results(results_path):
    """Parse results file and return a dictionary with query_id as key and list of doc_ids as value."""
    results_dict = {}
    with open(results_path, 'r') as file:
        current_query_id = None
        for line in file:
            line = line.strip()
            if line.startswith("Query ID:"):
                current_query_id = line.split()[-1]
                results_dict[current_query_id] = []
            elif line.startswith("Total number of matching documents:"):
                continue
            elif current_query_id is not None:
                results_dict[current_query_id].append(line)
    return results_dict

def load_index(index_path):
    """Load the index file into a dictionary."""
    index_dict = {}
    with open(index_path, 'r') as index_file:
        reader = csv.DictReader(index_file)
        for row in reader:
            index_dict[row['doc_id']] = int(row['offset'])
    return index_dict

def process_query(query_id, correct_doc_id, doc_ids, corpus_path, index_dict):
    """Process a single query to find documents before the correct document and return their details."""
    results = []
    correct_doc_found = False
    doc_id_set = set(doc_ids)
    doc_index_map = {doc_id: idx for idx, doc_id in enumerate(doc_ids)}

    with open(corpus_path, 'r') as corpus_file:
        for doc_id in doc_ids:
            if doc_id == correct_doc_id:
                correct_doc_found = True
                break
            if doc_id in index_dict:
                corpus_file.seek(index_dict[doc_id])
                line = corpus_file.readline()
                doc = json.loads(line)
                results.append((doc_index_map[doc['doc_id']], doc))
    
    results.sort()
    return query_id, [doc for _, doc in results]

def write_results(query_id, results, output_path):
    """Write results to output file."""
    with open(output_path, 'a') as out_file:
        for doc in results:
            out_file.write(f"Query ID: {query_id}\n")
            out_file.write(f"Document ID: {doc['doc_id']}\n")
            sections = "\n".join(f"{sec['section']} (start: {sec['start']}, end: {sec['end']})" for sec in doc.get('sections', []))
            out_file.write(f"Sections: {sections}\n")
            out_file.write(f"Text: {doc['text']}\n")
            out_file.write("\n")

def main():
    qrel_path = "/home/shuvam/Information_Retrieval/reults_bm25/qrel_querries/qrel.txt"
    results_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/results_k1_0_6_b_1_0_txt"
    corpus_path = "/home/shuvam/Information_Retrieval/TREC_ToT_baselines/Corpu_and_dataset/corpus.jsonl"
    index_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/corpus_index.csv"
    output_path = "/home/shuvam/Information_Retrieval/reults_bm25/results_2/all_results_before_corr_ans_indexing_approach.txt"

    qrel_dict = parse_qrel(qrel_path)
    results_dict = parse_results(results_path)
    index_dict = load_index(index_path)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for query_id, correct_doc_id in qrel_dict.items():
            if query_id in results_dict:
                doc_ids = results_dict[query_id]
                futures.append(executor.submit(process_query, query_id, correct_doc_id, doc_ids, corpus_path, index_dict))
        
        for future in concurrent.futures.as_completed(futures):
            query_id, results = future.result()
            write_results(query_id, results, output_path)

if __name__ == "__main__":
    main()
